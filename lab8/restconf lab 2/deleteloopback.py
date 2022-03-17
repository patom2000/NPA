import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://10.0.15.111/restconf/data/ietf-interfaces:interfaces/interface=Loopback2"

headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
basicauth = ("admin", "cisco")


resp = requests.delete(api_url, auth=basicauth, headers=headers, verify=False)

if(resp.status_code >= 200 and resp.status_code <= 299):
    print("STATUS OK: {}".format(resp.status_code))
else:
    print('Error. Status Code: {} \nError message: {}'.format(resp.status_code,resp.json()))
