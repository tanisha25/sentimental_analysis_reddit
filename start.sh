#!/bin/bash
# Activate the virtual environment
source .venv/bin/activate

# Use the PORT provided by Render
export FLASK_URL="http://0.0.0.0:$PORT"

# Start Flask app using Gunicorn
gunicorn -w 4 -b 0.0.0.0:$PORT app.app:app
