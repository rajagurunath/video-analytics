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
topic = "producer_tracker"
# generate client ID with pub prefix randomly
client_id = f'device-tracker'

# username = 'emqx'
# password = 'public'
username ='admin'
password = 'password'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
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
        print(data)
        # print(type(data))
        # # open("test.txt","w").write(data)
        # im,frame_num, producer_id = json2im(data)
        # plt.imshow(im)
        # plt.savefig(f"images/consumer/{client_id}-{producer_id}-{frame_num}.png")
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()