# https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
from flask import Flask
from markupsafe import escape

# Name of the module initializing / running the program
app = Flask(__name__)

# If a user wishes to view this webpage at this url, they will see this text.
@app.route("/")
def index():
    return "Index Page"

# Route can also be used to bind a function to a URL.
@app.route("/hello")
def hello():
    return "Hello, World"

# If the user is providing text input, it needs to be escaped to prevent injection attacks.
@app.route("/<name>")
def hello_name(name):
    return f'Hello, {escape(name)}!'
