from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Renders the home page of the website, the first page that a user will land on when visiting the website."""
    return render_template('index.html')


@app.route("/linear")
def ml_form():
    """Renders the machine learning form for the linear regression model. This is done by pressing the button on the navigation bar."""
    return render_template('ml_form.html')

if __name__ == "__main__":
    app.run(debug=True)