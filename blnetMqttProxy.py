#!/usr/bin/env python
import time

import paho.mqtt.client as mqtt

from pyblnet import BLNETDirect


# connect to MQTT-Broker
mqqtClient = mqtt.Client()
mqqtClient.connect("10.0.0.36", 1883, 60)
mqqtClient.loop_start()

# connect to BLnet
ip = "10.0.0.170"
blnet = BLNETDirect(ip)

while True:
    myBLnet = blnet.get_latest()
    if myBLnet[0] == 'timeout' or myBLnet[1] == 'timeout':
        print("Timeout")
        break

    # frame1 = myBLnet[0]
    print(myBLnet)
    mqqtClient.publish("tumi/heizung", str(myBLnet))
    time.sleep(300)
