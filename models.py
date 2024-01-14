"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image_url = "https://img.freepik.com/free-vector/illustration-businessman_53876-5856.jpg?w=740&t=st=1705249885~exp=1705250485~hmac=35636232d0820634839c56ebd576dede968f2c0e5e951fb79f95c195aa08c881"

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=default_image_url)
    

def connect_db(app):
    db.app = app
    db.init_app(app)