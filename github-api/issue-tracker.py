import requests
import json
from datetime import datetime
import time

GITHUB_USERNAME = 'BIDS'
GITHUB_REPO = 'sensor-group'


#Runs updateASBase every 10 seconds
def main():
	while True:
		updateASBase();
		time.sleep(10);


"""
Grabs issues from the GITHUB_REPO repository under GITHUB_USERNAME
and posts them on ASbase.
"""
def updateASBase():
	last_posted_timestamp = getLastPostTime('https://github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO)
	updated_issues = getUpdatedIssues(last_posted_timestamp)

	#Retrieve repository information for issues
	repo_request_url = 'https://api.github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO
	repo_response = requests.get(url=repo_request_url, auth=('dec2cca3656a040cdcf2ad2d4f73598ecd6d9fb8', '')).json()
	# repo_response = requests.get(repo_request_url).json()

	for issue in updated_issues:

		verb = getVerb(issue)

		body = {'published': issue['created_at'], 'verb': verb, 'timestamp' : str(datetime.now())}
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
			'url' : 'https://github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO,
			'objectType' : 'repository',
			'id': repo_response['id'],
			'displayName': repo_response['full_name']
		}
		converted = json.dumps(body)
		asbase_url = 'http://russet.ischool.berkeley.edu:8080/activities'
		requests.post(url=asbase_url, data=converted)

"""
Goes to ASBase and gets a timestamp of the last time this repo was updated.
"""
def getLastPostTime(repo_url):
	query = { "target.url" : { "$in" : [ repo_url ] } }
	converted_query = json.dumps(query)
	#print(converted_query)
	response = requests.post(url='http://russet.ischool.berkeley.edu:8080/query', data=converted_query).json()
	#print('response: ' + str(response))
	if response['totalItems'] == 0:
		return None
	else:
		#print(response['items'][0]['timestamp'])
		return response['items'][0]['timestamp']

"""
Goes to Github and grabs issues that have been updated since the timestamp provided.
"""
def getUpdatedIssues(timestamp):
	if not timestamp:
		issue_request_url = 'https://api.github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO + '/issues'
		return requests.get(url=issue_request_url, auth=('dec2cca3656a040cdcf2ad2d4f73598ecd6d9fb8', '')).json()
		# return requests.get(issue_request_url).json()
	else:
		issue_request_url = 'https://api.github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO + '/issues?since='+ timestamp + '&state=all'
		return requests.get(url=issue_request_url, auth=('dec2cca3656a040cdcf2ad2d4f73598ecd6d9fb8', '')).json()
		# return requests.get(issue_request_url).json()

"""
Sets the verb attribute of the ASBase record based on whether the issue was created, updated, or closed.
"""
def getVerb(issue):
	if issue['state'] == "closed":
		return "close"
	elif issue['updated_at'] != issue['created_at']:
		return "update"
	else:
		return "create"

main()
