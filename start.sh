#!/bin/bash
set -e

cd "$(dirname "$0")"

# Create a virtual environment in .venv (only if it doesn't exist)
if [ ! -d .venv ]; then
    python -m venv .venv
fi
source .venv/bin/activate

# Upgrade pip (optional but helpful)
pip install --upgrade pip

# Install project dependencies, including gunicorn
pip install -r deps.txt

# Run the app
exec gunicorn brian:app --bind 0.0.0.0:"${PORT:-8000}"
