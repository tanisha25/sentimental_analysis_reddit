#!/bin/bash

# Create virtual environment if not already created
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start Flask app in the background using Gunicorn
.venv/bin/gunicorn -w 4 -b 0.0.0.0:$PORT app.app:app &

# Start Streamlit app on a fixed port
.venv/bin/python -m streamlit run sentiment_app.py --server.port 8502 --server.headless true
