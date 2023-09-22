// Main node.js/express app file. This file handles running the JS server.
const http = require('http');
const { domainToASCII } = require('url');
const cors = require('cors');
var multer = require('multer');
const express = require("express");
var tr = require("./transfer")
var fs = require('fs');
const { transcode } = require('buffer');
const Papa = require('papaparse');

// Set up multer requirements
const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: {fileSize: 1024 * 1024 * 5}
});

// Create the app
const app = express();
const port = 5000;

// Allow use of static files in public directory
app.use(express.static('public'))
app.use(express.urlencoded({ extended: true }));

// Remove cors error
app.use(cors());

// Load the home/index page.
app.get('/', (req, res) => {
	fs.readFile('./index.html', null, function(error, data) {
		if(error) {
			res.writeHead(404);
			res.write('File not Found');
		} else {
			res.writeHead(200, {'Content-type': 'text/html'});
			res.write(data);
		}
		res.end();
	});
});


/*When a submit form request is made, this function will activate to:
   1. Create a .toString() buffer of the csv file.
   2. Send the file to Python for parsing.
   3. Perform the csv parsing.
   4. Generate the json needed for the graphing in index.js*/
app.post('/upload', upload.single('csvFile'), (req, res) => {
    // Ensure the file was uploaded
    if (!req.file) {
	    return res.status(400).send('No file uploaded');
	  }

    // Report if the file buffer is empty
	  if (!req.file.buffer) {
      return res.status(400).send('File buffer is empty');
    }

    //check to see if csv file was uploaded 
	  if(req.file.mimetype !== 'text/csv') {
		  return res.status(400).send('Invalid File format');
    }

    // Utilizes PapaParser to parsed the csv file into something useable for canvas.js
    const csvBuffer = req.file.buffer.toString();
    console.log("Python Response:" + tr.transfer(csvBuffer)); // To ensure we're getting a response from Python Flask for future computation
    Papa.parse(csvBuffer, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: function (results) {
        let labels = [];
        let datasets = [];
        let datasetLabels = results.meta.fields.filter(field => field !== 'Print-Runs');
        datasetLabels.forEach(label => datasets.push({ label: label, data: [] }));
        results.data.forEach(row => {
          labels.push(row['Print-Runs']);
          datasetLabels.forEach((label, index) => datasets[index].data.push(Number(row[label].replace(/,/g, ''))));
        });
        res.json({ labels, datasets });
      },
      error: function (error) {
        console.error("CSV parsing error:", error);
        res.status(500).send('Error parsing CSV');
      }
	});
});

// Tells the server what port to listen on.
app.listen(port, () => {
  console.log(`Server started...`);
}); 