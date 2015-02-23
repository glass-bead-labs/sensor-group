var createSubscriptions = require('./createSubscriptions.js');
var listen = require('./listen.js');

// Handle the published AS
function handleEvent(eventInJSON) {
	console.log("Processing event: " + JSON.stringify(eventInJSON));
}

createSubscriptions(handleEvent);
listen();