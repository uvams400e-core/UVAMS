import os
import shutil
import time
import sqlite3
import json
from google.cloud import storage

def rotate_vault(node_id):
    source = "/app/data/uvams_vault.db"
    if not os.path.exists(source): return None
    
    timestamp = int(time.time())
    # Keep local backup on your MacBook
    backup_path = f"/app/data/backup_{node_id}_{timestamp}.db"
    shutil.copy(source, backup_path)
    
    jsonl_path = f"/app/data/upload_{node_id}_{timestamp}.jsonl"
    
    try:
        conn = sqlite3.connect(source)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # ARCHITECT HACK: Auto-detect the first table name in the DB
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if not tables:
            print("❌ SQLite Error: No tables found in vault.")
            return None
        
        actual_table_name = tables[0]['name']
        print(f"📊 Extracting from table: {actual_table_name}")
        
        cursor.execute(f"SELECT * FROM {actual_table_name}")
        rows = cursor.fetchall()
        
        with open(jsonl_path, 'w') as f:
            for row in rows:
                # We inject the node_id and a processed_at timestamp for the Data Lake
                record = dict(row)
                record['node_id'] = node_id
                record['processed_at'] = timestamp
                f.write(json.dumps(record) + '\n')
        
        conn.close()
        os.remove(source) 
        return jsonl_path
    except Exception as e:
        print(f"❌ Transformation failed: {e}")
        return None

def upload_to_gcs(file_path):
    # (Same upload logic as before)
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob_name = f"vh_sat_telemetry/{os.path.basename(file_path)}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        os.remove(file_path)
        print(f"✅ Uploaded {os.path.basename(file_path)} to GCS.")
        return True
    except Exception as e:
        print(f"⚠️ Upload failed: {e}")
        return False
