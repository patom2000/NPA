from netmikolab import *

def test_all():
    test_ip()
    test_subnet()
    test_status()
    test_desc()

def test_ip():
    assert get_ip(device, "G0/0") == "172.31.101.4"
    assert get_ip(device, "G0/3") == "unassigned"
    print("ip pass")

def test_subnet():
    assert get_subnet(device, "G0/0") == "/28"
    assert get_subnet(device, "G0/3") == "no subnet"
    print("subnet pass")

def test_desc():
    assert get_desc(device, "G0/0") == "Connect to G0/2 of S0"
    assert get_desc(device, "G0/1") == "Connect to G0/2 of S1"
    assert get_desc(device, "G0/2") == "Connect to G0/1 of R2"
    assert get_desc(device, "G0/3") == None
    print("decription pass")

def test_status():
    assert get_status(device, "G0/0") == "up"
    assert get_status(device, "G0/1") == "up"
    assert get_status(device, "G0/2") == "up"
    assert get_status(device, "G0/3") == "admin down"
    print("status pass")
