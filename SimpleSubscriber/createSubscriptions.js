var request = require('request');

var asBaseURL = 'http://russet.ischool.berkeley.edu:8080';

// (0) Put your own Host/IP/Port here - this is where ASbase will push notifications
var callbackURL = 'http://10.10.91.251:9090';

var userName = 'BIDSuser';
var subscriptionID = 'BIDSsubscription';

var asBaseUsersURL = asBaseURL + '/users';
var asBaseSubscriptionsURL = asBaseUsersURL + '/' + userName + '/subscriptions';
var headers = { 'Content-Type': 'application/json' };

function createSubscriptions(handleEvent) {
	console.log('Registering with ASBase at ' + asBaseUsersURL + '...');
	
	// (1) First create a subscriber...
	createSimpleUser(handleEvent);
}

function createSimpleUser(handleEvent) {
	
	// (2) ...by sending a user description to ASBase that includes the callback address for AS that are published by AS
	var user = {
			userID: userName, 
			channels: [ { type: 'URL_Callback', data: callbackURL } ] 
		};
	
	console.log('Sending: ' + JSON.stringify(user));
	request.post( {	url: asBaseUsersURL, json: user, headers: headers }, function (error, response, body) { handleUserCreationResponse(error, response, body); });
}

function handleUserCreationResponse(error, response, body) {
	
	if (!error && (response.statusCode == 201 || response.statusCode == 409)) {
		// (3) And, if the creation of a subscriber was successful (i.e. status code 201) or the user already exists (i.e. status code 409), create a subscription...
		console.log('User registration successful! Subscribing to events...');
		
		// (4) ... by sending an AS Template that is associated to the subscriber. This subscription will be triggered whenever "Martin Smith" "post"s something
		var subscription = { 
				userID: userName, 
				subscriptionID: subscriptionID, 
				ASTemplate: { 
					'actor.displayName' : { '$in': [ 'Martin Smith' ] }
				}
			};
		
		// (5) ... and HTTP POSTing that to the user's subscription URL at ASBase
		request.post( {	url: asBaseSubscriptionsURL, json: subscription, headers: headers }, function (error, response, body) { handle(error, response, body); });
	} else {
		console.log('Error, HTTP Status Code: ' + response.statusCode);
		console.log('Response body: ' + JSON.stringify(body));		
	}
}

function handle(error, response, body) {

	// (6) Finally, handle the response to the subscription creation - this should have the response code '201'
	if (!error && response.statusCode == 201) {
		console.log('Subscription successfully created!')
		console.log('\tResponse code: ' + response.statusCode);
		console.log('\t' + body);
	} else if (!error && response.statusCode == 409) {
		console.log('Subscription already exists!')
		console.log('\tResponse code: ' + response.statusCode);
		console.log('\t' + body);
	} else {
		console.log(error);
	}
}

module.exports = createSubscriptions;
