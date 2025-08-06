#!/bin/bash
# Run the automated defense cycle
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/security/imp-automated-defense.py" "$@"
