"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

## ROUTES ##

@app.route("/")
def home():
    """Redirects to users"""

    return redirect("/users")


@app.route("/users")
def users():
    users_list = User.query.all()
    return render_template("users/index.html", users=users_list)
