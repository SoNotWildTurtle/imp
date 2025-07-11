#!/bin/bash
# Simple wrapper to run the motivation engine
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/../core/imp-motivation.py"
