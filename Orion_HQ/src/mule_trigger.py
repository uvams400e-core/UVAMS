import sys
import os

# Ensure /app is in the path so we can find our other files
sys.path.append('/app')

from src.mule import rotate_vault, upload_to_gcs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mule_trigger.py NODE_NAME")
        sys.exit(1)
        
    node_name = sys.argv[1]
    print(f"🔄 Starting rotation for {node_name}...")
    
    path = rotate_vault(node_name)
    if path:
        success = upload_to_gcs(path)
        if success:
            print(f"✅ Sync complete for {node_name}")
        else:
            print(f"⚠️ Upload failed for {node_name}, file saved locally.")
    else:
        print(f"❌ No vault file found for {node_name}")
