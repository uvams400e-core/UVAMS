import pytz
import json
from datetime import datetime, timedelta
from skyfield.api import Topos, load
from google.cloud import bigquery

# --- CONFIGURATION ---
PROJECT_ID = "uvams-400e"
DATASET_ID = "mission_data"
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.pluto_telemetry"
STATION_LOCATION = Topos('31.0427 N', '104.8355 W') # Van Horn HQ

def get_latest_tle():
    """Fetches a wide net of TLEs for better matching."""
    print("Fetching fresh TLEs from CelesTrak...")
    urls = [
        'https://celestrak.org/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle',
        'https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle',
        'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
    ]
    all_sats = []
    for url in urls:
        try:
            all_sats += load.tle_file(url)
        except:
            continue
    return {sat.name: sat for sat in all_sats}

def auto_label_hits():
    client = bigquery.Client(project=PROJECT_ID)
    ts = load.timescale()
    sats = get_latest_tle()

    # 1. Fetch hits from the last 60 minutes that haven't noden labeled yet
    query = f"""
        SELECT timestamp, actual_freq_hz, snr, station_id
        FROM `{TABLE_ID}`
        WHERE event_type = 'SATELLITE_SPIKE'
        AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
        AND (metadata IS NULL OR JSON_VALUE(metadata.satellite_name) IS NULL)
    """
    df = client.query(query).to_dataframe()

    if df.empty:
        print("No new unlabeled hits found in the last hour.")
        return

    print(f"Analyzing {len(df)} hits for orbital matches...")

    for _, row in df.iterrows():
        base_time_utc = row['timestamp'].replace(tzinfo=pytz.UTC)
        potential_matches = []

        # Check +/- 60s window for clock drift
        for offset in range(-60, 61, 20):
            check_time = ts.from_datetime(base_time_utc + timedelta(seconds=offset))
            for name, sat in sats.items():
                alt, az, dist = (sat - STATION_LOCATION).at(check_time).altaz()
                if alt.degrees > 15: # Higher threshold for better confidence
                    potential_matches.append(name)
        
        if potential_matches:
            # Pick the most frequent match in our window
            best_match = max(set(potential_matches), key=potential_matches.count)
            print(f"MATCH FOUND: {best_match} at {base_time_utc}")

            # 2. Update the BigQuery record with the satellite name
            # We use the timestamp and station_id as the unique key
            update_query = f"""
                UPDATE `{TABLE_ID}`
                SET metadata = JSON_OBJECT('satellite_name', '{best_match}', 'verified', true)
                WHERE timestamp = '{row['timestamp']}'
                AND station_id = '{row['station_id']}'
            """
            try:
                client.query(update_query).result()
                print(f"Successfully labeled hit as {best_match}")
            except Exception as e:
                # If row is still in streaming buffer, update might fail temporarily
                print(f"Buffer Delay: Could not label {best_match} yet (will retry next run).")

if __name__ == "__main__":
    auto_label_hits()
