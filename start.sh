#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start Flask app in the background
python -m app.app &  # Start Flask app in the background

# Start Streamlit app
streamlit run sentiment_app.py --server.port $PORT --server.headless true  # Use the same port as Flask
