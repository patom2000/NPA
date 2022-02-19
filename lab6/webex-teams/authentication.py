# Fill in this file with the authentication code from the Webex Teams exercise
from email import header
from os import access
import requests
import json

access_token = "ZjM3OTJhNGItNDkyMS00NWE0LWIzYmMtZDkwMDFkMmVjODkyMWJjZTk1ZWQtMmI5_P0A1_4a252141-f787-4173-a4c9-bde69c553a24"
url = "https://webexapis.com/v1/people/me"

header = {
    "Authorization": f'Bearer {access_token}'
}

res = requests.get(url, headers=header)

print(json.dumps(res.json(), indent=4))