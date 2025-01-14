import os
from dotenv import load_dotenv
from app import create_app
from app.logger import configure_logger

load_dotenv()

app = create_app()
configure_logger(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 