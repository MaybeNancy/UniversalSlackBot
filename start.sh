#!/bin/bash
# Install dependencies (same as buildCommand)
pip install -r deps.txt

# Start the app (same as startCommand)
gunicorn brian:app
