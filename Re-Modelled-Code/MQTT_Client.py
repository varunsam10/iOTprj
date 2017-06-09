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
