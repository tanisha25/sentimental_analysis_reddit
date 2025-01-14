import os

from dotenv import load_dotenv
load_dotenv()

class Config:
    # Redis URL for caching
    REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')

    # PostgreSQL database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///sentiments.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

