from netmikolab import *
import json

test_file = open('test_data.json')
json_data = json.load(test_file)
test_file.close()

def get_netmiko_device_info(data):
    return {
        "device_type": data["device_type"],
        "ip": data["ip"],
        "username": data["username"],
        "password": data["password"]
    }

def test_ip():
    for device in json_data:
        for interface in device["interfaces"]:
            assert get_ip(get_netmiko_device_info(device), interface["name"]) == interface["ip"], f'IP of {interface["name"]} in {device["name"]} is incorrect'
    print("ip pass")

def test_subnet():
    for device in json_data:
        for interface in device["interfaces"]:
            assert get_subnet(get_netmiko_device_info(device), interface["name"]) == interface["subnet_mask"], f'Subnet of {interface["name"]} in {device["name"]} is incorrect'
    print("subnet pass")

def test_desc():
    for device in json_data:
        for interface in device["interfaces"]:
            assert get_desc(get_netmiko_device_info(device), interface["name"]) == interface["description"], f'Description of {interface["name"]} in {device["name"]} is incorrect'
    print("description pass")

def test_status():
    for device in json_data:
        for interface in device["interfaces"]:
            assert get_status(get_netmiko_device_info(device), interface["name"]) == interface["status"], f'Status of {interface["name"]} in {device["name"]} is incorrect'
    print("status pass")