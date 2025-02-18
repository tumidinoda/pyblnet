#!/usr/bin/env python

import paho.mqtt.client as mqtt
import json
import datetime
import time

from pyblnet.blnet_conn import BLNETDirect

# connect to MQTT-Broker
broker = '10.62.0.204'
mqqtClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqqtClient.connect(broker, 1883, 60)
print(" ")
print(str(datetime.datetime.now()) + ": Mqtt " + broker + " connected")
mqqtClient.loop_start()

# send discovery payload to broker
# template: <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
# see: https://www.home-assistant.io/integrations/mqtt#mqtt-discovery
topic = 'homeassistant/sensor/blnet/config'

# auto discovery device payload
device = {}
device['name'] = "blnet"
device['identifiers'] = "blnetSeyring"
device['configuration_url'] = "http://10.62.0.170"

# auto discovery payload
ap = {}
ap['name'] = 'Solar_Fuehler'
ap['unique_id'] = 'Solar_Fuehler'
ap['state_topic'] = 'tumi/heizung/sensor/Solar_Fuehler'
ap['unit_of_measurement'] = "°C"
ap['device'] = device

print("Topic: " + topic)
print("Payload: " + json.dumps(ap))
mqqtClient.publish(topic, json.dumps(ap), qos=1, retain=True)

mqqtClient.publish("tumi/heizung/sensor/Solar_Fuehler", 10, qos=1)

"""

mqqtClient.publish("tumi/heizung/sensors", json.dumps(mySensorsJson), qos=1, retain=True)
print(str(mySensorsJson))

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
print(str(mySensorsJson))
"""

time.sleep(5)
exit(0)
