#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start Flask app in the background
python -m app.app &  # Start Flask app in the background