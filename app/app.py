import os
from dotenv import load_dotenv
from app import create_app
from app.utils.logger import configure_logger
import gunicorn

# Load environment variables
load_dotenv()

# Create the Flask app instance
app = create_app()

# Set up logging
logger = configure_logger()

# Check the environment and run the appropriate server
if __name__ == '__main__':
    # if os.getenv('FLASK_ENV') == 'development':
    #     # Development mode: Use Flask's built-in server
    #     app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
    # else:
    #     # Production mode: Use Gunicorn directly (configured in the command line or Gunicorn config file)
    #     # Run the app using Gunicorn, if in production environment
    #     # This is typically executed via the command line with gunicorn, e.g., `gunicorn app:app`
    #     gunicorn_options = {
    #         'bind': f"0.0.0.0:{os.getenv('PORT', 5000)}",  # Use Render's provided PORT environment variable
    #         'workers': 4,  # Number of workers for Gunicorn
    #     }
    #     # Gunicorn is typically started via the command line, but if you need to programmatically start it, you can use this:
    #     gunicorn.app.base.Application(app, options=gunicorn_options).run()
    app.run(debug=True)
