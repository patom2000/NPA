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

def get_result_from_interface(interface, result, interface_index):
    for line in result[1:]:
        words = line.split()
        if words[interface_index][0] == interface[0] and words[interface_index][-3:] == interface[1:]:
            return words

def get_subnet(device, interface):
    data_control = get_control_data_ip_route_list(device)
    data_management = get_management_ip_route_list(device)
    result_control = output_text_to_list(data_control)
    result_management = output_text_to_list(data_management)
    result_control_in_interface = get_result_from_interface(interface, result_control, -1)
    result_management_in_interface = get_result_from_interface(interface, result_management, -1)
    if result_control_in_interface != None:
        return result_control_in_interface[1][-2:]
    elif result_management_in_interface != None:
        return result_management_in_interface[1][-2:]
    else:
        return "no subnet"
    
def get_ip(device_info, interface):
    data = get_ip_list(device_info)
    data_list = output_text_to_list(data)
    for line in data_list[1:]:
        int_prefix, int_num, int_ip = re.search(r"(\w)\w+(\d\/\d+)\s+(\d+.\d+.\d+.\d+|unassigned)", line).groups()
        int_name = int_prefix + int_num
        if int_name == interface:
            return int_ip
            
def get_desc(device_info, interface):
    data = get_int_desc_list(device_info)
    results = output_text_to_list(data)
    result_line = get_result_from_interface(interface, results, 0)
    if result_line[1] == "up":
        return ' '.join(result_line[3:])
    elif result_line[1] == "admin":
        return ' '.join(result_line[4:])

def get_status(device_info, interface):
    data = get_int_desc_list(device_info)
    result = output_text_to_list(data)
    interface_status_line = get_result_from_interface(interface, result, 0)
    if interface_status_line[1] == "admin" and interface_status_line[2] == "down":
        return "admin down"
    return interface_status_line[1]

def get_desc_from_cdp(cdp_result, device_name):
    data = output_text_to_list(cdp_result)
    interface_description = dict()
    for line in data:
        words = line.split()
        if device_name == f"{words[0][:2].upper()}":
            interface_description[f"{words[1][0]}{words[2]}"] = "Connect to WAN"
        else:
            interface_description[f"{words[1][0]}{words[2]}"] = f"Connect to {words[6][0]}{words[7]} of {words[0][:2].upper()}"
    return interface_description

def config_description(device_name, device):
    with ConnectHandler(**device) as ssh:
        cdp_result = ssh.send_command("show cdp nei | include npa.com")
        connection_desc_list = get_desc_from_cdp(cdp_result, device_name)
        interface_result = ssh.send_command("show ip int br | include Gigabit")
        interface_list = output_text_to_list(interface_result)
        ssh.config_mode()
        for interface_line in interface_list:
            interface_info = interface_line.split()
            interface_name = interface_info[0][0]+interface_info[0][-3:]
            interface_status = interface_info[4]
            if len(interface_info) == 6 and interface_status == "administratively":
                interface_status = "administratively down"

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
