# Fill in this file with the code to create a new room from the Webex Teams exercise
from email import header
from os import access
import requests

access_token = "ZjM3OTJhNGItNDkyMS00NWE0LWIzYmMtZDkwMDFkMmVjODkyMWJjZTk1ZWQtMmI5_P0A1_4a252141-f787-4173-a4c9-bde69c553a24"
url = "https://webexapis.com/v1/rooms/"

headers = {
    "Authorization": f'Bearer {access_token}',
    "Content-Type": "application/json"
}

params = {
    "title": "Devnet Associate Traning!"
}

res = requests.post(url, headers=headers, json=params)

print(res.json())