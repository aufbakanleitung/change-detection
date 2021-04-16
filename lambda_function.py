import boto3
import requests
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


sns = boto3.client('sns')

def lambda_handler(event, context):
    # url = "https://www.piccardthof.nl/huisjes-te-koop/"
    url = event['url']
    # check_line = "<h6>Er zijn op dit moment geen huisjes te koop</h6>"
    check_line = event['check_line']
    # original_element = "h6"
    original_element = event['original_element']
    # message = "Er staat een huisje te koop op het Piccardthof!"

    if check_website(url, check_line, original_element):
        sns.publish(PhoneNumber=event['phone'], Message=event['message'])
        return 'Change found!'
    else:
        return 'No changes detected'

event = {"url": "https://www.piccardthof.nl/huisjes-te-koop/",
         "check_line": "<h6>Er zijn op dit moment geen huisjes te koop</h6>",
         "original_element": "h6",
         "message": "Er staat een huisje te koop op het Piccardthof!",
         "phone": "+31642783886"}

# lambda_handler(event, "context")

# If the site has no constantly changing elements such as hashes or a time, then you can use below
# def hash_site():
#     unchanged_hash = "bdfc55f654a0813aecb7edf31dabf0f97c699f076907034d760cbe45"
#     hashable_response = urlopen(URL).read()
#     currentHash = hashlib.sha224(hashable_response).hexdigest()
#     if currentHash == unchanged_hash:
#         print("No changes detected")
#     else:
#         print("Website changed. Notifying user")
#         print(f"Current hash {currentHash} \n original hash: {unchanged_hash}")
json = '{"url": "https://www.piccardthof.nl/huisjes-te-koop/", "check_line": "<h6>Er zijn op dit moment geen huisjes te koop</h6>","original_element": "h6","message": "Er staat een huisje te koop op het Piccardthof!"}'