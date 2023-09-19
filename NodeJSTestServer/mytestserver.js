var http = require('http');
var fs = require('fs');
var querystring = require('querystring');
//var formidable = require('formidable'); // allows for file uploads 




let handleRequest = (req, res) => {

	if(req.method === 'POST') 
	{ // check for form submission 
		res.write('<p> file uploaded!');
		res.end();
		
		
	}
	else // Display htlmpage 
	{
		res.writeHead(200, {'Content-type': 'text/html'});
		
		fs.readFile('./testpage.html', null, function ( error, data ) 
		{
			if(error) 
			{
				res.writeHead(404);
				res.write("file not found");
			}
			else
			{
				res.write(data);
			}
			res.end();
		});
	}
};
		



const server = http.createServer(handleRequest);

server.listen(8080, () => {
	console.log('server started!');
});



	
	
