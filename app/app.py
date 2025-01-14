import os
from dotenv import load_dotenv
from app import create_app
from app.utils.logger import configure_logger

# Load environment variables
load_dotenv()

# Create the Flask app instance
app = create_app()

# Set up logging
logger = configure_logger()

# Run the Flask app
if __name__ == '__main__':
    # Get Flask port from environment or default to 5001
    # flask_port = int(os.getenv('FLASK_PORT', 5001))
    app.run(debug=True)
