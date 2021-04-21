import requests
import json
from bs4 import BeautifulSoup

def check_website(url, check_line, original_element):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    current_line = str(soup.find(original_element))

    if current_line == check_line:
        print("No changes detected")
        print(f"Current website says: {check_line}")
        return False
    else:
        print("Website changed. Notifying user")
        print(f"Current website says: {check_line}")
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
        return "Slack message send"

def lambda_handler(event, context):
    url = event['url']
    check_line = event['check_line']
    original_element = event['original_element']

    if check_website(url, check_line, original_element):
        post_message_to_slack("huisje beschikbaar", event['webhook_url'])
        # boto3.client('sns').publish(PhoneNumber=event['phone'], Message=event['message'])
        return 'Change found!'
    else:
        return 'No changes detected'

event = {
    "url": "https://www.piccardthof.nl/huisjes-te-koop/",
    "check_line": "<h6>Er zijn op dit moment geen huisjes te koop</h6>",
    "original_element": "h6",
    "message": "Er staat een huisje te koop op het Piccardthof!",
    "phone": "+31642783886"}

# lambda_handler(event, "context")
