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

# Start Flask app using Gunicorn
.venv/bin/gunicorn -w 4 -b 0.0.0.0:$PORT app.app:app &
FLASK_PID=$!

# Start Streamlit app on a different port
python -m streamlit run sentiment_app.py --server.port 8502 --server.headless true &
STREAMLIT_PID=$!

# Wait for both processes to exit
wait $FLASK_PID $STREAMLIT_PID
