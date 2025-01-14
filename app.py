import os
from dotenv import load_dotenv
from app import create_app
from app.logger import configure_logger

# Load environment variables
load_dotenv()



# Check the environment and run the appropriate server
if __name__ == '__main__':
    # Create the Flask app instance
    app = create_app()

    # Set up logging
    logger = configure_logger()
    port = int(os.getenv('PORT', 5000))  # Use the PORT from the environment, default to 5000 if not set
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
