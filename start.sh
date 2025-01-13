#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Start Flask app using Gunicorn in the background
.venv/bin/gunicorn -w 4 -b 0.0.0.0:5001 app.app:app &

# Start Streamlit app using a different port (8502 in this case)
python -m streamlit run sentiment_app.py --server.port 8502 --server.headless true
