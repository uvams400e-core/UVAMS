#!/bin/bash

# 1. Identify current state
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "------------------------------------------------"
echo "🚀 UVAMS MISSION CONTROL: GIT CHECK-IN"
echo "Current Branch: $BRANCH"
echo "------------------------------------------------"

# 2. Show what is about to be committed
echo "[*] Changes detected:"
git status -s

# 3. Prompt for the Mission Log (Commit Message)
echo ""
echo "Enter your mission log message (e.g., 'Calibrated RFI threshold for Van Horn'):"
read -r MISSION_LOG

if [ -z "$MISSION_LOG" ]; then
    echo "[!] Error: You must provide a message. Commit aborted."
    exit 1
fi

# 4. Execute the Check-in
echo "[*] Adding changes..."
git add .

echo "[*] Locking into $BRANCH..."
git commit -m "$MISSION_LOG"

echo "------------------------------------------------"
echo "✅ Logged to $BRANCH: $MISSION_LOG"
echo "------------------------------------------------"
