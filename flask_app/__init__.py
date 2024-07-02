from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "cf3e811af6be5434467e31f97ce7a5a6a43179712b5d8b76d71c539ae8562e82"
bcrypt = Bcrypt(app)
