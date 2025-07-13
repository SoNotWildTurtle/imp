#!/bin/bash

echo "🚀 Running Full IMP System Test Suite..."

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
BASE_DIR="$(dirname "$SCRIPT_DIR")"

python3 "$SCRIPT_DIR/test-core-functions.py"
python3 "$SCRIPT_DIR/test-security.py"
python3 "$SCRIPT_DIR/test-performance.py"
python3 "$SCRIPT_DIR/test-expansion.py"
python3 "$SCRIPT_DIR/test-self-improvement.py"
python3 "$SCRIPT_DIR/test-code-quality.py"
python3 "$SCRIPT_DIR/test-metacognition.py"
python3 "$SCRIPT_DIR/test-conversation-analyzer.py"
python3 "$SCRIPT_DIR/test-perception-analyzer.py"
python3 "$SCRIPT_DIR/test-interaction.py"
python3 "$SCRIPT_DIR/test-gi-builder.py"
python3 "$SCRIPT_DIR/test-gi-conversation-builder.py"
python3 "$SCRIPT_DIR/test-gi-creator.py"
python3 "$SCRIPT_DIR/test-gi-goal-viewer.py"
python3 "$SCRIPT_DIR/test-gi-profile-manager.py"
python3 "$SCRIPT_DIR/test-gi-communicator.py"
python3 "$SCRIPT_DIR/test-gi-evolution-planner.py"
python3 "$SCRIPT_DIR/test-config.py"
python3 "$SCRIPT_DIR/test-logs.py"

echo "✅ All Tests Completed!"
