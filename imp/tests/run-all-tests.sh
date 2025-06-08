#!/bin/bash
#chmod +x /root/imp/tests/run-all-tests.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 Running Full IMP System Test Suite..."

python3 "$SCRIPT_DIR/test-core-functions.py"
python3 "$SCRIPT_DIR/test-security.py"
python3 "$SCRIPT_DIR/test-performance.py"
python3 "$SCRIPT_DIR/test-expansion.py"
python3 "$SCRIPT_DIR/test-self-improvement.py"
python3 "$SCRIPT_DIR/test-neural-network.py"
python3 "$SCRIPT_DIR/test-intranet.py"
python3 "$SCRIPT_DIR/test-metacognition.py"
python3 "$SCRIPT_DIR/test-config.py"
python3 "$SCRIPT_DIR/test-logs.py"
python3 "$SCRIPT_DIR/test-install.py"

echo "✅ All Tests Completed!"
