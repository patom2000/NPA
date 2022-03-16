from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="10.0.15.111",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

#write filter tag in here
netconf_filter = """
<filter>
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
"""

netconf_reply = m.get_config(source="running", filter=netconf_filter)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
