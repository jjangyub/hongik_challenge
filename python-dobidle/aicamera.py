import cv2
from threading import Thread
import threading

class camera(threading.Thread):
    def __init__(self,client):
        super().__init__()
        self.client=client
        
    def run(self):
        # open camera
        cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
        
        # set dimensions
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        
        # take frame
        ret, frame = cap.read()
        # write frame to file
        cv2.imwrite('image.jpg', frame)
        print('take picture')
        self.client.publish("camera", "1")
        # release camera
        cap.release()