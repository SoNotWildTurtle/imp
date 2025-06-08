#!/bin/bash

# Simple wrapper to execute all test modules relative to this script's location
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 Running Full IMP System Test Suite..."

python3 "$DIR/test-core-functions.py"
python3 "$DIR/test-security.py"
python3 "$DIR/test-performance.py"
python3 "$DIR/test-expansion.py"
python3 "$DIR/test-self-improvement.py"
python3 "$DIR/test-config.py"
python3 "$DIR/test-logs.py"

echo "✅ All Tests Completed!"
