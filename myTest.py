#!/usr/bin/env python
import time
from pyblnet import BLNETDirect
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("10.0.0.11", 1883, 60)

client.loop_start()

ip='10.0.0.170'
blnet=BLNETDirect(ip)


while True:
    myWetter=blnet.get_latest()
    if myWetter[0]=='timout':
        print(myWetter[0])
        break
    frame1=myWetter[0]
    myWetterMQTT=str(myWetter)
    print(myWetterMQTT)
    client.publish("tumi/wetter", str(frame1))
    time.sleep(300)



