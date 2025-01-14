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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=8080)
