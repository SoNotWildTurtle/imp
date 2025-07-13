#!/bin/bash
# Install required Python packages and start IMP
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REQUIREMENTS="$ROOT/requirements.txt"

if [ -f "$REQUIREMENTS" ]; then
    echo "Installing Python requirements..."
    pip3 install -r "$REQUIREMENTS"
fi

"$ROOT/bin/imp-start.sh"
