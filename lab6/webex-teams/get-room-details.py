# Fill in this file with the code to get room details from the Webex Teams exercise
import requests

access_token = "ZjM3OTJhNGItNDkyMS00NWE0LWIzYmMtZDkwMDFkMmVjODkyMWJjZTk1ZWQtMmI5_P0A1_4a252141-f787-4173-a4c9-bde69c553a24"
room_id = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNTg4MjliOTAtOTE5Mi0xMWVjLWI3ZjMtODFlZDdmNGJiODhm"
url = f"https://webexapis.com/v1/rooms/{room_id}/meetingInfo"

headers = {
    "Authorization": f'Bearer {access_token}',
    "Content-Type": "application/json"
}

res = requests.get(url, headers=headers)

print(res.json())