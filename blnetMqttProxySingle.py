#!/usr/bin/env python
import time

import paho.mqtt.client as mqtt

from pyblnet import BLNETDirect

# connect to MQTT-Broker
mqqtClient = mqtt.Client()
mqqtClient.connect("10.0.0.11", 1883, 60)
mqqtClient.loop_start()

# connect to BLnet
ip = '10.0.0.170'
blnet = BLNETDirect(ip)
myBLnet = blnet.get_latest()
print(myBLnet)
if myBLnet[0] == 'timout':
    exit(1)
mqqtClient.publish("tumi/heizung", str(myBLnet))
exit(0)

