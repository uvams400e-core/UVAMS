cat << 'EOF' > uvams_env.sh
# ==========================================================
# 🛰️ UVAMS MISSION CONTROL BLUEPRINT (VH_MISSION)
# ==========================================================
# Author: Vee K. | Mission: VH_ALPHA
# Logic: Zero-Trust / Encrypted-at-Rest / Sovereign Transport
# ==========================================================

# --- 1. CORE PATHS ---
# Automatically find the project root regardless of laptop user
export VH_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export VH_LAKE="gs://uvams-pluto-data-lake/vh_alpha"

# --- 2. THE node (Data Generation) ---
# Purpose: Starts the Harvester to collect, stamp, and encrypt 915MHz signals.
alias vh-node='python3 "$VH_ROOT/edge_nodes/pluto_harvester.py"'

# --- 3. THE HARVESTER (Local Logistics) ---
# Purpose: Moves encrypted files from the "Outbox" (Edge) to "Staging" (Transport).
alias vh-harvest='rsync -av --remove-source-files "$VH_ROOT/telemetry_buffer/outbox/" "$VH_ROOT/transport_layer/staging/"'

# --- 4. THE REAPER (Verification) ---
# Purpose: Decrypts Staging data and updates the "Clean Room" for local analysis.
alias vh-reap='python3 "$VH_ROOT/security_monitor/reaper.py"'

# --- 5. THE MULE (Cloud Archive) ---
# Purpose: Pushes encrypted data to the GCP Lake and clears local staging.
alias vh-mule-push='gsutil cp "$VH_ROOT/transport_layer/staging/"*.jsonl "$VH_LAKE/" && rm "$VH_ROOT/transport_layer/staging/"*.jsonl'

# --- 6. THE MASTER SYNC (End-of-Day) ---
# Purpose: Executes the full chain: Harvest -> Verify -> Archive in one click.
alias vh-sync='vh-harvest && vh-reap && vh-mule-push'

# --- 7. MISSION STATUS (Audit) ---
# Purpose: Quick count of data sitting in each layer of the pipeline.
alias vh-status='echo "--- UVAMS MISSION STATUS ---"; \
echo "🛰️ Outbox (Edge):  $(ls $VH_ROOT/telemetry_buffer/outbox/ 2>/dev/null | wc -l) files"; \
echo "🚜 Staging (Mule):  $(ls $VH_ROOT/transport_layer/staging/ 2>/dev/null | wc -l) files"; \
echo "💎 Clean Room:     $(ls $VH_ROOT/transport_layer/clean_room/ 2>/dev/null | wc -l) files"; \
echo "☁️  Cloud Lake:     $(gsutil ls $VH_LAKE | wc -l) objects"'

# --- 8. NAVIGATION ---
alias vh-cd='cd "$VH_ROOT"'

echo "🛰️ UVAMS Environment Active: $VH_ROOT"
# ==========================================================
EOF

source uvams_env.sh
