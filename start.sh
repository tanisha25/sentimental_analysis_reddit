#!/bin/bash
# Activate the virtual environment
source .venv/bin/activate

# Export FLASK_URL for Streamlit
export FLASK_URL=http://0.0.0.0:5001

# Start Flask app using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app.app:app
