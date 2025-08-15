#!/bin/bash
# Simple script to query or adjust IMP's mood
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="python3"

case "$1" in
    --get)
        $PYTHON "$ROOT/core/imp-mood-manager.py" --get
        ;;
    --adjust)
        shift
        $PYTHON "$ROOT/core/imp-mood-manager.py" --adjust "$1"
        ;;
    --decay)
        $PYTHON "$ROOT/core/imp-mood-manager.py" --decay
        ;;
    --event)
        shift
        $PYTHON "$ROOT/core/imp-mood-manager.py" --event "$1"
        ;;
    *)
        echo "Usage: $0 --get | --adjust <delta> | --decay | --event <type>"
        exit 1
        ;;
esac

