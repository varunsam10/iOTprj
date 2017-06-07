import os
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
import sys
from paho.mqtt.client import Client
import datetime
 

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


def repeat(temp_list):
     for i in range (len(temp_list) - 1):
        if temp_list[i] == temp_list[i + 1]:
            return True;
        return False;

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        #print(temp_string)
        temp_c = float(temp_string) / 1000.0
        #print (temp_c)
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        print (temp_f)
        return temp_f

Normal_temp=85
list_temp=[]

#overallstart_time = datetime.datetime.now()
#print(str(overallstart_time))

while True:
	temp_value=read_temp()
	systemstart_time = datetime.datetime.now()
	print (systemstart_time)
	while temp_value > Normal_temp:
		list_temp.append(temp_value)
		print (list_temp)
		finish_time = datetime.datetime.now()
                print (str(finish_time))
                total_duration = (finish_time - systemstart_time)
                print total_duration
                if (str(total_duration) < "0:10:00"):
                    continue
                else:
                    break   
                #finishoverall_time = datetime.datetime.now()
                #print (str(finishoverall_time))
                #totalsystem_duration = (finish_time - overallstart_time)
                #print totalsystem_duration
                #if (str(totalsystem_duration) > "4:00:00"):
                #    continue
                #else:
                #    break        
     
if max_temp > Normal_temp:
    if repeat(list_temp):
        state = 1
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        pin = 22
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, (GPIO.LOW if state == 0 else GPIO.HIGH))
        client = Client(client_id="my_id_pub", userdata="user2")
        client.connect("172.27.246.86")
        message = str(temp_value)
        topic = "temp_value"
        client.publish(topic, message)
        break
    
	

