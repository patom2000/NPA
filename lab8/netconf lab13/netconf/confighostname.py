from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="10.0.15.111",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
#put config part of xml here
netconf_config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>R11</hostname>
  </native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_config)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())