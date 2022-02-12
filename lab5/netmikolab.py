from netmiko import ConfigInvalidException, ConnectHandler
import ast #to covert env string to dict
from dotenv import dotenv_values
import re

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

def send_ssh_command(device, command):
    with ConnectHandler(**device) as ssh:
        result = ssh.send_command(command)
        return result

def get_ip_list(device):
    return send_ssh_command(device, "sh ip int br")

def get_int_desc_list(device):
    return send_ssh_command(device, "sh int description")

def get_management_ip_route_list(device):
    return send_ssh_command(device, "sh ip route vrf management | include ^C")

def get_control_data_ip_route_list(device):
    return send_ssh_command(device, "sh ip route vrf control-Data | include ^C")
 
def output_text_to_list(text):
    return text.strip().split("\n")

def get_subnet(device, interface):
    data_control = get_control_data_ip_route_list(device)
    data_management = get_management_ip_route_list(device)
    data_list = output_text_to_list(data_control)
    data_list.extend(output_text_to_list(data_management))
    print(data_list)
    for line in data_list[1:]:
        try:
            subnet, int_prefix, int_num = re.search(r"C\s+\d+\.\d+\.\d+\.\d+\/(\d+)[\w ,]+ (\w)\w+(\d\/\d+)", line).groups()
            int_name = int_prefix + int_num
            if int_name == interface:
                return subnet
        except:
            pass
    return "no subnet"

def get_ip(device_info, interface):
    data = get_ip_list(device_info)
    data_list = output_text_to_list(data)
    for line in data_list[1:]:
        try:
            int_prefix, int_num, int_ip = re.search(r"(\w)\w+(\d\/\d+)\s+(\d+\.\d+\.\d+\.\d+|unassigned)", line).groups()
            int_name = int_prefix + int_num
            if int_name == interface:
                return int_ip
        except:
            pass

def get_desc(device_info, interface):
    data = get_int_desc_list(device_info)
    data_list = output_text_to_list(data)
    for line in data_list[1:]:
        try:
            int_prefix, int_num, int_desc = re.search(r"(\w)\w+(\d\/\d+)\s+(?:up|down|admin down)\s+(?:up|down|admin down)\s+(.+)\n?", line).groups()
            int_name = int_prefix + int_num
            if int_name == interface:
                return int_desc
        except:
            pass

def get_status(device_info, interface):
    data = get_int_desc_list(device_info)
    data_list = output_text_to_list(data)
    for line in data_list[1:]:
        try:
            int_prefix, int_num, int_status = re.search(r"(\w)\w+(\d\/\d+)\s+(up|down|admin down)\s+", line).groups()
            int_name = int_prefix + int_num
            if int_name == interface:
                return int_status
        except:
            pass

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
