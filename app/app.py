import subprocess
import threading
import sys
import os
from dotenv import load_dotenv
from app import create_app
from app.utils.logger import configure_logger

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = create_app()

# Set up logging
logger = configure_logger()

def run_flask():
    """Function to run Flask app."""
    flask_port = os.getenv('FLASK_PORT', 5001)  # Use environment variable for Flask port, default to 5001
    try:
        app.run(debug=True, use_reloader=False, port=flask_port, host='0.0.0.0')  # Disable reloader to avoid running Flask twice
    except Exception as e:
        logger.error(f"Error running Flask: {e}")

def run_streamlit():
    """Function to run Streamlit app."""
    try:
        streamlit_port = os.getenv('STREAMLIT_PORT', '8501')  # Use environment variable for Streamlit port, default to 8501
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "sentiment_app.py", "--server.port", streamlit_port, "--server.headless", "true"])
        logger.info(f"Streamlit app is running on port {streamlit_port}.")
    except Exception as e:
        logger.error(f"Error running Streamlit: {e}")

if __name__ == '__main__':
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run Streamlit in the main thread
    run_streamlit()
