#!/bin/bash
set -e  # exit on any error

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Optional: create/activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r deps.txt

# Start the app
exec gunicorn brian:app --bind 0.0.0.0:"${PORT:-8000}"
