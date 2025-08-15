#!/bin/bash
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/core/imp-voice-menu.py" "$@"
