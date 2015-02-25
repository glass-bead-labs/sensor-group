import requests
import json

"""
Grabs issues from the sensor-group repository and posts them on ASbase
"""

issue_request_url = 'https://api.github.com/repos/bids/sensor-group/issues'
issue_response =  requests.get(url=issue_request_url).json()

repo_request_url = 'https://api.github.com/repos/bids/sensor-group'
repo_response = requests.get(url=repo_request_url).json()

count = 0
for issue in issue_response:
	body = {'published': issue['created_at'], 'verb': 'issue'}
	body['actor'] = {
		'url' : issue['user']['html_url'],
		'objectType' : issue['user']['type'],
		'id' : issue['user']['id'],
		'displayName' : issue['user']['login']
		}
	body['object'] = {
		'url' : issue['html_url'],
		'id' : issue['id']
	}
	body['target'] = {
		'url' : 'https://github.com/repos/BIDS/sensor-group',
		'objectType' : 'repository',
		'id': repo_response['id'],
		'displayName': repo_response['full_name']
	}
	converted = json.dumps(body)

	asbase_url = 'http://russet.ischool.berkeley.edu:8080/activities'
	requests.post(url=asbase_url, data=converted)