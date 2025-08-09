#!/bin/bash
# Launch the IMP self-healer
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/self-improvement/imp-self-healer.py" "$@"
