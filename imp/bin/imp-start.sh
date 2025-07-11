#!/bin/bash
# remember to chmod +x /root/imp/bin/imp-start.sh

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# Launch from an absolute path so startup works even if the cwd changes
nohup python3 /root/imp/core/imp-execute.py &

echo "Starting IMP AI System..."
nohup python3 "$ROOT/core/imp-learning-memory.py" &
nohup python3 "$ROOT/core/imp-strategy-generator.py" &
nohup python3 "$ROOT/self-improvement/imp-code-updater.py" &
nohup python3 "$ROOT/security/imp-security-optimizer.py" &
nohup python3 "$ROOT/expansion/imp-cluster-manager.py" &
nohup python3 "$ROOT/core/imp-mood-manager.py" &
echo "IMP AI is now running."

