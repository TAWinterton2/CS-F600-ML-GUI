// This script handles a simple request to python flask and resolves the response.

var request = require('request-promise');

async function transfer(data) {
    console.log("Data being sent to Python:" + data);
    // Creates the options for the POST request to the Flask server.
    var options = {
        method: 'POST',
        uri: 'http://127.0.0.1:8001/transfer',
        body: data,
    };

    // Creates and returns a new Promise that will store the Python contents once the request is complete.
    return new Promise(function (resolve, reject)
    {
        request(options, function(error, response, body) 
        {
            if (!error)
                resolve(body);
            else
                reject(error);
        })
    });
}

// Exports the script to be used by app.js
exports.transfer = transfer;