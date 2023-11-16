# CS-F600-ML-GUI
Repository for CSf600 Project 

## Front End Implementation
### Dependencies
- [Python](https://www.python.org/downloads/)
- [Python Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [Pandas](https://pandas.pydata.org/)
- [chart.js](https://www.chartjs.org/)
- [scikit-learn](https://scikit-learn.org/stable/install.html#installation-instructions)

<details>
<summary><h1>Benchmark Testing</h1></summary>

## Benchmark Requirements
The requirements for this benchmark testing are as follows:
1. The website must be able to display an HTML front page.
2. The user must be able to upload a .csv file to the website.
3. This csv file's contents should be displayed as a simple graph to the front end.
4. This csv file should not be stored on the server.


# 1. Python Flask
The first benchmark test for this project utilizes [Python Flask](https://flask.palletsprojects.com/en/2.3.x/). 
  
## Prerequisites
### Python
[Python](https://www.python.org/downloads/) is required to run this project. This project was built utilizing Python 3.11.


### Creating a Virtual Environment
It is recommended that users create a [Python Virtual Environment](https://docs.python.org/3/library/venv.html) to run this project. The link for installing Python Flask also contains instructions for setting up a virtual environment.


### Installing Dependencies
- [Python Flask](https://flask.palletsprojects.com/en/2.3.x/installation/) will install Flask and the required dependencies. It is installed via the command: `pip install Flask`
- [Pandas](https://pandas.pydata.org/): `pip install pandas`
- [Matplotlib](https://matplotlib.org/): `python -m pip install -U matplotlib`
- [locust](https://docs.locust.io/en/stable/what-is-locust.html): This is the library used for stress testing the server.


## Running the Project
### Activating the Project
On command line, navigate to the directory that contains `app.py`. The following command will start the project: 
`flask run`

This will open up the app on `http://127.0.0.1:5000` (unless changed by the user).

If app.py is renamed to something else, the command to run the project will change to:
`flask --app name_of_python_file run`

When running a file with this benchmark, please use `test.csv`. The code used to create the graph image does not support `dummy.csv`, as it is strictly an x-y line graph.

For running the `locust.py` simple stress test, open a terminal and navigate to the same directory as `locust.py`. While the server is running, type the following command: `locust -f locust.py --headless -u # -r # -t #m --html locust_report.html`
- -u: is the number of concurrent users
- -r: is the spawn rate of users per second
- -t: the duration of the test
- `--html locust_report`: specifies the stress test output file.


# 2. NodeJS
The first benchmark test for this project follows [NodeJS](https://nodejs.org/en). The primary resources used by the team for learning are listed below.
- https://nodejs.org/en
- https://www.w3schools.com/nodejs/nodejs_intro.asp
- https://www.tutorialspoint.com/nodejs/index.htm
  
## Prerequisites
### NodeJS
[Node JS](https://nodejs.org/en) is required to run this project. 
[Express JS](https://expressjs.com/) is required to run this Project.


### Packages
- file system (fs): `npm install fs`
- [multer](https://expressjs.com/en/resources/middleware/multer.html): `npm install multer`
- [Express JS](https://expressjs.com/):`npm install expressjs`
- [papaparser](https://www.papaparse.com/): `npm install papaparser`
- [chart.js](https://www.chartjs.org/): `npm install chart.js` (include  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> in html file)
- [artillery.io](https://www.npmjs.com/package/artillery) :`sudo npm install -g artillery`
  

## Running the Project
### Activating the Project
  - download index.html and mytestserver.js
  - install all packages above
  - store both html and js file in same directory
  - open terminal into directory storing files
  - activate server using 'node mytestserver.js'
  - open webroswer and access website by entering "localhost:8080/"

### NodejS Stress Testing
 Stress testing was done using the artillery package [https://www.artillery.io/] using the quick testing function

 - Make sure to have artillery installed on machince
 - start nodejs server with node mytestserver.js
 - initialize artillery test using the following line in the terminal:
`artillery quick --count [insert virtual user count here] --num [insert http call count per user here]  http://localhost:8080/`
  

## Benchmark Requirements
The requirements for this benchmark testing are as follows:
1. The website must be able to display an HTML front page.
2. The user must be able to upload a .csv file to the website.
3. This csv file's contents should be displayed as a simple graph to the front end.
4. This csv file should not be stored on the server.

# 3. NodeJS / Python
The final benchmark test attempts to implement a NodeJS map that can communicate with a Python Flask server on the side.


## Prerequisites
### Python Dependencies
This implementation does not contain any new Python dependencies compared to the above implementation of Python Flask.
- [Python](https://www.python.org/downloads/) 
- [Python Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/): `python -m pip install -U matplotlib`


### NodeJS Dependencies
Note: Ensure you are in the working directory (the directory that contains the files `flask_server.py` and `app.js`) before installing the NodeJS dependencies.
- [NodeJS and npm](https://nodejs.org/en/download)
- [Express](https://expressjs.com/en/starter/installing.html): `npm install express`
- [cors](https://expressjs.com/en/resources/middleware/cors.html): `npm install cors`
- [multer](https://expressjs.com/en/resources/middleware/multer.html): `npm install multer`
- [papaparser](https://www.papaparse.com/): `npm install papaparser`
- [chart.js](https://www.chartjs.org/): `npm install chart.js`
- [request-promise](https://www.npmjs.com/package/request-promise): `npm install request-promise` DO NOTE: This library is deprecated, and the script using it will be changed to remove it!


## Running the Project
### Activating the Project
Open 2 separate terminals. In both terminals, navigate to the working directory where `flask_server.py` and `app.js` are located. This should be `/benchmarks/node_flask`.

Once there, install the NodeJS dependencies. These should store in the `node_modules` directory in the project. Ensure that the version of your packages that you have installed match the version found within `package.json`.

Once the additional dependencies have been installed, it is time to activate the servers. In one terminal, you will activate the flask server by calling: `flask run -p 8001` to have the server listen on port 8001. To activate the NodeJS server, call `node app` in the other terminal. This will allow you to see the webpage at `127.0.0.1:5000`. 

Do note that this implementation uses NodeJS to host the web server. When a file is uploaded, the buffered contents are sent to Python Flask at `127.0.0.1:8001/transfer` to simulate what might occur in the full program. The information is changed into a useable format and stored into a pandas data frame. This data frame is resolved in JSON format back to the NodeJS and is displayed in the console once the request is finished. NodeJS also parses the csv file to display the graph contents on the screen.
</details>


<details>  
<summary><h1>Running the Project</h1></summary>
<h2>Deployment Installation</h2>

For ease of installation, we recommend using [Anaconda](https://www.anaconda.com/download) for managing the packages for this project:
`conda create -n myenv`

Once the environment is created, download the following dependencies:
`conda install flask`
`conda install pandas`
`conda install scikit-learn`
`npm install chartjs`
>If using a remote Linux server, ensure that Anaconda is installed on your account. If it is not, be sure to use wget to get the latest version of Anaconda to install it before attempting to create an environment for this project.

Once the required dependencies are installed in the virtual environment, download or clone a copy of the this repository.
>If you choose to download a .zip file of this repository, you can use scp to transfer the file to the Linux server.

On command line (Windows Shell, Visual Studio, Terminal Emulator in Linux) navigate to `./CS-F600-ML-GUI/website`, where the `app.py` file is located. To run, use the following command: `flask run --host=0.0.0.0 --port=6002`.

<h2>Installation on Personal Machine</h2>
- Clone the repository `gh repo clone TAWinterton2/CS-F600-ML-GUI` in directory of your choice.
- On command line (Windows Shell, Visual Studio, Terminal Emulator in Linux) navigate to `./CS-F600-ML-GUI/website`, where the `app.py` file is located. 
- run the app by using the command: `flask run`
- This will open up the app on `http://127.0.0.1:5000` (unless changed by the user).
- If app.py is renamed to something else, the command to run the project will change to: `flask --app name_of_python_file run`
- To run the server in debug mode, use the command `flask run --debug`
