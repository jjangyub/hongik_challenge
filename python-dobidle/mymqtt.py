import paho.mqtt.client as mqtt
import paho.mqtt.publish as publisher
from threading import Thread

class MqttWorker:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def mymqtt_connect(self):
        try:
            print('broker connect start')
            self.client.connect('192.168.35.129',1883)
            self.client.loop_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print('end')
    def on_connect(self, client, userdata, flags, rc):
        print('connect...'+str(rc))
        if rc == 0:
            client.subscribe('web')
        else:
            print('connect failed')
    
    def on_message(self, client, userdata, message):
        try:
            myval = message.payload.decode('utf-8')
            print(message.topic+'----'+myval)
            if myval =='start':
                while True:
                    print('complete')
        except:
            pass
        finally:
            pass
if __name__=='__main__':
    mymqtt = MqttWorker()
    mymqtt.mymqtt_connect()
    