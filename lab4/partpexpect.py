import pexpect
import ast #to covert env string to dict
from dotenv import dotenv_values

config = dotenv_values(".env")
routers = ast.literal_eval(config["ROUTER"])
ip_list = [i for i in routers.values()]
# telnet_login(config.USER, )

class Telnet:
    def __init__(self, ip, username, password):
        self.child = pexpect.spawn(f'telnet {ip}') #Note spawn ใช้ได้แค่นอก window https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows
        self.child.expect('Username', timeout=120)
        self.child.sendline(username)
        self.child.expect("Password")
        self.child.sendline(password)

    def run(self, expect, command):
        self.child.expect(expect)
        self.child.sendline(command)
        return self

    def get_before(self, expect):
        self.child.expect(expect)
        return self.child.before

    def close(self):
        self.child.close()

def config_loopback(ip, username, password, ip_loopback):
    """telnet and login to router"""
    telnet = Telnet(ip, username, password)
    telnet.run('#', 'conf t')
    telnet.run('#', 'int loopback 0')
    telnet.run('#', f'ip address {ip_loopback} 255.255.255.255')
    telnet.run('#', 'end')
    telnet.run('#', 'wr')
    print(telnet.get_before('#').decode('UTF-8'))
    telnet.close()

for ip in ip_list:
    iplb = 1
    iplb32 = str(iplb)+("."+str(iplb))*3
    config_loopback(ip, config["USERNAME"], config["PASSWORD"], iplb32)
    iplb += 1
