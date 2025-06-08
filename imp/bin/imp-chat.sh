#!/bin/bash
# Launch the IMP goal chatbot
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-online}"
python3 "$ROOT/core/imp-goal-chat.py" --mode "$MODE"
