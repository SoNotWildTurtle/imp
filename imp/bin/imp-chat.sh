#!/bin/bash
# Launch the IMP goal chatbot
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/core/imp-goal-chat.py" "$@"
