from flask import app
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def init_db(app):
    """ Initialize the database with the Flask app """
    db.init_app(app)

def create_tables():
    """ Create all tables in the database (if not exists) """
    with app.app_context():
        db.create_all()
