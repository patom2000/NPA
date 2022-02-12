from netmiko import ConnectHandler
import ast
import re
from dotenv import dotenv_values

config = dotenv_values(".env")
routers = ast.literal_eval(config["ROUTER"])
device_list = []
for router_name in routers:
    device_list.append((router_name, {
        "device_type": "cisco_ios",
        "ip": routers[router_name],
        "username": config["USERNAME"],
        "password": config["PASSWORD"]
    }))
 
def output_text_to_list(text):
    return text.strip().split("\n")

def get_desc_from_cdp(cdp_result, device_name):
    data = output_text_to_list(cdp_result)
    interface_description = dict()
    for line in data:
        port_device_name, int_prefix, int_num, port_prefix, port_num = re.search(r"(\w\d)+\.npa\.com\s+(\w)\w+ (\d\/\d+)\s+\d+\s+[\w ]+\s+(\w)\w+ (\d\/\d+)", line).groups()
        if device_name == port_device_name:
            interface_description[f"{int_prefix}{int_num}"] = "Connect to WAN"
        else:
            interface_description[f"{int_prefix}{int_num}"] = f"Connect to {port_prefix}{port_num} of {port_device_name.upper()}"
    return interface_description

def config_description(device_name, device):
    with ConnectHandler(**device) as ssh:
        cdp_result = ssh.send_command("show cdp nei | include npa.com")
        connection_desc_list = get_desc_from_cdp(cdp_result, device_name)
        interface_result = ssh.send_command("show ip int br | include Gigabit")
        interface_list = output_text_to_list(interface_result)
        ssh.config_mode()
        for interface_line in interface_list:
            int_prefix, int_num = re.search(r"(\w)\w+(\d\/\d+)\s+", interface_line).groups()
            interface_name = int_prefix + int_num
            try:
                interface_desc = connection_desc_list[interface_name]
                ssh.send_command(f"int {interface_name}", expect_string=r"\#")
                ssh.send_command(f"description {interface_desc}", expect_string=r"\#")
            except KeyError:
                ssh.send_command(f"int {interface_name}", expect_string=r"\#")
                ssh.send_command(f"description Not Use", expect_string=r"\#")
        ssh.save_config()

for device_name, device in device_list:
    config_description(device_name, device)
