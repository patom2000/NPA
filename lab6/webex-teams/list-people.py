# Fill in this file with the authentication code from the Webex Teams exercise
from email import header
from os import access
import requests
import json

access_token = "ZjM3OTJhNGItNDkyMS00NWE0LWIzYmMtZDkwMDFkMmVjODkyMWJjZTk1ZWQtMmI5_P0A1_4a252141-f787-4173-a4c9-bde69c553a24"
url = "https://webexapis.com/v1/people/me"
person_id = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jNWU1NGY5ZC01YjA2LTQ5OTgtOWI0OC0wODQ5YzM5Zjc3OGU"
url2 = f'https://webexapis.com/v1/people/{person_id}'

headers = {
    "Authorization": f'Bearer {access_token}',
    "Content-Type": "application/json"
}
params = {
    "email": "62070111@it.kmitl.ac.th"
}

res = requests.get(url, headers=headers)
print(json.dumps(res.json(), indent=4))
