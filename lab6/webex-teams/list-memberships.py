# Fill in this file with the membership code from the Webex Teams exercise
import json
import requests

access_token = "ZjM3OTJhNGItNDkyMS00NWE0LWIzYmMtZDkwMDFkMmVjODkyMWJjZTk1ZWQtMmI5_P0A1_4a252141-f787-4173-a4c9-bde69c553a24"
room_id = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNTg4MjliOTAtOTE5Mi0xMWVjLWI3ZjMtODFlZDdmNGJiODhm"
url = "https://webexapis.com/v1/memberships"

headers = {
    "Authorization": f'Bearer {access_token}',
    "Content-Type": "application/json"
}

params = {'roomId':room_id}
res = requests.get(url, headers=headers, params=params)

print(json.dumps(res.json(), indent=4))