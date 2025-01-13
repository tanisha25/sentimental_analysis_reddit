#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Start Flask app using Gunicorn
gunicorn -w 4 -b 0.0.0.0:$PORT app.app:app &

# Start Streamlit app
python -m streamlit run sentiment_app.py --server.port $PORT --server.headless true
