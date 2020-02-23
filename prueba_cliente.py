# imports
import time
import paho.mqtt.client as mqtt
import re
import string
import random



# Setup callback functions that are called when MQTT events happen like 
# connecting to the server or receiving data from a subscribed feed. 
def on_connect(client, userdata, flags, rc): 
   print("Connected with result code " + str(rc)) 
   # Subscribing in on_connect() means that if we lose the connection and 
   # reconnect then subscriptions will be renewed. 
   client.subscribe("lec", qos=0)
   client.subscribe("devol", qos=0)


# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg): 
    print(msg.topic+" "+str( msg.payload)) 
    # Check if this is a message for the Pi LED. 
    if msg.topic == '/devol': 
        print(msg.topic+" "+str( msg.payload)) 

    if msg.topic == '/promedio': 
        print(msg.topic+" "+str( msg.payload)) 


# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running 
# this script and the MQTT server. 
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 
client.connect('192.168.0.28', 1883, 60) 
# Connect to the MQTT server and process messages in a background thread. 
client.loop_start() 
# Main loop to listen for button presses. 
print('Script is running, press Ctrl-C to quit...') 
while True:
    
    time.sleep(5)

    num = random.randint(1,101)
    print('publicando el numero ' + str(num))
    client.publish(topic='esc/', payload=num, qos=0, retain=False)