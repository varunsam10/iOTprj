import os
import glob
from time import sleep
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

def main():
	Normal_temp=80
	body_temp = Temperature.Temperature(device_file)
	temperature = []
	temperature.append(body_temp.get_temp())
	max_temp = max(temperature)
	print max_temp
	if max_temp > Normal_temp:
		publish = MQTT_Client.MQTT_Client(max_temp)
		publish.RunMQTT_Client()
	
	
if __name__ == "__main__":
    main()
