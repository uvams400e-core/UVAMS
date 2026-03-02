import time
import random
import os
import json
from datetime import datetime

# Path to the outbox (The Nest)
OUTBOX_DIR = "telemetry_buffer/outbox"

from security_monitor.shield import encrypt_yield
import json

def pack_to_jsonl(data):
    os.makedirs(OUTBOX_DIR, exist_ok=True)
    filename = f"mission_data_{datetime.now().strftime('%Y%m%d')}.jsonl"
    filepath = os.path.join(OUTBOX_DIR, filename)
    
    # 1. Add metadata
    data['timestamp'] = datetime.utcnow().isoformat() + "Z"
    
    # 2. Encrypt the entire payload
    cleartext = json.dumps(data)
    ciphertext = encrypt_yield(cleartext)
    
    # 3. Store as a hex-string or base64 in the JSONL
    with open(filepath, "a") as f:
        # We store the encrypted block so the file remains JSONL compatible
        f.write(json.dumps({"v": "1", "payload": ciphertext.decode()}) + "\n")

def get_signal_data():
    """Attempts to read from PlutoSDR, otherwise mocks data."""
    try:
        # Placeholder for real hardware logic
        # import adi
        # sdr = adi.Pluto("ip:192.168.2.1")
        # return {"signal_strength": sdr.rx_power_db(), "mode": "HARDWARE"}
        raise Exception("Hardware not connected")
    except Exception:
        return {
            "mission": "VH_ALPHA",
            "signal_strength": round(random.uniform(-95, -45), 2),
            "source_node": "MB_AIR_SIM",
            "status": "MOCK_MODE"
        }

if __name__ == "__main__":
    print("🛰️ Bee is starting... Press Ctrl+C to stop.")
    try:
        while True:
            payload = get_signal_data()
            pack_to_jsonl(payload)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] yield Stored: {payload['signal_strength']} dBm")
            time.sleep(5) 
    except KeyboardInterrupt:
        print("\n🛰️ Bee is resting. Mission paused.")
