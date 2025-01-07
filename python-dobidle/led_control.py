import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴
import time                 # 시간관련 모듈을 불러옴
from threading import Thread
import threading

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정
GPIO.setup(26,GPIO.OUT)


class LED(threading.Thread):
    def __init__(self,client):
        super().__init__()
        self.client = client
    
    def run(self):
        max_time = time.time() + 10
        while True:
            GPIO.output(26,True)  # on
            time.sleep(0.5)
            GPIO.output(26,False)
            if time.time() > max_time:
                break
