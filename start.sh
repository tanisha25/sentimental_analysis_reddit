#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Start Flask app using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.app:app &

# Start Streamlit app
python -m streamlit run streamlit.py --server.port $STREAMLIT_PORT --server.headless true
