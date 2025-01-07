import RPi.GPIO as gpio
import time
import threading

gpio.setmode(gpio.BCM)

pin_line1 = 21
pin_line2 = 19

gpio.setup(pin_line1,gpio.IN)
gpio.setup(pin_line2,gpio.IN)

class InfraredRay(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client
    
    def run(self):
        try:
            print("InfraredRay - run() called")
            gpio.setmode(gpio.BCM)
            gpio.setup(pin_line1, gpio.IN)
            while True:
                status1 = gpio.input(pin_line1)
                status2 = gpio.input(pin_line2)
                print("no1, infraredray :", status1)
                print("no2, infraredray :", status2)
                #no1 infraredray sensor
                if status1 == 0:
                    # object detect
                    print("InfraredRay line 1 motion detect")
                    self.client.publish("infra", "1")
                    self.client.publish("infra", "access/1")
                    time.sleep(1)
                    self.client.publish("infra", "finish/1")
                    break
                
                #no2 infraredray sensor
                if status2 == 0:
                    # object detect
                    print("InfraredRay line 2 motion detect")
                    self.client.publish("infra", "2")
                    self.client.publish("infra", "access/2")
                    time.sleep(1)
                    self.client.publish("infra", "finish/2")
                    break
                    

        except RuntimeError as error:
            print("InfraredRay error")
            print(error.args[0])
        finally:
            print("InfraredRay - run() finish")
        
