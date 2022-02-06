from http import client
import time
import paramiko
from dotenv import dotenv_values
import ast

config = dotenv_values(".env")
routers = ast.literal_eval(config["ROUTER"])
ip_list = ["172.31.101.4", "172.31.101.5","172.31.101.6"]

user = config["USERNAME"]
password = config["PASSWORD"]
commands = {
  "172.31.101.4": [
    "en",
    "conf t",
    "router ospf 1 vrf control-Data",
    "network 172.31.101.16 0.0.0.15 area 0",
    "network 172.31.101.32 0.0.0.15 area 0",
    "network 172.31.101.48 0.0.0.15 area 0",
    "network 1.1.1.1 255.255.255.255 area 0",
    "exit",
    "access-list 101 permit tcp 172.31.101.0 0.0.0.15 any eq telnet",
    "access-list 101 permit tcp 172.31.101.0 0.0.0.15 any eq 22",
    "access-list 101 permit tcp 10.253.190.0 0.0.0.255 any eq telnet",
    "access-list 101 permit tcp 10.253.190.0 0.0.0.255 any eq 22",
    "access-list 101 deny   tcp any any eq telnet",
    "access-list 101 deny   tcp any any eq 22",
    "access-list 101 permit tcp any any",
    "line vty 0 924",
    "access-class 101 in",
    "end",
    "wr",
  ],
  "172.31.101.5": [
    "en",
    "conf t",
    "router ospf 1 vrf control-Data",
    "network 172.31.101.16 0.0.0.15 area 0",
    "network 172.31.101.32 0.0.0.15 area 0",
    "network 172.31.101.48 0.0.0.15 area 0",
    "network 2.2.2.2 255.255.255.255 area 0",
    "exit",
    "access-list 101 permit tcp 172.31.101.0 0.0.0.15 any eq telnet",
    "access-list 101 permit tcp 172.31.101.0 0.0.0.15 any eq 22",
    "access-list 101 permit tcp 10.253.190.0 0.0.0.255 any eq telnet",
    "access-list 101 permit tcp 10.253.190.0 0.0.0.255 any eq 22",
    "access-list 101 deny   tcp any any eq telnet",
    "access-list 101 deny   tcp any any eq 22",
    "access-list 101 permit tcp any any",
    "line vty 0 924",
    "access-class 101 in",
    "end",
    "wr",
  ],
  "172.31.101.6": [
    "en", 
    "conf t",
    "ip route 0.0.0.0 0.0.0.0 192.168.122.1",
    "router ospf 1 vrf control-Data",
    "network 172.31.101.16 0.0.0.15 area 0",
    "network 172.31.101.32 0.0.0.15 area 0",
    "network 172.31.101.48 0.0.0.15 area 0",
    "network 3.3.3.3 255.255.255.255 area 0",
    "default-information originate",
    "exit",
    "int g0/1",
    "ip nat inside", 
    "int g0/2",
    "ip address dhcp",
    "ip nat outside",
    "exit",
    "access-list 1 permit any any",
    "ip nat inside source list 1 interface Gi0/2 vrf control-Data overload",
    "access-list 101 permit tcp 172.31.101.0 0.0.0.15 any eq telnet",
    "access-list 101 permit tcp 172.31.101.0 0.0.0.15 any eq 22",
    "access-list 101 permit tcp 10.253.190.0 0.0.0.255 any eq telnet",
    "access-list 101 permit tcp 10.253.190.0 0.0.0.255 any eq 22",
    "access-list 101 deny   tcp any any eq telnet",
    "access-list 101 deny   tcp any any eq 22",
    "access-list 101 permit tcp any any",
    "line vty 0 924",
    "access-class 101 in",
    "end",
    "wr",
  ]
}

for ip in ip_list:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=user, look_for_keys=True)
    print(f"Connecting to {ip}...")
    with client.invoke_shell() as ssh:
        for command in commands[ip]:
            print(command)
            ssh.send(f"{command}\n")
            time.sleep(1)
            print('***')
        # result = ssh.recv(1000).decode("ascii")
        # print(result)
