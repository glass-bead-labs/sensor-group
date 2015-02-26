import requests
import json

GITHUB_USERNAME = 'bids'
GITHUB_REPO = 'sensor-group'


"""
Grabs issues from the GITHUB_REPO repository under GITHUB_USERNAME
and posts them on ASbase.
"""
def main():
	issue_request_url = 'https://api.github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO + '/issues'
	issue_response =  requests.get(url=issue_request_url, auth=('9faf448d82e9f0e96049311bdb9e8edcb29a91e2', '')).json()

	repo_request_url = 'https://api.github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO
	repo_response = requests.get(url=repo_request_url, auth=('9faf448d82e9f0e96049311bdb9e8edcb29a91e2', '')).json()

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
			'url' : 'https://github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO,
			'objectType' : 'repository',
			'id': repo_response['id'],
			'displayName': repo_response['full_name']
		}
		converted = json.dumps(body)

		#getLastPostTime('https://github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO)

		asbase_url = 'http://russet.ischool.berkeley.edu:8080/activities'
		#requests.post(url=asbase_url, data=converted)

	"""
	https://api.github.com/repos/bids/sensor-group/issues?since=2015-02-25
	"""


"""
Goes to ASBase and gets a timestamp of the last time this repo was updated.
"""
def getLastPostTime(repo_url):
	repo_url = 'https://github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO
	query = { "target.objectType" : {
	    "$in" : [ "repository" ] 
	    	}
	    }
	converted_query = json.dumps(query)
	print(converted_query)
	#response = requests.post(url='http://russet.ischool.berkeley.edu:8080/query', data=converted_query)
	timestamp = 
	print('response: ' + str(response.text))

"""
Goes to Github and grabs issues that have been updated since the timestamp provided.
"""
def getUpdatedIssues(timestamp):


main()
getLastPostTime('https://github.com/repos/' + GITHUB_USERNAME + '/' + GITHUB_REPO)