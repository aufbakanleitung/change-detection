import hashlib
import json
from urllib.request import urlopen
import requests

# If the site has no constantly changing elements such as hashes or a time, then you can use below
def hash_site(url, unchanged_hash):
    hashable_response = urlopen(url).read()
    currentHash = hashlib.sha224(hashable_response).hexdigest()
    if currentHash == unchanged_hash:
        print("No changes detected")
        print(f"Current hash {currentHash}")
        return False
    else:
        print("Website changed. Notifying user")
        print(f"Current hash {currentHash} \n original hash: {unchanged_hash}")
        return True


def post_message_to_slack(text, webhook_url):
    slack_data = {'text': text}
    response = requests.post(
               webhook_url,
               data=json.dumps(slack_data),
               headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    else:
        print(f"Slack: {text}")
        return "Slack message send"


def lambda_handler(event, context):
    url = event['url']
    unchanged_hash = event['unchanged_hash']
    if hash_site(url, unchanged_hash):
        print(event['webhook_url'])
        post_message_to_slack("hvdveer.nl hash veranderd", event['webhook_url'])
        # boto3.client('sns').publish(PhoneNumber=event['phone'], Message=event['message'])
        return 'Change found!'
    else:
        return 'No changes detected'

test_event = {
  "url": "https://www.hvdveer.nl",
  "unchanged_hash": "b624597f6baf137d5416f5c75a4a4ab61097e58fdb73feea422fd836",
  "message": "My website hvdveer.nl changed",
  "phone": "+31642783886",
  "webhook_url": "https://hooks.slack.com/services/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"
}