#!/bin/bash
# remember to chmod +x /root/imp/bin/imp-start.sh

echo "🔥 Starting IMP AI System..."
nohup python3 /root/imp/imp-execute.py &
nohup python3 /root/imp/core/imp-learning-memory.py &
nohup python3 /root/imp/core/imp-strategy-generator.py &
nohup python3 /root/imp/self-improvement/imp-code-updater.py &
nohup python3 /root/imp/security/imp-security-optimizer.py &
nohup python3 /root/imp/expansion/imp-cluster-manager.py &

echo "✅ IMP AI is now running."
