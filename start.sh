#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Start Flask app in the background using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app &

# Start Streamlit app
python -m streamlit run sentiment_app.py --server.port $STREAMLIT_PORT --server.headless true
