# Fill in this file with the rooms/spaces listing code from the Webex Teams exercise
import requests
import json

access_token = "ZjM3OTJhNGItNDkyMS00NWE0LWIzYmMtZDkwMDFkMmVjODkyMWJjZTk1ZWQtMmI5_P0A1_4a252141-f787-4173-a4c9-bde69c553a24"
url = "https://webexapis.com/v1/rooms/"

headers = {
    "Authorization": f'Bearer {access_token}',
    "Content-Type": "application/json"
}
params = {
    "max":'100'
}

res = requests.get(url, headers=headers, params=params)
print(json.dumps(res.json(), indent=4))
