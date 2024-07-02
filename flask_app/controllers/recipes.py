from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash


@app.route("/recipes")
def recipes():
    """This route displays all recipes"""
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipes = Recipe.retrieve_info()
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_recipe.html", recipes=recipes, user=user)


@app.get("/recipes/new")
def new_recipe():
    """This route displays new recipe"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("new_recipe.html", user=user)


@app.get("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    """This route displays a recipes info"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    recipe = Recipe.retrieve_by_id_with_user(recipe_id)
    user = User.find_by_user_id(session["user_id"])
    if recipe == None:
        return "No recipe information found"
    return render_template("recipe_details.html", recipe=recipe, user=user)


@app.post("/recipes/create")
def create_recipe():
    """The route that processes the create form"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    if not Recipe.form_is_valid(request.form):
        return redirect("/recipes/new")

    print("*******************************")
    print(request.form)
    recipe_id = Recipe.create(request.form)
    # print("New Recipe:" + str(recipe_id))#
    return redirect("/recipes")


@app.get("/recipes/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    """This route displays edit form"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipe = Recipe.retrieve_by_id_with_user(recipe_id)
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_recipe.html", recipe=recipe, user=user)


@app.post("/recipes/update")
def update_recipe():
    """This route processes the Edit form"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipe_id = request.form["recipe_id"]

    if not Recipe.form_is_valid(request.form):
        return redirect(f"/recipes/{recipe_id}/edit")

    Recipe.update(request.form)
    return redirect(f"/recipes/{recipe_id}")


@app.post("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    """Deletes a recipe"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    Recipe.delete_by_id(recipe_id)
    return redirect("/recipes")
