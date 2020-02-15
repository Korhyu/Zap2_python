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
   client.subscribe("promedio", qos=0)
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
client.connect('192.168.0.21', 1883, 60) 
# Connect to the MQTT server and process messages in a background thread. 
client.loop_start() 
# Main loop to listen for button presses. 
print('Script is running, press Ctrl-C to quit...') 
while True:
    num1 = random.randint(1,101)
    num2 = random.randint(1,101)
    print('publicando suma de numeros ' + str(num1) + ' y ' + str(num2))
    client.publish(topic='suma', payload=num1, qos=0, retain=False)
    client.publish(topic='suma', payload=num2, qos=0, retain=False)

    time.sleep(3)
    print('publicando resta de numeros ' + str(num1) + ' y ' + str(num2))
    client.publish('/resta', num1)
    client.publish('/resta', num2)

    time.sleep(3)
    print('publicando promedio de numeros ' + str(num1) + ' y ' + str(num2))
    client.publish('/promedio', num1)
    client.publish('/promedio', num2)




'''
operacion = input('Ingrese la operacion a realizar: ')
    if operacion != 4:
        num1 = input('Ingrese el primer numero:  ')
        num2 = input('Ingrese el segundo numero: ')

        if operacion == 1:
            client.publish('/suma', num1)
            client.publish('/suma', num2)
        
        elif operacion == 2:
            client.publish('/resta', num1)
            client.publish('/resta', num2)

        elif operacion == 3:
            client.publish('/promedio', num1)
            client.publish('/promedio', num2)

        else:
            print("Ingrese un caracter valido \n\t'1' para sumar \n\t'2' para restar \n\t'3' para promediar \n\t'4' para leer la base")

    else:
        client.publish('/completo')
'''