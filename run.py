import subprocess
import threading
import sys
from app import create_app
from app.utils.logger import configure_logger

# Initialize the Flask app
app = create_app()

# Set up logging
logger = configure_logger()

def run_flask():
    """Function to run Flask app."""
    app.run(debug=True, use_reloader=False)  # Disable reloader to avoid running Flask twice

def run_streamlit():
    """Function to run Streamlit app."""
    try:
        # Run Streamlit app using subprocess
        subprocess.run([sys.executable, "-m", "streamlit", "run", "sentiment_app.py"])
    except Exception as e:
        logger.error(f"Error running Streamlit: {e}")

if __name__ == '__main__':
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run Streamlit in the main thread
    run_streamlit()
