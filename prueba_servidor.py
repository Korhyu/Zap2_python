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
   client.subscribe("/suma")
   client.subscribe("/resta")
   client.subscribe("/promedio")
   client.subscribe("/lectura")


# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg):
    print(msg.topic+" "+str( msg.payload))

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()

    # Check if this is a message for the Pi LED. 
    if msg.topic == "/suma":
        cont = cont + 1
        print("cont = ", cont)
        if cont == 1:
            aux = re.findall("\d+\.\d+", msg.payload)
            print("cont = ", cont)
        if cont == 2:
            aux == aux + re.findall("\d+\.\d+", msg.payload)
            print("cont = ", cont)
            cont = 0
            print("cont = ", cont)
            print("La suma es ", aux)

            cur.execute("INSERT INTO `prueba`(`cadena`, `coma`) VALUES ('s'," + str(aux) + ")")

    if msg.topic == "/resta": 
        cont = cont + 1
        if cont == 1:
            aux = re.findall("\d+\.\d+", msg.payload)
        if cont == 2:
            aux == aux + re.findall("\d+\.\d+", msg.payload)
            cont = 0
            print("La resta es ", aux) 

            cur.execute("INSERT INTO `prueba`(`cadena`, `coma`) VALUES ('r'," + str(aux) + ")")

    if msg.topic == "/promedio": 
        cont = cont + 1
        if cont == 1:
            aux = re.findall("\d+\.\d+", msg.payload)
        if cont == 2:
            aux == (aux + re.findall("\d+\.\d+", msg.payload)) / cont
            cont = 0
            print("El promedio es ", aux)
            cur.execute("INSERT INTO `prueba`(`cadena`, `coma`) VALUES ('p'," + str(aux) + ")")

    if msg.topic == "/lectura":
        "leer la base de datos completa"


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
