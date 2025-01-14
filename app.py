import os
from dotenv import load_dotenv
from app import create_app
from app.logger import configure_logger

# Load environment variables
load_dotenv()

# Create the Flask app instance
app = create_app()

# Set up logging
logger = configure_logger()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Use the PORT from the environment, default to 5000 if not set
    app.run(host="0.0.0.0", port=port)
