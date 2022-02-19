import urllib.parse
import requests
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "DAGRA2xKHCNEX4IkpGMB37AU8bgPgKui"

while 1:
    orig = input("starting location: ")
    dest = input("Destination: ")
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    print(f"URL:\n{url}")
    json_data = requests.get(url).json()
    status = json_data["info"]["statuscode"]
    if status == 0:
        print(f"API status: {status} = A successful route call.\n")
