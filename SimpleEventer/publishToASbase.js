var asBaseURL = 'http://russet.ischool.berkeley.edu:8080';

function publishEvent(asData, asBaseURL) {
	
	// Load restler library for HTTP requests
	var rest = require('restler');
	
	// Log message
	console.log('Publishing: ' + JSON.stringify(asData));
	
	// Post AS to ASbase
	rest.post(asBaseURL, {

		// Specify data that should be sent to the broker - the ActivityStream
		data : JSON.stringify(asData),
		
		// Set correct HTTP header
		headers : { 'Content-Type': 'application/stream+json' }
	
	}).on('complete', function(data, response) {
		
		// Check that the correct response code was received
		if (response.statusCode === 200) {
			console.log('Great!');
		} else {
			console.log('Response Code:' + response.statusCode);
		}
	});
}

// Publish forever, with the specified timeout in milliseconds
function publishContinuously() {

	// Create ActivityStream (corresponds to the example in the ASBase API Doc)
	var asData = { 
			published : "2011-02-10T15:04:55Z",
			actor : {
			    url : "http://example.org/martin",
			    objectType : "person",
			    id : "tag:example.org,2011:martin",
			    displayName : "Martin Smith"
			  },
			  verb : "post",
			  object : {
			    url : "http://example.org/blog/2011/02/entry",
			    id : "tag:example.org,2011:abc123/xyz"
			  },
			  target : {
			    url : "http://example.org/blog/",
			    objectType : "blog",
			    id : "tag:example.org,2011:abc123",
			    displayName : "Martin's Blog"
			  }
		};

	publishEvent(asData, asBaseURL + '/activities');
	
	setTimeout(publishContinuously, timeout);
}

// Specify timeout and call function
timeout = 5000;
publishContinuously();
