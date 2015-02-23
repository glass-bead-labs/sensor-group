// This is a simple HTTP server that listens for HTTP POST requests in port 9090
function listen(handlePostedEvent) {
	var http = require('http'),
    fs = require('fs'),
    express = require('express'),
    bodyParser = require('body-parser'),
    mysql = require('mysql'),
    ejs = require('ejs');
	
	port = 9090;
	
	var app = express();
	app.use(bodyParser.urlencoded({
	    extended: true
	}));
	
	app.use(bodyParser.json());
		
	app.post("/", function(req, res) {
		console.log("Processing event: " + JSON.stringify(req.body));
		res.send("Thanks!");
	});

	app.listen(port);
	console.log('Listening...');
}

module.exports = listen;