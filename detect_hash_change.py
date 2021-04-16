import hashlib
from urllib.request import urlopen
import boto3


# If the site has no constantly changing elements such as hashes or a time, then you can use below
def hash_site(url, unchanged_hash, ):
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


def lambda_handler(event, context):
    url = event['url']
    unchanged_hash = event['unchanged_hash']

    if hash_site(url, unchanged_hash):
        boto3.client('sns').publish(PhoneNumber=event['phone'], Message=event['message'])
        return 'Change found!'
    else:
        return 'No changes detected'

test_event = {
    "url": "https://www.hvdveer.nl/",
    "unchanged_hash": "ee45ce4e2f39e24a1b68b827f6cd76e7766789d57dc81346064f549f",
    "message": "My website hvdveer.nl changed",
    "phone": "+31642783886"}

lambda_handler(test_event, 'context')