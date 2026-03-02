import json
import os
import sys
from security_monitor.shield import decrypt_yield

# Paths
STAGING_DIR = "transport_layer/staging"
CLEAN_ROOM = "transport_layer/clean_room"

# The Proprietary Signature we expect to find inside the data
EXPECTED_SIG = "ALPHA-STAMP-2026-400EB-VH"

def reap_data():
    """Decrypts, validates ownership, and archives telemetry."""
    if not os.path.exists(CLEAN_ROOM):
        os.makedirs(CLEAN_ROOM)

    files = [f for f in os.listdir(STAGING_DIR) if f.endswith('.jsonl')]
    
    if not files:
        print("📭 Staging is empty. No telemetry to reap.")
        return

    print(f"🕵️  Reaper active. Analyzing {len(files)} mission file(s)...")
    
    for filename in files:
        src_path = os.path.join(STAGING_DIR, filename)
        dest_path = os.path.join(CLEAN_ROOM, f"DECRYPTED_{filename}")
        
        valid_records = 0
        total_records = 0

        with open(src_path, "r") as f_in, open(dest_path, "w") as f_out:
            for line in f_in:
                total_records += 1
                try:
                    envelope = json.loads(line)
                    ciphertext = envelope.get("payload")
                    
                    if ciphertext:
                        # 1. Decrypt
                        cleartext = decrypt_yield(ciphertext.encode())
                        data = json.loads(cleartext)
                        
                        # 2. Verify Proprietary Stamp
                        sig = data.get("governance", {}).get("signature")
                        if sig == EXPECTED_SIG:
                            # 3. Save to Clean Room
                            f_out.write(json.dumps(data) + "\n")
                            valid_records += 1
                        else:
                            print(f"❌ INVALID STAMP FOUND: Data may be compromised or foreign.")
                            
                except Exception as e:
                    print(f"⚠️  Decryption error on record {total_records}: {e}")

        print(f"✅ Finished {filename}: {valid_records}/{total_records} records verified and reaped.")

if __name__ == "__main__":
    try:
        reap_data()
    except KeyboardInterrupt:
        print("\n🛑 Reaper suspended.")
        sys.exit(0)
