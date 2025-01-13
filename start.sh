#!/bin/bash

# Create a virtual environment if not already created
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install the required dependencies if they are not installed yet
pip install -r requirements.txt

# Ensure gunicorn is installed (if it's not already installed)
pip install gunicorn

# Start Flask app using Gunicorn in the background
.venv/bin/gunicorn -w 4 -b 0.0.0.0:5001 app.app:app &

# Start Streamlit app using a different port (8502 in this case)
python -m streamlit run sentiment_app.py --server.port 8502 --server.headless true
