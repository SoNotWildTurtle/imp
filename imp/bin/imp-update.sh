#!/bin/bash
#chmod +x /root/imp/bin/imp-update.sh

echo "Fetching latest updates for IMP..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

git -C "$ROOT_DIR" pull origin main
python3 "$ROOT_DIR/self-improvement/imp-code-updater.py"
echo "IMP AI has been updated."
