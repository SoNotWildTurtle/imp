#!/bin/bash
# remember to chmod +x imp/bin/imp-start.sh

echo "Starting IMP AI System..."
nohup python3 /root/imp/core/imp-execute.py &

# determine the project root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

nohup python3 "$ROOT/core/imp-learning-memory.py" &
nohup python3 "$ROOT/core/imp-strategy-generator.py" &
nohup python3 "$ROOT/self-improvement/imp-code-updater.py" &
nohup python3 "$ROOT/security/imp-security-optimizer.py" &
nohup python3 "$ROOT/expansion/imp-cluster-manager.py" &

echo "IMP AI is now running."

