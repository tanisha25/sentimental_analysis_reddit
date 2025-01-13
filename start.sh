#!/bin/bash

# Create a virtual environment if not already created
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start Flask app using Gunicorn on the public Render port ($PORT)
.venv/bin/gunicorn -w 4 -b 0.0.0.0:$PORT app.app:app &
FLASK_PID=$!

# Wait for the Flask process to exit
wait $FLASK_PID
