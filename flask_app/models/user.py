from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    _db = "recipes_db"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def register_form_is_valid(form_data):
        """This method validates the registration form"""

        is_valid = True

        if len(form_data["first_name"].strip()) == 0:
            flash("Please Enter First Name.", "register")
            is_valid = False
        elif len(form_data["first_name"].strip()) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False

        if len(form_data["last_name"].strip()) == 0:
            flash("Please Enter Last Name.", "register")
            is_valid = False
        elif len(form_data["last_name"].strip()) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False

        if len(form_data["email"].strip()) == 0:
            flash("Please Enter email.", "register")
            is_valid = False

        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email Not Vaild", "register")
            is_valid = False

        if len(form_data["password"].strip()) == 0:
            flash("Please Enter password.", "register")
            is_valid = False

        elif len(form_data["password"].strip()) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False

        elif form_data["password"] != form_data["confirm_password"]:
            flash("passwords do not match", "register")
            is_valid = False

        return is_valid

    @staticmethod
    def login_form_is_valid(form_data):
        """This method validates the Login form"""

        is_valid = True

        if len(form_data["email"].strip()) == 0:
            flash("Please Enter email.", "login")
            is_valid = False

        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email Not Vaild", "login")
            is_valid = False

        if len(form_data["password"].strip()) == 0:
            flash("Please Enter password.", "login")
            is_valid = False

        elif len(form_data["password"].strip()) < 8:
            flash("Password must be at least 8 characters.", "login")
            is_valid = False

        return is_valid

    @classmethod
    def register(cls, user_data):
        """This method creates a new user in the DB"""

        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """

        user_id = connectToMySQL(User._db).query_db(query, user_data)
        return user_id

    @classmethod
    def find_by_email(cls, email):
        """This method finds a user by email"""

        query = """
        SELECT * FROM users WHERE email = %(email)s
        """
        data = {"email": email}
        list_of_dict = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dict) == 0:
            return None
        user = User(list_of_dict[0])
        return user

    @classmethod
    def find_by_user_id(cls, user_id):
        """This method finds a user by user_id"""

        query = """
        SELECT * FROM users WHERE id = %(user_id)s
        """
        data = {"user_id": user_id}
        list_of_dict = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dict) == 0:
            return None
        user = User(list_of_dict[0])
        return user
