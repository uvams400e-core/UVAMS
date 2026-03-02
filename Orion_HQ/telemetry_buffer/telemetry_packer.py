# ~/Orion_HQ/telemetry_buffer/telemetry_packer.py
import json
import os
import datetime

# Mission Root Path
DATA_DIR = "Orion_HQ/telemetry_buffer/outbox"

def pack_to_jsonl(payload, mission_id="ORION_ALPHA"):
    """
    Converts raw data into a single JSONL line with a timestamp.
    """
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = {
        "mission": mission_id,
        "timestamp": timestamp,
        "data": payload
    }
    
    file_path = os.path.join(DATA_DIR, f"{mission_id}_telemetry.jsonl")
    
    # Append to the file (The 'Honey' accumulating in the Nest)
    with open(file_path, "a") as f:
        f.write(json.dumps(record) + "\n")
    
    print(f"Packed new telemetry to {file_path}")

# Example Usage:
# pack_to_jsonl({"node_id": "Marfa-Pi-01", "status": "active", "temp": 32})
