import RPi.GPIO as gpio


gpio.setmode(gpio.BCM)
dc_ENA = 25
dc_IN1 = 24
dc_IN2 = 23
gpio.setup(dc_ENA,gpio.OUT)
gpio.setup(dc_IN1,gpio.OUT)
gpio.setup(dc_IN2,gpio.OUT)
gpio.cleanup()
