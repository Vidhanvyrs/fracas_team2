from flask import render_template, flash, request, redirect, url_for, session
from flask_login import current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, SignUpForm, ButtonForm
from app.models import User

from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        session["username"] = user.username
        session["user_id"] = user.id
        return render_template("index.html", title="Home")
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.get_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        session["username"] = user.username
        session["user_id"] = user.id
        flash("Login successful")
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        session["username"] = user.username
        session["user_id"] = user.id
        flash("Registration succesful!")
        return redirect(url_for("index"))
    return render_template("signup.html", title="Sign Up", form=form)


def get_username(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        return user.username
    else:
        return None
