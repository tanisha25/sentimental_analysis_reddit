from flask import Flask
from flask_cors import CORS

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    from app.routes import sentiment_bp
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')

    return app