from flask import Flask
from .sentiment.routes import sentiment_bp
from .utils.config import Config
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')

    return app
