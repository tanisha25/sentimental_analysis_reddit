from dotenv import load_dotenv

from app import create_app
import os

from app.utils.logger import configure_logger

load_dotenv()

app = create_app()
logger = configure_logger()


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'))