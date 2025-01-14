from flask import Flask
from flask_cors import CORS
from app.routes import sentiment_bp

def create_app():
  app = Flask(__name__)

  # Enable CORS for all routes
  CORS(app)

  # Register Blueprints
  app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')

  return app