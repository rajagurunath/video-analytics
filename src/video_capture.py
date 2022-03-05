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

def im2json(im):
    """Convert a Numpy array to JSON string"""
    imdata = pickle.dumps(im)
    jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
    return jstr

def save_captured_frame(frame1,frame_num):
    print("a new scene: ", len(frame1),frame1,frame_num)
    # plt.imshow(frame1)
    # plt.savefig(f"images/change-{frame_num}")
    im2json(frame1)

    # plt.show()



def main():
    
    # cap = cv2.VideoCapture()
    cam = cv2.VideoCapture(0)
    # cap.open(sys.argv[1])
    manager = SceneManager()
    manager.add_detector(
        # ContentDetector(threshold=10)
        ThresholdDetector(threshold=12)
    )
    manager.detect_scenes(frame_source=cam,callback=save_captured_frame)

    
 
if __name__ == "__main__":
    main()