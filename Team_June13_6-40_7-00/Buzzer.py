import RPi.GPIO as GPIO
import time


class Buzzer:
	def __init__(self,state):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.IN)
	
	def getState(self);
		pin = 22
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin, (GPIO.LOW if state == 0 else GPIO.HIGH))
	


