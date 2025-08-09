#!/bin/bash
# Trigger automatic verification and healing
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/self-improvement/imp-auto-heal.py" "$@"
