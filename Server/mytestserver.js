const http = require('http');
const fs = require('fs');
const multer = require('multer');
const csv = require('csv-parser');
const express = require('express');
const Papa = require('papaparse');
const bodyParser = require('body-parser');




const app = express(); //create an express application 
const port = 8080;



//set up multer config for handling files
const storage = multer.memoryStorage();
const upload = multer({ 
    storage: storage,
    limits: {fileSize: 1024 * 1024 * 5},
});

// Serve statc files from 'public' directory
app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended: true}));

////////////////////////////////////////////////////////////


//start server
app.listen(port, () => {
	console.log("Server Started!");

});

//Rout for Home page 

app.get('/', (req, res) => {
	fs.readFile('./index.html', null, function(error, data) {
		if(error)
		{
			res.writeHead(404);
			res.write('File not Found');
		
		}
		else
		{
			res.writeHead(200, {'Content-type': 'text/html'});
			res.write(data);

		}
		res.end();
	});
});

app.post("/upload", upload.single('csvFile'), (req, res) => {
	if (!req.file) {
	  return res.status(400).send('No file uploaded');
	}

	if (!req.file.buffer) {
        return res.status(400).send('File buffer is empty');
    }

	//check to see if csv file was uploaded 
	if(req.file.mimetype !== 'text/csv') {
		return res.status(400).send('Invalid File format');
	}
	
	console.log("here!");
	console.log(__dirname);
	
	var stuff = req.file["buffer"];
	console.log(stuff.toString());
	res.send(stuff.toString());
	
	

  });




	
	