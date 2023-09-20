const http = require('http');
const fs = require('fs');
const multer = require('multer');
const csv = require('csv-parser');
const express = require('express');


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

app.post("/upload", upload.single('csvFile'), (req, res) => {
	if (!req.file) {
	  return res.status(400).send('No file uploaded');
	}
	console.log("BING!");

  });
  



//Rout for Home page 

app.get('/', (req, res) => {
	fs.readFile('./testpage.html', null, function(error, data) {
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


//start server
app.listen(port, () => {
	console.log("Server Started!");

});



	
	