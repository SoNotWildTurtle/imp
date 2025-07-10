#!/bin/bash
# Simple wrapper for IMP code enhancement
# Usage: imp-enhance.sh [offline|online|auto]
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-auto}"
python3 "$ROOT/self-improvement/imp-code-updater.py" --mode "$MODE"

