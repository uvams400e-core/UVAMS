import subprocess

def trigger_sync(container_name):
    print(f"📡 Requesting Sync for: {container_name}")
    
    # We use a simpler string structure to avoid escape-character hell
    # We call python3 -m to treat it as a module directly
    cmd = (
        f"docker exec {container_name} python3 -c "
        f"'import sys; sys.path.append(\"/app\"); "
        f"from src.mule import rotate_vault, upload_to_gcs; "
        f"p = rotate_vault(\"{container_name.upper()}\"); "
        f"upload_to_gcs(p) if p else print(\"No vault\")'"
    )
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"❌ Error on {container_name}: {result.stderr}")

if __name__ == "__main__":
    nodes = ["vh-gs-1", "vh-gs-2", "vh-gs-3"]
    for node in nodes:
        trigger_sync(node)
