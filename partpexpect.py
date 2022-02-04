import pexpect
import ast #to covert env string to dict
from dotenv import dotenv_values

config = dotenv_values(".env")
routers = ast.literal_eval(config["ROUTER"])
ip_list = [i for i in routers.values()]
# telnet_login(config.USER, )

def config_loopback(ip, username, password, ip_loopback):
    """telnet and login to router"""
    child = pexpect.spawn(f'telnet {ip}') #Note spawn ใช้ได้แค่นอก window https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows
    child.expect('Username', timeout=120)
    child.sendline(username)
    child.expect("Password")
    child.sendline(password)
    child.expect('#')
    child.sendline('conf t')
    child.expect("(config)#")
    child.sendline('int loopback 0')
    child.expect("(config-if)#")
    child.sendline(f'ip address {ip_loopback}')
    child.sendline('end')
    child.expect("#")
    child.sendline('wr')
    child.close()

for ip in ip_list:
    iplb = 1
    iplb32 = str(iplb)+("."+str(iplb))*3
    config_loopback(ip, config["USERNAME"], config["PASSWORD"], iplb32)
    iplb += 1
