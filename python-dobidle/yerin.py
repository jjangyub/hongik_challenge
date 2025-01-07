from dcmotor import DCmotor
from infraredray_sensor import InfraredRay
from aicamera import camera
from servo_motor import servo
from led_control import LED

import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publisher
from threading import Thread
import threading
import pymysql

db = pymysql.connect(host='223.130.128.237', user='dobidb', password='ehqlemf^^7', db='site_db')


class MqttWorker:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.dcmotor = DCmotor(self.client,'start',None)
        self.dcmotor.run()
        self.infraredRay = InfraredRay(self.client)
        self.infraredRay.start()
        self.camera = None
        self.servo = None
        self.led = LED(self.client)
        
    def mymqtt_connect(self):
        try:
            print('broker connect start')
            self.client.connect('192.168.35.129',1883)
            mythreadobj = Thread(target=self.client.loop_forever)
            mythreadobj.start()
            
        except KeyboardInterrupt:
            pass
        finally:
            print('end')
            
    def on_connect(self, client, userdata, flags, rc):
        print('connect...'+str(rc))
        if rc == 0:
            client.subscribe('infra')
            client.subscribe('aimodel')
            client.subscribe('servo')
            client.subscribe('camera')
            
        else:
            print('connect failed')
    
    def on_message(self, client, userdata, message):
        msg = message.payload.decode('utf-8')
        try:
            if message.topic == 'infra':
                # no1 infra object access
                if msg == "access/1":
                    # dcmotor stop
                    self.dcmotor = DCmotor(self.client,"start","stop")
                    self.dcmotor.start()
                    self.camera = camera(self.client)
                    self.camera.start()
                    
                elif msg == "access/2":
                    # dcmotor stop
                    self.dcmotor = DCmotor(self.client,"start","stop")
                    self.dcmotor.start()
                    print('error')
                    self.led.start()
                    
                elif msg =='end':
                    self.infraredRay = InfraredRay(self.client)
                    self.infraredRay.start()
                    
            if message.topic == 'aimodel':
                if msg == 'donut':
                    self.servo = servo(self.client,'1')
                    self.servo.start()
                elif msg == 'hotdog':
                    self.servo = servo(self.client,'2')
                    self.servo.start()
                else:
                    self.servo = servo(self.client,'3')
                    self.servo.start()
                #db commit
                cur = db.cursor()
                cur.execute('UPDATE stock_stock SET product_count=product_count+1 WHERE product_name= %s',msg)
                db.commit()
            if message.topic == 'servo':
                self.dcmotor = DCmotor(self.client,'start',None)
                self.dcmotor.start()
                
                
        except:
            pass
        finally:
            pass


    
if __name__=='__main__':
    mymqtt = MqttWorker()
    mymqtt.mymqtt_connect()
