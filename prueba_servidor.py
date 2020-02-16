#SQL
import MySQLdb

# RPi
import time
import paho.mqtt.client as mqtt

import re

#Cosas de la Rasp
import RPi.GPIO as GPIO 

# Configuration: 
LED_PIN        = 24 
BUTTON_PIN     = 23 

# Initialize GPIO for LED and button. 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False) 
GPIO.setup(LED_PIN, GPIO.OUT) 
GPIO.output(LED_PIN, GPIO.LOW) 
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 


db = MySQLdb.connect(host="localhost",
                     user="zap2app",
                     passwd="zap2app",
                     db="zap2")


# Setup callback functions that are called when MQTT events happen like 
# connecting to the server or receiving data from a subscribed feed. 
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code " + str(rc)) 
    # Subscribing in on_connect() means that if we lose the connection and 
    # reconnect then subscriptions will be renewed. 
    client.subscribe("esc", qos=0)
    client.subscribe("lec", qos=0)
    client.message_callback_add("esc", on_message_esc)
    client.message_callback_add("lec", on_message_lec)


def on_message_esc(client, userdata, msg):
    cur = db.cursor()
    comando = "INSERT INTO `prueba`(`cadena`, `coma`) VALUES ('test'," + str(msg.payload) + ")"
    print("QUERY: " + comando)
    cur.execute(comando)
    cur.close()

def on_message_lec(client, userdata, msg):
    print("todavia nada")


# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg):
    print("Recibido: " + msg.topic + " " + str( msg.payload))

# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running 
# this script and the MQTT server. 
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 
client.connect("localhost", 1883, 60) 
# Connect to the MQTT server and process messages in a background thread. 
client.loop_start() 
# Main loop to listen for button presses. 
print("Script is running, press Ctrl-C to quit...") 
while True: 
   # Look for a change from high to low value on the button input to 
   # signal a button press. 
   button_first = GPIO.input(BUTTON_PIN) 
   time.sleep(0.02)  # Delay for about 20 milliseconds to debounce. 
   button_second = GPIO.input(BUTTON_PIN) 
   if button_first == GPIO.HIGH and button_second == GPIO.LOW: 
       print("Button pressed!") 
       # Send a toggle message to the ESP8266 LED topic. 
       client.publish("/leds/esp8266", "TOGGLE") 
