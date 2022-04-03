# python3.6

import random
import json
import base64
from PIL import Image
from io import BytesIO
from paho.mqtt import client as mqtt_client
import pickle
import matplotlib.pyplot as plt

broker = 'localhost'
port = 1883
topic = "/python/mqtt/monitoring"
client_id = f'device-monitor'
topic_tracker = "device_tracker"

# username = 'emqx'
# password = 'public'
username ='admin'
password = 'password'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.publish(topic_tracker,client_id)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = msg.payload.decode()
        print(type(data))
        print(data)
        

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()