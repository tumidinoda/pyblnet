#!/usr/bin/env python

import paho.mqtt.client as mqtt
import json
import datetime
import time

from pyblnet.blnet_conn import BLNETDirect

# connect to MQTT-Broker
print(" ")
print(str(datetime.datetime.now()) + ": Blnet started")
mqqtClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqqtClient.connect("10.62.0.204", 1883, 60)
mqqtClient.loop_start()

# connect to BLnet
ip = "10.62.0.170"
blnet = BLNETDirect(ip)
myBLnet = blnet.get_latest()
# print(myBLnet)
if myBLnet[0] == 'timeout' or myBLnet[1] == 'timeout':
    print(str(datetime.datetime.now()) + ": Timeout")
    exit(1)
# mqqtClient.publish("tumi/heizung/raw", str(myBLnet)) */

mySgrp1 = myBLnet[0]['analog']
mySgrp2 = myBLnet[1]['analog']
# mySgrp1=mySgrp1['analog']

mySensorsJson = {}
mySensorsJson["Solar_Fuehler"] = mySgrp1[1]
mySensorsJson["Solar_Vorlauf"] = mySgrp1[2]
mySensorsJson["Solar_Unten"] = mySgrp1[3]
mySensorsJson["Puffer_Unten"] = mySgrp1[3]
mySensorsJson["Puffer_Mitte"] = mySgrp1[4]
mySensorsJson["Puffer_Oben"] = mySgrp1[5]
mySensorsJson["Puffer_Top"] = mySgrp1[6]
mySensorsJson["Ruecklauf"] = mySgrp1[7]
mySensorsJson["Kessel"] = mySgrp1[8]
mySensorsJson["Vorlauf"] = mySgrp1[9]
mySensorsJson["Vorlauf_HK"] = mySgrp1[10]
mySensorsJson["Vorlauf_FBH"] = mySgrp1[11]
mySensorsJson["Raum_HK"] = mySgrp1[12]
mySensorsJson["Raum_FBH"] = mySgrp1[13]
mySensorsJson["Aussen"] = mySgrp1[14]
mySensorsJson["Wasser_Mitte"] = mySgrp1[15]
mySensorsJson["Wasser_Oben"] = mySgrp1[16]

mySensorsJson["Soll_FBH"] = mySgrp2[2]
mySensorsJson["Soll_HK"] = mySgrp2[5]
mySensorsJson["Raum_WG"] = mySgrp2[12]
mySensorsJson["Zirkulation_RL"] = mySgrp2[14]

mqqtClient.publish("tumi/heizung/sensors", json.dumps(mySensorsJson), qos=1, retain=True)

# base topic
bt = "tumi/heizung/sensor/"
mqqtClient.publish(bt + "Solar_Fuehler", mySgrp1[1], qos=1, retain=True)
mqqtClient.publish(bt + "Solar_Vorlauf", mySgrp1[2], qos=1, retain=True)
mqqtClient.publish(bt + "Solar_Unten", mySgrp1[3], qos=1, retain=True)
mqqtClient.publish(bt + "Puffer_Unten", mySgrp1[3], qos=1, retain=True)
mqqtClient.publish(bt + "Puffer_Mitte", mySgrp1[4], qos=1, retain=True)
mqqtClient.publish(bt + "Puffer_Oben", mySgrp1[5], qos=1, retain=True)
mqqtClient.publish(bt + "Puffer_Top", mySgrp1[6], qos=1, retain=True)
mqqtClient.publish(bt + "Ruecklauf", mySgrp1[7], qos=1, retain=True)
mqqtClient.publish(bt + "Kessel", mySgrp1[8], qos=1, retain=True)
mqqtClient.publish(bt + "Vorlauf", mySgrp1[9], qos=1, retain=True)
mqqtClient.publish(bt + "Vorlauf_HK", mySgrp1[10], qos=1, retain=True)
mqqtClient.publish(bt + "Vorlauf_FBH", mySgrp1[11], qos=1, retain=True)
mqqtClient.publish(bt + "Raum_HK", mySgrp1[12], qos=1, retain=True)
mqqtClient.publish(bt + "Raum_FBH", mySgrp1[13], qos=1, retain=True)
mqqtClient.publish(bt + "Aussen", mySgrp1[14], qos=1, retain=True)
mqqtClient.publish(bt + "Wasser_Mitte", mySgrp1[15], qos=1, retain=True)
mqqtClient.publish(bt + "Wasser_Oben", mySgrp1[16], qos=1, retain=True)

mqqtClient.publish(bt + "Soll_FBH", mySgrp2[2], qos=1, retain=True)
mqqtClient.publish(bt + "Soll_HK", mySgrp2[5], qos=1, retain=True)
mqqtClient.publish(bt + "Raum_WG", mySgrp2[12], qos=1, retain=True)
mqqtClient.publish(bt + "Zirkulation_RL", mySgrp2[14], qos=1, retain=True)


print(str(mySensorsJson))
time.sleep(5)
exit(0)
