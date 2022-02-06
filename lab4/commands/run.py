from re import template
import jinja2
import json
file_loader = jinja2.FileSystemLoader("commands")
env = jinja2.Environment(loader=file_loader)
 
f = open("data.json")
data = json.load(f)

#template = env.get_template("paramiko2.jinja")
#output = template.render(data=data)
print(data)