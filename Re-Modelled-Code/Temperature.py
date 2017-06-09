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
	
	
    
