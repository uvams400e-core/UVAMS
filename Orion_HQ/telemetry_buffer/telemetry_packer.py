# ~/Orion_HQ/telemetry_buffer/telemetry_packer.py
import json
import os
import datetime

# Mission Root Path
DATA_DIR = "Orion_HQ/telemetry_buffer/outbox"

import json
import os

def pack_to_jsonl(data_dict):
    """
    Appends a dictionary as a single line of JSON to the outbox.
    Works perfectly for AI-tagged 'smart_packets'.
    """
    # Use the variables we calibrated earlier
    mission_id = "ORION_ALPHA"
    DATA_DIR = "Orion_HQ/telemetry_buffer/outbox"
    file_path = os.path.join(DATA_DIR, f"{mission_id}_telemetry.jsonl")

    # The 'a' mode ensures we append without overwriting the old 'honey'
    with open(file_path, "a") as f:
        # Convert dictionary to string and add a newline
        f.write(json.dumps(data_dict) + "\n")
