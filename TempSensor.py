import os
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
import sys
from paho.mqtt.client import Client
import datetime
import sched, time
s = sched.scheduler(time.time, time.sleep)
 

#intialise the device
os.system ('sudo modprobe w1-gpio')
os.system ('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def run_periodically(start, end, interval, func):
    event_time = start
    while event_time < end:
        s.enterabs(event_time, 0, func, ())
        event_time += interval
    s.run()
    run_periodically(time()+5, time()+10, 1,read_temp_raw)


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.1)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        #print(temp_string)
        temp_c = float(temp_string) / 1000.0
        #print (temp_c)
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #print (temp_f)
        return temp_f

while True:
	#print(read_temp())
	temp_value = read_temp()
	normal_temp=86
	frequency =4
	if temp_value > normal_temp:
            print (temp_value)
            current_time = datetime.datetime.now()
            print (current_time)
        else:
            print 'system is in sleep'
	state=0
	temp_threshold = 87
	if temp_value > temp_threshold:
		state = 1
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		pin = 22
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, (GPIO.LOW if state == 0 else GPIO.HIGH))
		client = Client(client_id="my_id", userdata="user1")
		client.connect("192.168.1.16")
		message = str(temp_value)
		topic = "temp_value"
		client.publish(topic, message)
	state = 0
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	pin = 22
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, (GPIO.LOW if state == 0 else GPIO.HIGH))
        s.enter(60, 1, read_temp, ())

s.enter(60, 1, read_temp, (s,))
s.run()





#from sched import scheduler
#from time import time, sleep

#s = scheduler(time, sleep)

#def run_periodically(start, end, interval, func):
 #   event_time = start
  #  while event_time < end:
   #     s.enterabs(event_time, 0, func, ())
    #    event_time += interval
    #s.run()

#if __name__ == '__main__':

 #   def say_hello():
  #      print 'hello'    

   # run_periodically(time()+5, time()+10, 1, say_hello)
        

