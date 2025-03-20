#!/bin/bash
#chmod +x /root/imp/tests/run-all-tests.sh

echo "🚀 Running Full IMP System Test Suite..."

python3 /root/imp/tests/test-core-functions.py
python3 /root/imp/tests/test-security.py
python3 /root/imp/tests/test-performance.py
python3 /root/imp/tests/test-expansion.py
python3 /root/imp/tests/test-self-improvement.py
python3 /root/imp/tests/test-config.py
python3 /root/imp/tests/test-logs.py

echo "✅ All Tests Completed!"
