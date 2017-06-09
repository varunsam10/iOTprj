import os
import glob
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

#def scheduler_func():
	
	#print overallstart_time
	#finish_time = overallstart_time+timedelta(minutes=2)
	#print finish_time
	#temperature = []
	#if (current_time-overallstart_time)==timedelta(minutes=2):
		#temp_func()
		#overallstart_time = datetime.datetime.now().replace(microsecond=0)
		#print "The end of each schedule"
	#overallstart_time=curren

def main():
	#frequency=sys.argv[0]
	frequency = 2
	overallstart_time = datetime.datetime.now().replace(microsecond=0)
	next_iteration_time=overallstart_time+timedelta(minutes=5)
	print "Start one"
	temp_func()
	print overallstart_time
	print next_iteration_time
	for i in range(0,frequency):
		print next_iteration_time-overallstart_time
		current_time=datetime.datetime.now().replace(microsecond=0)
		print current_time
		if (next_iteration_time-current_time==timedelta(minutes=5)):
			temp_func()
			print "The end of Iteration"
		print "The end of each frequency"
		next_iteration_time=datetime.datetime.now().replace(microsecond=0)+timedelta(minutes=5)
		print next_iteration_time
	
	
	


if __name__ == "__main__":
    main()
