#!/bin/bash
# Monitor network connections
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/security/imp-network-monitor.py" "$@"
