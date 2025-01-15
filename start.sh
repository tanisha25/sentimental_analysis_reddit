#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the tests
pytest test_sentiments.py

# Start the app
python app.py
