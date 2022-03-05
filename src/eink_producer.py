import sys
import cv2
from numpy import save

from scenedetect.detectors import ThresholdDetector,ContentDetector
from scenedetect import SceneManager
import matplotlib.pyplot as plt
from paho.mqtt import client as mqtt_client
import base64
import pickle
import json
import uuid
import time
from asyncio import Queue
import cv2

broker = 'localhost'
port = 1883
topic = "/python/mqtt/images"
client_id = f'eink-producer-1'
topic_tracker = "device_tracker"
username ='admin'
password = 'password'
debug = True



def im2json(im,frame_num,client_id):
    """Convert a Numpy array to JSON string"""
    imdata = pickle.dumps(im)
    jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii'),"frame_num":frame_num,"client_id":client_id,"time":time.now()})
    return jstr



    # plt.show()
def change_detection(client):

    def face_detection(img,frame_num):
        face_cascade = cv2.CascadeClassifier('../models/haarcascade.xml')

        # img = cv2.imread('test.jpg')
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        if len(faces) >0:
            # publish if the face was detected !
            data= im2json(img,frame_num,client_id)
            
            result = client.publish(topic, data)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send msg to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            # Display the output
            # cv2.imshow('img', img)
            if debug:
                plt.imshow(img)
                plt.savefig(f"images/producer/ss-{frame_num}.png")
        # cv2.waitKey()


    def save_captured_frame(frame1,frame_num):
        #step 2 Face detection
        face_detection(frame1,frame_num)
        
       



    # cap = cv2.VideoCapture()
    cam = cv2.VideoCapture(0)
    # cap.open(sys.argv[1])
    manager = SceneManager()
    manager.add_detector(
        ContentDetector(threshold=10)
    )
    manager.detect_scenes(frame_source=cam,callback=save_captured_frame)


def connect_mqtt():
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



def publish(client):
    """
    change based trigger /publish
    ____________________      _________________________     ________________     ____________________________
   |camera/video capture| --> |change/ secene detection| -->| Face detection|--> |if face is detected publish|
   | ___________________|     |________________________|    |_______________|    |___________________________|
    
    """
    # step 1 change/scene detection
    change_detection(client)
    

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == "__main__":
    run()