var http = require('http');

http.createServer(function (req, res) {
	res.writeHead(200, {'Content-type': 'text/html'});
	res.end('Hello, this is a test!');
}).listen(8080);
console.log("sever started!");

	
	