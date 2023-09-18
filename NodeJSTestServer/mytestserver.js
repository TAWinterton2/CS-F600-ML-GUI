var http = require('http');
var fs = require('fs');
var querystring = require('querystring');





let handleRequest = (req, res) => {

	if(req.method === 'POST' && req.url === '/submit') 
	{ // check for form submission 
		let requestBody = '';
		
		req.on('data', (data) => {
			requestBody += data.toString();
		});
		
		req.on('end', () => {
			// Parse the form
			
			const formData = querystring.parse(requestBody);
			const feedback = formData.feedback;
			
			res.writeHead(200, {'Content-type': 'text/html' });
			res.write('<h1> Feedback Received!<h1>');
			res.write('<p> Thank you for the feedback!' + feedback + "</p>");
			
			
			res.end();
			
		
		
		}); 
		
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



	
	