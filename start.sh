#!/bin/bash
# Activate the virtual environment
source .venv/bin/activate

# Start Flask app in the background using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
