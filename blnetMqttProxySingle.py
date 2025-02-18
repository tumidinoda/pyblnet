#!/usr/bin/env python
#improved by ChatGPT :-)

import paho.mqtt.client as mqtt
import json
import datetime
import time
import logging
from pyblnet.blnet_conn import BLNETDirect

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# MQTT Configuration
BROKER_ADDRESS = "10.62.0.204"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
BASE_TOPIC = "tumi/heizung/sensor/"
FULL_TOPIC = "tumi/heizung/sensors"

# BLnet Configuration
BLNET_IP = "10.62.0.170"


# Initialize MQTT Client
def connect_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    try:
        client.connect(BROKER_ADDRESS, MQTT_PORT, MQTT_KEEPALIVE)
        logging.info(f"Connected to MQTT Broker: {BROKER_ADDRESS}")
        client.loop_start()
        return client
    except Exception as e:
        logging.error(f"Failed to connect to MQTT Broker: {e}")
        return None


# Connect to BLnet and retrieve data
def get_blnet_data():
    blnet = BLNETDirect(BLNET_IP)
    data = blnet.get_latest()

    if data[0] == "timeout" or data[1] == "timeout":
        logging.error("BLnet connection timeout")
        return None

    return data


# Publish Sensor Data to MQTT
def publish_sensor_data(client, data):
    if client is None or data is None:
        logging.error("MQTT Client or BLnet data is unavailable. Skipping publishing.")
        return

    mySgrp1, mySgrp2 = data[0]["analog"], data[1]["analog"]

    sensors = {
        "Solar_Fuehler": mySgrp1[1],
        "Solar_Vorlauf": mySgrp1[2],
        "Solar_Unten": mySgrp1[3],
        "Puffer_Unten": mySgrp1[3],
        "Puffer_Mitte": mySgrp1[4],
        "PufferOben": mySgrp1[5],
        "PufferTop": mySgrp1[6],
        "Ruecklauf": mySgrp1[7],
        "Kessel": mySgrp1[8],
        "Vorlauf": mySgrp1[9],
        "Vorlauf_HK": mySgrp1[10],
        "Vorlauf_FBH": mySgrp1[11],
        "Raum_HK": mySgrp1[12],
        "Raum_FBH": mySgrp1[13],
        "Aussen": mySgrp1[14],
        "Wasser_Mitte": mySgrp1[15],
        "Wasser_Oben": mySgrp1[16],
        "Soll_FBH": mySgrp2[2],
        "Soll_HK": mySgrp2[5],
        "Raum_WG": mySgrp2[12],
        "ZirkulationRL": mySgrp2[14],
    }

    # Publish all sensor data in a single JSON message
    # client.publish(FULL_TOPIC, json.dumps(sensors), qos=1, retain=True)
    # logging.info(f"Published all sensor data to {FULL_TOPIC}")

    # Publish each sensor separately, for Homeassistant
    for sensor, value in sensors.items():
        client.publish(BASE_TOPIC + sensor, value, qos=1, retain=True)
        logging.info(f"Published {sensor}: {value}")
        time.sleep(0.5)  # Slight delay to avoid flooding the broker


def main():
    logging.info("Blnet script started")

    mqtt_client = connect_mqtt()
    blnet_data = get_blnet_data()

    if blnet_data:
        publish_sensor_data(mqtt_client, blnet_data)

    logging.info("Publishing complete. Exiting in 5 seconds.")
    time.sleep(5)


if __name__ == "__main__":
    main()
