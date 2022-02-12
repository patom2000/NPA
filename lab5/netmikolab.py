from netmiko import ConnectHandler
from pprint import pp, pprint

def send_ssh_command(device, command):
    with ConnectHandler(**device) as ssh:
        result = ssh.send_command(command, use_textfsm=True)
        return result

def get_ip_list(device):
    return send_ssh_command(device, "sh ip int br")

def get_int_desc_list(device):
    return send_ssh_command(device, "sh int description")

def get_management_ip_route_list(device):
    return send_ssh_command(device, "sh ip route vrf management")

def get_control_data_ip_route_list(device):
    return send_ssh_command(device, "sh ip route vrf control-Data")

def get_subnet(device, interface_name):
    data_list = get_control_data_ip_route_list(device)
    data_list.extend(get_management_ip_route_list(device))
    for route in data_list:
        if route["protocol"] == "C" and route["nexthop_if"][0]+route["nexthop_if"][-3:] == interface_name:
            return route["mask"]
    return "no subnet"

def get_ip(device_info, interface_name):
    data_list = get_ip_list(device_info)
    for interface in data_list:
        if interface["intf"][0]+interface["intf"][-3:] == interface_name:
            return interface["ipaddr"]

def get_desc(device_info, interface_name):
    data_list = get_int_desc_list(device_info)
    for interface in data_list:
        if interface["port"][0] + interface["port"][-3:] == interface_name:
            return interface["descrip"]

def get_status(device_info, interface_name):
    data_list = get_int_desc_list(device_info)
    for interface in data_list:
        if interface["port"][0] + interface["port"][-3:] == interface_name:
            return interface["status"]
