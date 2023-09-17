# https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
from flask import Flask, render_template
from markupsafe import escape

# Name of the module initializing / running the program
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

# Route can also be used to bind a function to a URL.
# If a user wishes to view this webpage at this url, they will see this text.
@app.route("/hello")
def hello():
    return "Hello, World"

# If the user is providing text input, it needs to be escaped to prevent injection attacks.
# "render_template" allows Jinja2 to load html for webpages.
@app.route("/<name>")
def hello_name(name=None):
    return render_template('name.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)
