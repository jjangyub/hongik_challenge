import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
import threading

GPIO.setmode(GPIO.BCM)     

servo1_pin = 16                  
servo2_pin = 20                    
servo3_pin = 17

GPIO.setup(servo1_pin, GPIO.OUT)  
GPIO.setup(servo2_pin, GPIO.OUT)  
GPIO.setup(servo3_pin, GPIO.OUT)

servo1 = GPIO.PWM(servo1_pin, 50)  
servo2 = GPIO.PWM(servo2_pin, 50) 
servo3 = GPIO.PWM(servo3_pin, 50)

servo1.start(0)  
servo2.start(0)  
servo3.start(0)

servo_min_duty = 3               
servo_max_duty = 12             

class servo(threading.Thread):
    def __init__(self, client, servo_num):
        super().__init__()
        self.client = client
        self.servo_num = servo_num
        
    def set_servo_degree(self,servo_num, degree): 

        if degree > 180:
            degree = 180
        elif degree < 0:
            degree = 0

        duty = servo_min_duty+(degree*(servo_max_duty-servo_min_duty)/180.0)

        if servo_num == 1:
            GPIO.setup(servo1_pin,GPIO.OUT)
            servo1.ChangeDutyCycle(duty)
            sleep(0.3)
            GPIO.setup(servo1_pin,GPIO.IN)
            
        elif servo_num == 2:
            GPIO.setup(servo2_pin, GPIO.OUT) 
            servo2.ChangeDutyCycle(duty)
            sleep(0.3)
            GPIO.setup(servo2_pin, GPIO.IN)
            
        elif servo_num == 3:
            GPIO.setup(servo3_pin, GPIO.OUT)
            servo3.ChangeDutyCycle(duty)
            sleep(0.3)
            GPIO.setup(servo3_pin, GPIO.IN)
            
    def run(self):
        print('servo motor - Run() called')
        try:
            GPIO.setmode(GPIO.BCM) 
            if self.servo_num == '1':
                self.set_servo_degree(1,150)
                self.client.publish('servo','1/ok')
                sleep(3)
                self.set_servo_degree(1,90)
            
            elif self.servo_num=='2':
                self.set_servo_degree(2,130)
                self.client.publish('servo','2/ok')
                sleep(4)
                self.set_servo_degree(2,180)
            else:
                self.set_servo_degree(3,50)
                self.client.publish('servo','3/ok')
                sleep(6)
                self.set_servo_degree(3,0)
            self.client.publish('infra','end')
        
        except Exception as e:
            print('servo error')
            print(e.args[0])
            
        finally:                               
            print('servo motor - run() finish')