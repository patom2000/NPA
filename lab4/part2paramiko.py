from http import client
import time
import paramiko
from dotenv import dotenv_values
import ast

import jinja2
import json
file_loader = jinja2.FileSystemLoader("./commands")
env = jinja2.Environment(loader=file_loader)

data = json.load(open("./commands/data.json"))

template = env.get_template("paramiko2.jinja")

config = dotenv_values(".env")
routers = ast.literal_eval(config["ROUTER"])
ip_list = ["172.31.101.4", "172.31.101.5","172.31.101.6"]

user = config["USERNAME"]
password = config["PASSWORD"]

for ip in ip_list:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=user, look_for_keys=True)
    print(f"Connecting to {ip}...")
    with client.invoke_shell() as ssh:
        rendered = template.render(data=data[ip])
        commands = [cmd.strip() for cmd in rendered.split("\n") if cmd.strip()]
        for command in commands:
            ssh.send(f"{command}\n")
            time.sleep(1)
            result = ssh.recv(2000).decode("ascii")
            print(result)
            print('***')
