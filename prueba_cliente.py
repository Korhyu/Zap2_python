# imports
import time
import paho.mqtt.client as mqtt
import re



# Setup callback functions that are called when MQTT events happen like 
# connecting to the server or receiving data from a subscribed feed. 
def on_connect(client, userdata, flags, rc): 
   print("Connected with result code " + str(rc)) 
   # Subscribing in on_connect() means that if we lose the connection and 
   # reconnect then subscriptions will be renewed. 
   client.subscribe("/promedio")
   client.subscribe("/devol")


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
client.connect('192.168.0.21', 1883, 60) 
# Connect to the MQTT server and process messages in a background thread. 
client.loop_start() 
# Main loop to listen for button presses. 
print('Script is running, press Ctrl-C to quit...') 
while True: 
    operacion = str(input('Ingrese la operacion a realizar: '))
    print (type(operacion))
    if operacion != "l":
        num1 = input('Ingrese el primer numero:  ')
        num2 = input('Ingrese el segundo numero: ')

        if operacion == "s":
            client.publish('/suma', num1)
            client.publish('/suma', num2)
        
        if operacion == "r":
            client.publish('/resta', num1)
            client.publish('/resta', num2)

        if operacion == "p":
            client.publish('/promedio', num1)
            client.publish('/promedio', num2)

        else:
            print("Ingrese un caracter valido \n's' para sumar \n'r' para restar \n'p' para promediar \n'l' para leer la base")

    else:
        client.publish('/completo')