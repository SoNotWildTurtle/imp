#!/bin/bash
# Simple wrapper for goal management
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CMD="$1"
shift || true

case "$CMD" in
    add)
        python3 "$ROOT/core/imp-goal-manager.py" "$@"
        ;;
    list)
        python3 - "$@" <<'PY'
from pathlib import Path
import json
root = Path(__file__).resolve().parents[2]
file = root / 'logs' / 'imp-goals.json'
if file.exists():
    goals = json.load(open(file))
    for g in goals:
        print(f"{g.get('status')} - {g.get('priority')} - {g.get('goal')}")
else:
    print('No goals found.')
PY
        ;;
    execute)
        python3 "$ROOT/core/imp-task-executor.py" "$@"
        ;;
    *)
        echo "Usage: $0 {add|list|execute}"
        ;;
esac
