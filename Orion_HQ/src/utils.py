import yaml
from google.cloud import bigquery

def generate_report():
    with open("config/uvams_config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    client = bigquery.Client(project=config['gcp']['project_id'])
    query = f"""
        SELECT JSON_VALUE(metadata, '$.satellite_name') as sat, COUNT(*) as hits, ROUND(AVG(snr), 2) as snr
        FROM `{config['gcp']['project_id']}.mission_data.pluto_telemetry`
        WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
        GROUP BY 1 ORDER BY hits DESC
    """
    df = client.query(query).to_dataframe()
    print("\n--- DAILY MISSION SUMMARY ---")
    print(df.to_string(index=False))
