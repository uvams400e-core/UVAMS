# ~/Orion_HQ/edge_nodes/edge_controller.py
import os
import time
from Orion_HQ.telemetry_buffer.telemetry_packer import pack_to_jsonl

# Path to the "Nest" (Outbox)
OUTBOX_PATH = "Orion_HQ/telemetry_buffer/outbox"

def check_for_harvest():
    """Returns True if the outbox is empty (Vee took the yield)."""
    # If the directory has 0 files, the harvest is complete
    return len(os.listdir(OUTBOX_PATH)) == 0

def start_astro_mission():
    print("🛰️ astro Mission Alpha Started: Collecting data...")
    # Simulated data collection
    fake_data = {"sensor": "PlutoSDR", "signal": "915MHz", "status": "Secure"}
    pack_to_jsonl(fake_data)

# --- THE MAIN LOOP ---
while True:
    if check_for_harvest():
        start_astro_mission()
        print("Waiting for Vee to harvest the new data...")
    else:
        # The yield is still there, so the node 'sleeps' to save power
        print("Outbox full. node is resting until the Mule arrives.")
    
    time.sleep(30) # Check every 30 seconds
