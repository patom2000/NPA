from http import client
import time
import paramiko
from dotenv import dotenv_values
import ast

config = dotenv_values(".env")
routers = ast.literal_eval(config["ROUTER"])
ip_list = list(routers.values())
ip_list.extend(["172.31.101.2", "172.31.101.3"])

user = config["USERNAME"]
password = config["PASSWORD"]

for ip in ip_list:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=user, look_for_keys=True)
    print(f"Connecting to {ip}...")
    with client.invoke_shell() as ssh:
        ssh.send("sh ip int br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)
