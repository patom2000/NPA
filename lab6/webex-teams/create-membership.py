# Fill in this file with the code to create a room membership from the Webex Teams exercise
import json
import requests

access_token = "ZjM3OTJhNGItNDkyMS00NWE0LWIzYmMtZDkwMDFkMmVjODkyMWJjZTk1ZWQtMmI5_P0A1_4a252141-f787-4173-a4c9-bde69c553a24"
room_id = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNTg4MjliOTAtOTE5Mi0xMWVjLWI3ZjMtODFlZDdmNGJiODhm"
url = "https://webexapis.com/v1/memberships"
person_email = "62070184@it.kmitl.ac.th"
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {'roomId': room_id, 'personEmail': person_email}
res = requests.post(url, headers=headers, json=params)
print(res.json())
