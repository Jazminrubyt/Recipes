from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User


@app.get("/")
def index():
    """This route displays the login and regristration form"""
    return render_template("index.html")


@app.post("/users/register")
def register():
    """This route processes the register form"""

    # If form not valid redirect
    if not User.register_form_is_valid(request.form):
        return redirect("/")

    # check if user already exist
    potential_user = User.find_by_email(request.form["email"])

    #  if user  exist redirect
    if potential_user != None:
        flash("Email in use, Please log in", "register")
        return redirect("/")

    #  user does not exist , safe to create and hash password
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    user_id = User.register(user_data)

    # save user id in session
    session["user_id"] = user_id
    return redirect("/recipes")


@app.post("/users/login")
def login():
    """This route processes the login form"""

    #  if form is not valid redirect
    if not User.login_form_is_valid(request.form):
        return redirect("/")

    #  does user exist?
    potential_user = User.find_by_email(request.form["email"])

    # if user does not exist, redirect
    if potential_user == None:
        flash("Invalid credentials.", "login")
        return redirect("/")

    # user exists!
    user = potential_user

    # check password
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials.", "login")
        return redirect("/")

    # save  user id in session (log in)
    session["user_id"] = user.id
    return redirect("/recipes")


@app.get("/users/logout")
def logout():
    """This route clears session"""
    session.clear()
    return redirect("/")


@app.get("/users/dashboard")
def dashboard():
    """This route displays user dashboard"""
    if "user_id" not in session:
        flash("Make sure you are logged in to view this page")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])

    return render_template("dashboard.html", user=user)
