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
