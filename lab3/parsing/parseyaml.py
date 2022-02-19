import json 
import yaml
with open('myfile.yaml','r') as yaml_file:
    ouryaml = yaml.safe_load(yaml_file)
    print(ouryaml)
    print("The access token is {}".format(ouryaml['access_token']))
    print("\n\n---")
    print(json.dumps(ouryaml, indent=4))
