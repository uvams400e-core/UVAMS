import os
import sys
import json
import base64
from cryptography.fernet import Fernet

# --- THE HARD-CODED MISSION KEY ---
# This is exactly 32 bytes of entropy.
TEST_KEY = b'8u1_Byu_m-d_Q6L8-FzX8G6R6kGf9T5_XyJ6bK6u3E8='

# 1. Force Absolute Paths
BASE_DIR = os.getcwd() # This is /Users/venkat/Documents/UVAMS
PAYLOAD_DIR = os.path.join(BASE_DIR, "Orion_HQ/telemetry_buffer/mule_payload")

def main():
    print(f"🛸 Gatekeeper Active: Standing watch at {BASE_DIR}")
    
    if not os.path.exists(PAYLOAD_DIR):
        print(f"❌ ERROR: Cannot find folder: {PAYLOAD_DIR}")
        return

    # 2. Identify the Harvest
    files = [f for f in os.listdir(PAYLOAD_DIR) if f.endswith(".jsonl")]
    print(f"📦 Files detected in the Mule: {files}")

    if not files:
        print("📭 The Mule is empty. No new data to process.")
        return

    for filename in files:
        file_path = os.path.join(PAYLOAD_DIR, filename)
        print(f"🔄 Opening: {filename}...")
        
        with open(file_path, "rb") as f:
            for line in f:
                # Decrypt and analyze logic goes here
                print(f"✨ Decrypting packet from {filename}...")
                # result = decrypt_packet(line)
                # print(f"🧠 Analysis: {result}")

        # 3. Archive the work
        os.rename(file_path, file_path + ".processed")
        print(f"✅ Archived: {filename}")

if __name__ == "__main__":
    main()
