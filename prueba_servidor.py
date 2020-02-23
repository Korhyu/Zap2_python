#SQL
import re
import time
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
#from sql_functions import insertar_prueba_db


# RPi
import RPi.GPIO as GPIO




# Datos de la base de datos
db = mysql.connector.connect(   host="localhost",
                                user="zap2app",
                                passwd="zap2app",
                                db="zap2")

# Funcion que se ejecuta en la conexion
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code " + str(rc))
    
    client.message_callback_add("esc", on_message_esc)
    client.message_callback_add("lec", on_message_lec)
    
    MQTT_TOPICS = [ ("/lec", 0),
                    ("/esc", 0)]

    client.subscribe(MQTT_TOPICS)
    


#funcion de escritura de db
def on_message_esc(client, userdata, msg):
    print("mensaje recibido")
    try:
        cur = db.cursor()
        instruccion = """INSERT INTO `prueba`(`cadena`, `coma`) VALUES ('test', %f)"""
        datos = float(msg.payload.decode("utf-8"))
        print("QUERY: " + instruccion + "datos " + datos)
        cur.execute(instruccion, datos)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        print("Dato almacenado")
        cur.close()


# Funcion de lectura de db
def on_message_lec(client, userdata, msg):
    try:
        cur = db.cursor()
        instruccion = """SELECT `*` FROM `prueba`"""
        print("QUERY: " + instruccion)
        cursor.execute(instruccion)
        cur.close()

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        for (id, entero, coma, cadena) in cursor:
            print("DATOs: {}, {}, {}, {}".format(id, entero, coma, cadena) )


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
        print("MySQL connection is closed")

# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running 
# this script and the MQTT server. 
client = mqtt.Client() 
client.connect("localhost", 1883, 60)
client.loop_start()
client.on_connect = on_connect 
client.on_message = on_message


 

print("Script is running, press Ctrl-C to quit...") 
while True:
    time.sleep(5)