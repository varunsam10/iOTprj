import time
from paho.mqtt.client import Client
 
def on_message(c, userdata, mesg):
    print "message: %s %s %s" % (userdata, mesg.topic, mesg.payload)
 
client = Client(client_id="my_id", userdata="user1")
client.connect("172.27.246.86")
client.on_message = on_message
client.subscribe("temp_value")
while True:
    client.loop()
    time.sleep(1)
import time
from paho.mqtt.client import Client

class MQTT_Client:
	
	def __init__(self,temp_value):
		self.temp_value = temp_value
		
	def RunMQTT_Client(self):
		client = Client(client_id="my_id_pub", userdata="user2")
		client.connect("172.27.246.86")
		message = str(self.temp_value)
		topic = "temp_value"
		client.publish(topic, message)
ó
ö1:Yc           @   s3   d  d l  Z  d  d l m Z d d d     YZ d S(   i˙˙˙˙N(   t   Clientt   MQTT_Clientc           B   s   e  Z d    Z d   Z RS(   c         C   s   | |  _  d  S(   N(   t
   temp_value(   t   selfR   (    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/MQTT_Client.pyt   __init__   s    c         C   sK   t  d d d d  } | j d  t |  j  } d } | j | |  d  S(   Nt	   client_idt	   my_id_pubt   userdatat   user2s   172.27.246.86R   (   R    t   connectt   strR   t   publish(   R   t   clientt   messaget   topic(    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/MQTT_Client.pyt   RunMQTT_Client	   s
    (   t   __name__t
   __module__R   R   (    (    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/MQTT_Client.pyR      s   	(    (   t   timet   paho.mqtt.clientR    R   (    (    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/MQTT_Client.pyt   <module>   s   import RPi.GPIO as GPIO
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
	


ó
ź6:Yc           @   s3   d  d l  Z  d  d l m Z d d d     YZ d S(   i˙˙˙˙N(   t   sleept   Temperaturec           B   s,   e  Z d    Z d   Z d   Z d   Z RS(   c         C   s   | |  _  d  S(   N(   t   device_file(   t   selfR   (    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/Temperature.pyt   __init__   s    c         C   s,   t  |  j d  } | j   } | j   | S(   Nt   r(   t   openR   t	   readlinest   close(   R   t   ft   lines(    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/Temperature.pyt   read_temp_raw   s    
c         C   sŁ   |  j    } x4 | d j   d d k rB t d  |  j    } q W| d j d  } | d k r | d | d } t |  d	 } | d
 d d } | GH| Sd  S(   Ni    iý˙˙˙t   YESgÉ?i   s   t=i˙˙˙˙i   g     @@g      "@g      @g      @@(   R   t   stripR    t   findt   float(   R   R
   t
   equals_post   temp_stringt   temp_ct   temp_f(    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/Temperature.pyt	   read_temp   s    
c         C   s
   |  j    S(   N(   R   (   R   (    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/Temperature.pyt   get_temp$   s    (   t   __name__t
   __module__R   R   R   R   (    (    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/Temperature.pyR      s   			(    (   t   globt   timeR    R   (    (    (    sU   /home/pi/Desktop/iot/Temperature-Sensor/Re-Modelled-Code/Final_IOT prj/Temperature.pyt   <module>   s   
import os
import glob
import time
from time import sleep
from datetime import timedelta
import RPi.GPIO as GPIO
import sys
import datetime
import Temperature
import MQTT_Client


#intialise the device
os.system ('sudo modprobe w1-gpio')
os.system ('sudo modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def temp_func():
	Normal_temp=93
	overallstart_time = datetime.datetime.now().replace(microsecond=0)
	print overallstart_time
	finish_time = overallstart_time+timedelta(minutes=1)
	print finish_time
	temperature = []
	while overallstart_time != finish_time:
		body_temp = Temperature.Temperature(device_file)
		temperature.append(body_temp.get_temp())
		overallstart_time = datetime.datetime.now().replace(microsecond=0)
		print overallstart_time
	max_temp = max(temperature)
	print ("The maximum value of temperature from th list is", max_temp)
	if max_temp > Normal_temp:
		publish = MQTT_Client.MQTT_Client(max_temp)
		publish.RunMQTT_Client()


def main():
	frequency = int(sys.argv[1])
	delta = int(sys.argv[2])
	sleep = delta*60
	overallstart_time = datetime.datetime.now().replace(microsecond=0)
	next_iteration_time=overallstart_time+timedelta(minutes=delta)
	print "Start one"
	#temp_func()
	print overallstart_time
	print next_iteration_time
	for i in range(0,frequency):
		print next_iteration_time-overallstart_time
		current_time=datetime.datetime.now().replace(microsecond=0)
		print current_time
		if (next_iteration_time-current_time==timedelta(minutes=delta)):
			temp_func()
			print "The end of Iteration"
		time.sleep(sleep)
		print ("The end of each frequency",i)
		next_iteration_time=datetime.datetime.now().replace(microsecond=0)+timedelta(minutes=delta)
		print next_iteration_time
	
if __name__ == "__main__":
    main()
import glob
from time import sleep


#intialise the device
#os.system ('sudo modprobe w1-gpio')
#os.system ('sudo modprobe w1-therm')
#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'
	
class Temperature:
	def __init__(self,device_file):
		self.device_file=device_file
	
	def read_temp_raw(self):
		f = open(self.device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines
	
	def read_temp(self):
		lines = self.read_temp_raw()
		while lines[0].strip()[-3:] != 'YES':
			sleep(0.2)
			lines = self.read_temp_raw()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			#print(temp_string)
			temp_c = float(temp_string) / 1000.0
			#print (temp_c)
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			print (temp_f)
			return temp_f
	def get_temp(self):
		return self.read_temp()
	
	
    
