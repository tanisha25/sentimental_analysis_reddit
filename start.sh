#!/bin/bash

# Create virtual environment if not already created
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start Flask app using Gunicorn, bind to $PORT
.venv/bin/gunicorn -w 4 -b 127.0.0.1:$PORT app.app:app &

# Start Streamlit app on port 8502
python -m streamlit run sentiment_app.py --server.port 8502 --server.headless true
