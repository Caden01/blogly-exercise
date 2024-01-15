"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)
with app.app_context():
    db.create_all()

## USER ROUTES ##

@app.route("/")
def home():
    """Redirects to users"""

    return redirect("/users")


@app.route("/users")
def users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("index.html", users=users)

@app.route("/users/new", methods=["GET"])
def create_form():
    """Creates a form that allows a new user to be created"""

    return render_template("form.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Retrieves form data to create new user"""

    new_user = User(
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        image_url = request.form["image_url"] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show information of specific user"""

    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show form that allows to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes an existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


## POST ROUTES ##

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show form that allows user to create a form"""

    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """Handles add new post form"""

    user = User.query.get_or_404(user_id)
    post = Post(title=request.form["title"],
                content=request.form["content"],
                user=user)
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show info of a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template("show-post.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Allow user to edit post"""

    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Update post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")