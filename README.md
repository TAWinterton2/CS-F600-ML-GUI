# CS-F600-ML-GUI
Repository for CSf600 Project 

# Benchmark Testing
## NodeJS
The first benchmark test for this project follows [NodeJS](https://nodejs.org/en). The primary resources used by the team for learning are listed below.
- https://nodejs.org/en
- https://www.w3schools.com/nodejs/nodejs_intro.asp
- https://www.tutorialspoint.com/nodejs/index.htm
  
### Prerequisites
#### NodeJS
[Node JS](https://nodejs.org/en) is required to run this project. 
[Express JS](https://expressjs.com/) is required to run this Project.


#### Packages
- file system (fs) (npm install fs)
- multer (npm install multer)
- express js (npm install expressjs)
- Papa.Parser (npm install Papa-parse)
- Chat.js (include  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> in html file)
- artillery.io (sudo npm install -g artillery)
  


### Running the Project
  -download index.html and mytestserver.js
  -install all packages above
  -store both html and js file in same directory
  -open terminal into directory storing files
  -activate server using 'node mytestserver.js'
  -open webroswer and access website by entering "localhost:8080/"

  ### NodejS Stress Testing
  Stress testing was done using the artillery package [https://www.artillery.io/] using the quick testing function

  - Make sure to have artillery installed on machince
  - start nodejs server with node mytestserver.js
  - initialize artillery test using the following line in the terminal:
          artillery quick --count [insert virtual user count here] --num [insert http call count per user here]  http://localhost:8080
  


