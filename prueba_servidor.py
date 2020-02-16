#SQL
import mysql.connector
from mysql.connector import Error

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


# Datos de la base de datos
db = mysql.connector.connect(   host="localhost",
                                user="zap2app",
                                passwd="zap2app",
                                db="zap2")

# Funcion que se ejecuta en la conexion
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code " + str(rc)) 

    client.subscribe("esc", qos=0)
    client.subscribe("lec", qos=0)
    client.message_callback_add("esc", on_message_esc)
    client.message_callback_add("lec", on_message_lec)


#funcion de escritura de db
def on_message_esc(client, userdata, msg):
    try:
        cur = db.cursor()
        instruccion = """INSERT INTO `prueba`(`cadena`, `coma`) VALUES ('test', %f)"""
        datos = float(msg.payload)
        print("QUERY: " + instruccion + "datos " + datos)
        cur.execute(instruccion, datos)
        cur.close()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        print("Dato almacenado")


# Funcion de lectura de db
def on_message_lec(client, userdata, msg):
    print("todavia nada")


# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg):
    print("Recibido: " + msg.topic + " " + str( msg.payload))






#Funcion ppal, primero verifico que la conexion con la db funcione
try:
    if db.is_connected():
        db_Info = db.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if (db.is_connected()):
        cursor.close()
        db.close()
        print("MySQL connection is closed - Linea 90")

# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running 
# this script and the MQTT server. 
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 
client.connect("localhost", 1883, 60)  
client.loop_start() 
 
try:
    cur = db.cursor()
    instruccion = """INSERT INTO prueba(cadena, coma) VALUES ('test', 1)"""
    cur.execute(instruccion)
    cur.close()

except Error as e:
    print("Error enviando el dato ", e)

finally:
    if (db.is_connected()):
        cursor.close()
        db.close()
        print("MySQL connection is closed - Linea 113")

'''
print("Script is running, press Ctrl-C to quit...") 
while True:
    print("Programa corriendo")
    time.sleep(5)
'''