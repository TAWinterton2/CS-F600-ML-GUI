# CS-F600-ML-GUI
Repository for CSf600 Project 

# Benchmark Testing
## Python Flask
The first benchmark test for this project follows [Python Flask](https://flask.palletsprojects.com/en/2.3.x/). The primary resources used by the team for learning are listed below.
- [Python Flask Quickstart](https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application)
- [Pythonistaplanet.com](https://pythonistaplanet.com/flask/)
- [Flask Calculator](https://medium.com/@alanbanks229/part-2-of-2-introduction-to-python-flask-29b58adbabaf)
  
### Prerequisites
#### Python
[Python](https://www.python.org/downloads/) is required to run this project. This project was built utilizing Python 3.11.

#### Creating a Virtual Environment
It is recommended that users create a [Python Virtual Environment](https://docs.python.org/3/library/venv.html) to run this project. The link for installing Python Flask also contains instructions for setting up a virtual environment in Python.

#### Installing Dependencies
- [Python Flask](https://flask.palletsprojects.com/en/2.3.x/installation/) will install Flask and the required dependencies. It is installed via the command: `pip install Flask`
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) will be required to use the SQLite database for this project. It is installed via the command: `pip install Flask-SQLAlchemy`

### Running the Project
#### Activating the Project
The following command will start the project: 
`flask run`

This will open up the app on `http://127.0.0.1:5000` (unless changed by the user).

If app.py is renamed to something else, the command to run the project will change to:
`flask --app name_of_python_file run`

#### Navigation
There are a few routes currently available to users:
- "/": The default index page, this simply displays text to the webpage that says "Index Page"
- "/hello": This page displays 'Hello, World' to the screen.
- "/<name>": This pages displays 'Hello, <name>' to the screen. Its main purpose is to practice HTML escaping.
- "/hello/": This page displays 'Hello, World' as <h1> instead of simple html text.
- "/hello/<name>": This page displays 'Hello, "<name>"' on the page as <h1>.
- "/calculator/": This page functions as a simple calculator. It operates as a FORM and will POST the solution (and any generated error messages) to the page "/calculator_result/"
- "/calculator_result/": URL for the POST request of the given calculator operations.

### To Do
- [ ] Index Page:   Add links to the various viable URL pages on webpage.
- [ ] Index Page:   Add description for website.
- [ ] db.py:        Test creating and using a SQLite database.