# ==========================================================
# 🛰️ UVAMS MISSION CONTROL BLUEPRINT (ORION_HQ)
# ==========================================================
# Author: Vee K. | Mission: ORION_ALPHA
# Logic: Zero-Trust / Encrypted-at-Rest / Sovereign Transport
# ==========================================================

# --- 1. CORE PATHS & PYTHON CONFIG ---
export UVAMS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${PYTHONPATH}:${UVAMS_ROOT}:${UVAMS_ROOT}/Orion_HQ"

# --- 2. GLOBAL MISSION SECRETS (THE SHIELD) ---
export ORION_SECRET_KEY="8u1_Byu_m-d_Q6L8-FzX8G6R6kGf9T5_XyJ6bK6u3E8="
export PLUTO_URI="usb:20.1.5"
export GCP_PROJECT_ID="uvams-pluto-node-2026"

# --- 3. HARDWARE ALIASES (THE HUNTER) ---
# Purpose: Direct capture from the PlutoSDR
alias vh-test-pluto='python3 "$UVAMS_ROOT/Orion_HQ/Pi_Node/pluto_test.py"'

# --- 4. LOGISTICS ALIASES (THE GATEKEEPER) ---
# Purpose: Process the mule payload through the local HQ logic
alias vh-gatekeeper='python3 "$UVAMS_ROOT/Orion_HQ/Mac_HQ/gatekeeper.py"'

# --- 5. DATA MANAGEMENT (THE MULE) ---
# Purpose: Quick count of data sitting in the pipeline layers
alias vh-status='echo "--- UVAMS MISSION STATUS ---"; \
echo "📡 Mule Payload: $(ls $UVAMS_ROOT/Orion_HQ/telemetry_buffer/mule_payload/*.jsonl 2>/dev/null | wc -l) new files"; \
echo "📦 Processed Data: $(ls $UVAMS_ROOT/Orion_HQ/telemetry_buffer/mule_payload/*.processed 2>/dev/null | wc -l) files"; \
echo "🧠 AI Brain Project: $GCP_PROJECT_ID"'

# --- 6. UTILITY ---
alias vh-cd='cd "$UVAMS_ROOT"'
alias vh-reset-honey='mv $UVAMS_ROOT/Orion_HQ/telemetry_buffer/mule_payload/*.processed $UVAMS_ROOT/Orion_HQ/telemetry_buffer/mule_payload/pluto_live.jsonl 2>/dev/null'

echo "🛰️ UVAMS Environment Engaged: Orion v1.0 Framework Active"
echo "📍 Root: $UVAMS_ROOT"
# ==========================================================
