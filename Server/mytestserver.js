const fs = require('fs');
const multer = require('multer');
const express = require('express');
const Papa = require('papaparse');
const bodyParser = require('body-parser');

const app = express(); 
const port = 8080;

const storage = multer.memoryStorage();
const upload = multer({ 
    storage: storage,
    limits: {fileSize: 1024 * 1024 * 5},
});

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

app.listen(port, () => {
	console.log("Server Started!");
});

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

app.post("/upload", upload.single('csvFile'), (req, res) => {
	if (!req.file) return res.status(400).send('No file uploaded');
	if (!req.file.buffer) return res.status(400).send('File buffer is empty');
	if(req.file.mimetype !== 'text/csv') return res.status(400).send('Invalid File format');
	
    const csvBuffer = req.file.buffer.toString();
    
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
