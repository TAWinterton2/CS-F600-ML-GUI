# CS-F600-ML-GUI
Repositroy for CSf600 Project 

# Benchmark Testing
## Python Flask
The benchmark testing follows the [Python Flask Quickstart](https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application) guide to build a simple server.
### Prerequisites
#### Python
[Python](https://www.python.org/downloads/) is required to run this project. This project was built utilizing Python 3.11.

#### Creating a Virtual Environment
It is recommended that users create a [Python Virtual Environment](https://docs.python.org/3/library/venv.html) to run this project. The link for installing Python Flask also contains instructions for setting up a virtual environment in Python.

#### Installing Python Flask
[Install Python Flask](https://flask.palletsprojects.com/en/2.3.x/installation/) by utilizing the following command:
`pip install Flask`

This command will install Flask and the required dependencies.

### Running the Project
#### Activating the Project
The following command will start the project.
`flask run`

This will open up the app on `http://127.0.0.1:5000` (unless changed by the user).

If app.py is renamed to something else, the command to run the project will change to:
`flask --app name_of_python_file run`