from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from pprint import pprint
from flask import flash


class Recipe:
    _db = "recipes_db"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.user_id = data["user_id"]
        self.is_under_30 = data["is_under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the recipe form"""

        is_valid = True

        if len(form_data["name"].strip()) == 0:
            flash("No name entered, please enter name!")
            is_valid = False
        elif len(form_data["name"].strip()) < 2:
            flash("Name must be at least 2 characters!")
            is_valid = False
        if len(form_data["description"].strip()) == 0:
            flash("No description entered, please enter description!")
            is_valid = False
        elif len(form_data["description"].strip()) < 2:
            flash("Description must be at least 2 characters!")
            is_valid = False
        if len(form_data["instructions"].strip()) == 0:
            flash("No instructions entered, please enter instructions!")
            is_valid = False
        elif len(form_data["instructions"].strip()) < 2:
            flash("Instructions must be at least 2 characters!")
            is_valid = False

        if len(form_data["date_cooked"].strip()) == 0:
            flash("No date entered, please enter date!")
            is_valid = False

        if "is_under_30" not in form_data:
            is_valid = False
            flash("*********Please select a yes or no option********")

        elif form_data["is_under_30"] not in ["1", "0"]:
            is_valid = False
            flash("------Please select a yes or no option------")
        print("form_data", form_data)
        return is_valid

    @classmethod
    def retrieve_info(cls):
        """retrieve all recipes info from database"""
        query = """
        SELECT * FROM recipes 
        LEFT JOIN users ON recipes.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query)
        print("************")
        pprint(list_of_dicts)
        print("************")

        recipes = []
        for recipe_info in list_of_dicts:
            recipe = Recipe(recipe_info)
            user_data = {
                "id": recipe_info["users.id"],
                "first_name": recipe_info["first_name"],
                "last_name": recipe_info["last_name"],
                "email": recipe_info["email"],
                "password": recipe_info["password"],
                "created_at": recipe_info["users.created_at"],
                "updated_at": recipe_info["users.updated_at"],
            }
            user = User(user_data)
            recipe.user = user
            recipes.append(recipe)
        return recipes

    @classmethod
    def retrieve_by_id_with_user(cls, recipe_id):
        """Finds one recipe by id and related user"""

        query = """
        SELECT * FROM recipes 
        LEFT JOIN users ON recipes.user_id = users.id
        WHERE recipes.id = (%(recipe_id)s);
        """
        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query, data)
        pprint(list_of_dicts)
        recipe = Recipe(list_of_dicts[0])
        print(recipe.name)
        for each_dict in list_of_dicts:
            if each_dict["users.id"] != None:

                user_data = {
                    "id": each_dict["users.id"],
                    "first_name": each_dict["first_name"],
                    "last_name": each_dict["last_name"],
                    "email": each_dict["email"],
                    "password": each_dict["password"],
                    "created_at": each_dict["users.created_at"],
                    "updated_at": each_dict["users.updated_at"],
                }
                user = User(user_data)
                recipe.user = user
        return recipe

    @classmethod
    def create(cls, form_data):
        """insert a new recipe into the database"""
        query = """
        INSERT INTO recipes
        (name, description, instructions, date_cooked, user_id, is_under_30)
        Values
        (%(name)s,
        %(description)s,
        %(instructions)s,
        %(date_cooked)s,
        %(user_id)s,
        %(is_under_30)s)
        """

        recipe_id = connectToMySQL(Recipe._db).query_db(query, form_data)
        return recipe_id

    @classmethod
    def retrieve_info_id_with_user(cls, recipe_id):
        """retrieve one recipe info from database"""
        query = """
        SELECT * FROM recipes 
        Join users 
        ON recipes.user_id = users.id
        WHERE recipes.id = %(recipe_id)s;"""
        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query, data)
        pprint(list_of_dicts)
        recipe = Recipe(list_of_dicts[0])
        one_dict = list_of_dicts[0]
        user_data = {
            "id": one_dict["users.id"],
            "first_name": one_dict["first_name"],
            "last_name": one_dict["last_name"],
            "email": one_dict["email"],
            "password": one_dict["password"],
            "created_at": one_dict["users.created_at"],
            "updated_at": one_dict["users.updated_at"],
        }
        user = User(user_data)
        recipe.user = user
        return recipe

    @classmethod
    def update(cls, form_data):
        """Update a recipe by id"""

        query = """
        UPDATE recipes
        SET
        name = (%(name)s),
        description = (%(description)s),
        instructions = (%(instructions)s),
        date_cooked = (%(date_cooked)s),
        is_under_30 = (%(is_under_30)s)
        WHERE id = %(recipe_id)s;
        """
        connectToMySQL(Recipe._db).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(cls, recipe_id):
        """Deletes a user by id"""

        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        data = {"recipe_id": recipe_id}
        connectToMySQL(Recipe._db).query_db(query, data)
        return
