import telnetlib
import getpass
import time

host = b"172.31.101.4"
user = input("Enter username: ")
password = getpass.getpass()


class Cisco:
    def __init__(self, host, username, password):
        self.tn = telnetlib.Telnet(host, 23, 5)
        self.tn.read_until(b"Username:", 5)
        self.tn.write(username.encode("ascii")+b"\n")
        time.sleep(1)

        self.tn.read_until(b"Password:", 5)
        self.tn.write(password.encode("ascii")+b"\n")
        time.sleep(1)

    def run(self, expect, command):
        self.tn.read_until(expect, 5)
        self.tn.write(command)
        time.sleep(1)
        return self

    def read_very_eager(self):
        return self.tn.read_very_eager()

    def close(self):
        self.tn.close()

def config_ip():
    cisco = Cisco(host, user, password)
    cisco.run(b"#", b"conf t\n")
    cisco.run(b"#", b"int g0/1\n")
    cisco.run(b"#", b"ip address 172.31.101.17 255.255.255.240\n")
    cisco.run(b"#", b"end\n")
    cisco.run(b"#", b"wr\n")

    output = cisco.read_very_eager()
    print(output.decode("ascii"))
    cisco.close()

config_ip()
