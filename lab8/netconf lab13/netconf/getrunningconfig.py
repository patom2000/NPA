from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="10.0.15.111",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

#get runnning config of device
ugly_netconf_reply = m.get_config(source="running") #as same as <running></running>
beautiful_netconf_reply = xml.dom.minidom.parseString(ugly_netconf_reply.xml).toprettyxml() #make xml easy to read 
print(beautiful_netconf_reply)
