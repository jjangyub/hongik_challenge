import RPi.GPIO as gpio
import time
from threading import Thread
import threading

gpio.setmode(gpio.BCM)
dc_ENA = 25
dc_IN1 = 24
dc_IN2 = 23
gpio.setup(dc_ENA,gpio.OUT)
gpio.setup(dc_IN1,gpio.OUT)
gpio.setup(dc_IN2,gpio.OUT)

#speed
pwm = gpio.PWM(dc_ENA,50)

class DCmotor(threading.Thread):
    def __init__(self, client, status, event):
        super().__init__()
        self.client = client
        self.status = status
        self.event = event
        
    def setMotor(self):
        gpio.setmode(gpio.BCM)
        dc_ENA = 25
        dc_IN1 = 24
        dc_IN2 = 23
        gpio.setup(dc_ENA,gpio.OUT)
        gpio.setup(dc_IN1,gpio.OUT)
        gpio.setup(dc_IN2,gpio.OUT)
        
        # motor stop
        if self.event =='stop':
            print('dcmotor stop')
            pwm.ChangeDutyCycle(0)
            gpio.output(dc_ENA,False)
            
            self.client.publish('dcmotor','stop')
            time.sleep(1)
        # motor error
        elif self.event == 'error':
            print('dcmotor error')
            pwm.ChangeDutyCycle(0)
            gpio.output(dc_ENA,True)
            gpio.output(dc_IN1,gpio.LOW)
            gpio.output(dc_IN2,gpio.LOW)
            self.client.publish('dcmotor','error')
            time.sleep(1)
        # motor start
        else:
            pwm.ChangeDutyCycle(50)
            gpio.output(dc_ENA,True)
            gpio.output(dc_IN1,gpio.LOW)
            gpio.output(dc_IN2,gpio.HIGH)
            self.client.publish('dcmotor','start')
            
    def motor_run(self):
        gpio.output(dc_IN1,False)
        gpio.output(dc_IN2,True)
        gpio.output(dc_ENA,True)
        
    def motor_stop(self):
        gpio.output(dc_IN1,False)
        gpio.output(dc_IN2,False)
        gpio.output(dc_ENA,True)
        
    def run(self):
        try:
            print("dcmotor - run() called")
            self.setMotor()
        except RuntimeError as error:
            print("dc error")
            print(error.args[0])
        finally:
            print("dcmotor - run() finish")
            pass 
