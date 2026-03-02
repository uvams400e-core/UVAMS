import sqlite3
import pandas as pd
import os

def harvest_station(station_path, station_name):
    db_path = os.path.join(station_path, "uvams_vault.db")
    if not os.path.exists(db_path):
        return None
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM satellite_hits", conn)
    df['source_station'] = station_name
    conn.close()
    return df

# Harvest both Station A and Station B
df_a = harvest_station("data/a", "VAN_HORN_01")
df_b = harvest_station("data/b", "VAN_HORN_02")

# Combine them into one "Master Record" on your laptop
master_record = pd.concat([df_a, df_b])
print(f"🛰️ Harvest Complete: {len(master_record)} total hits collected from the astro.")
print(master_record.tail())
