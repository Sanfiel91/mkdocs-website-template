#!/bin/bash

set -euo pipefail

echo "Starting combined EN/ES development server..."

if [ -x ".venv/bin/python" ]; then
    .venv/bin/python scripts/dev_server.py --host 0.0.0.0 --port 8005
else
    python3 scripts/dev_server.py --host 0.0.0.0 --port 8005
fi
