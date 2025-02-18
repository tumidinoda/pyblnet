import json
import datetime
import time
import logging
import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Broker Configuration
BROKER_ADDRESS = '10.62.0.204'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
DISCOVERY_PREFIX = 'homeassistant/sensor/blnet/'


# Initialize MQTT Client
def connect_mqtt():
    client = mqtt.Client()
    try:
        client.connect(BROKER_ADDRESS, MQTT_PORT, MQTT_KEEPALIVE)
        logging.info(f"Connected to MQTT Broker: {BROKER_ADDRESS}")
        client.loop_start()
        return client
    except Exception as e:
        logging.error(f"Failed to connect to MQTT Broker: {e}")
        return None


# Define Device Information
DEVICE_INFO = {
    "name": "blnet",
    "identifiers": "blnetSeyring",
    "configuration_url": "http://10.62.0.170"
}


# Function to create and send auto-discovery payload
def create_auto_discovery(client, sensor):
    if client is None:
        logging.error(f"MQTT Client not initialized. Skipping {sensor}.")
        return

    payload = {
        "unit_of_measurement": "°C",
        "device": DEVICE_INFO,
        "name": sensor,
        "unique_id": sensor,
        "state_topic": f'tumi/heizung/sensor/{sensor}'
    }

    topic = f"{DISCOVERY_PREFIX}{sensor}/config"

    try:
        client.publish(topic, json.dumps(payload), qos=1, retain=True)
        logging.info(f"Discovery payload sent: {topic}")
        time.sleep(0.5)  # Slight delay to avoid flooding the broker
    except Exception as e:
        logging.error(f"Failed to send discovery payload for {sensor}: {e}")


# List of sensors
SENSORS = [
    'Solar_Fuehler', 'Solar_Vorlauf',
    'Solar_Unten', 'Puffer_Unten', 'Puffer_Mitte', 'PufferOben', 'PufferTop',
    'Ruecklauf', 'Kessel', 'Vorlauf', 'Vorlauf_HK', 'Vorlauf_FBH', 'Raum_HK',
    'Raum_FBH', 'Aussen', 'Wasser_Mitte', 'Wasser_Oben', 'Soll_FBH', 'Soll_HK',
    'Raum_WG', 'ZirkulationRL'
]

# Main Execution
if __name__ == "__main__":
    mqtt_client = connect_mqtt()

    for sensor in SENSORS:
        create_auto_discovery(mqtt_client, sensor)

    logging.info("Auto discovery finished")
