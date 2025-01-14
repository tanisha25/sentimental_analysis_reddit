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
    app.run(debug=True, use_reloader=False, port=os.getenv('PORT'), host='0.0.0.0')  # Disable reloader to avoid running Flask twice

