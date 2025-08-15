#!/bin/bash
# Run the network auditor
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/security/imp-network-auditor.py" "$@"
