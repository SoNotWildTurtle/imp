#!/bin/bash
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/security/imp-authenticator.py" "$@"
