import json 
import yaml
with open('myfile.json', 'r') as json_file:
    ourjson = json.load(json_file)
    print("The access token is: {}".format(ourjson['access_token']))
    print("The token expire in {} seconds.".format(ourjson['expires_in']))

    print("\n\n---")
    print(yaml.dump(ourjson))
