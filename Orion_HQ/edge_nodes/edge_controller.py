import os
import time
import sys
# Force immediate output to terminal
print("🔥 SYSTEM BOOT: Orion HQ Controller is loading...", flush=True)

from Orion_HQ.orion_brain import analyze_signal
from Orion_HQ.security_monitor.shield import encrypt_packet
from Orion_HQ.telemetry_buffer.telemetry_packer import pack_to_jsonl

OUTBOX_PATH = "Orion_HQ/telemetry_buffer/outbox"

def check_for_harvest():
    if not os.path.exists(OUTBOX_PATH):
        os.makedirs(OUTBOX_PATH)
    return len(os.listdir(OUTBOX_PATH)) == 0

def start_astro_mission():
    print("🛰️  Astro Mission Alpha Started!", flush=True)
    fake_data = {"sensor": "PlutoSDR", "signal": "915MHz", "status": "Secure"}
    smart_packet = analyze_signal(fake_data)
    pack_to_jsonl(smart_packet)
    print("✅ Smart Honey Packed.", flush=True)

# --- THE EXECUTION ---
if __name__ == "__main__":
    print("🚀 Main Loop Engaged...", flush=True)
    while True:
        if check_for_harvest():
            start_astro_mission()
        else:
            print("⏸️  Outbox full. Node is resting...", flush=True)
        
        time.sleep(10) # Faster check for testing
