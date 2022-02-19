from turtle import distance
import urllib.parse
import requests
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "DAGRA2xKHCNEX4IkpGMB37AU8bgPgKui"

while 1:
    print("type q or quit to exit")
    orig = input("starting location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    print(f"URL:\n{url}")
    json_data = requests.get(url).json()
    status = json_data["info"]["statuscode"]
    if status == 0:
        print(f"API status: {status} = A successful route call.\n")
        print("==============================================================")
        print(f'Directions from {orig} to {dest}')
        print(f'Trip duration  : {json_data["route"]["formattedTime"]}')
        print(f'Miles          : {json_data["route"]["distance"]}')
        print(f'Kilometer      : {json_data["route"]["distance"]*1.61:.2f}')
        print(f'Fuel Used (Ltr): {json_data["route"]["fuelUsed"]*3.78:.2f}')
        print(f'Fuel Used (Gal): {json_data["route"]["fuelUsed"]}')
        print("==============================================================")
        route = 1
        for step in json_data["route"]["legs"][0]["maneuvers"]:
            print(("route " + str(route)).center(62,"="))
            print(f'{step["narrative"]} : {step["distance"]*1.61:.2f} km')
            route += 1