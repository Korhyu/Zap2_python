import sys
import os
import time
import paho.mqtt.client as paho
import mysql.connector
from mysql.connector import Error

global mqttclient;
global broker;
global port;


# Datos MQTT
broker = "localhost";
port = 1883;
MQTT_TOPICS = [ ("/lec", 0),
                ("/esc", 0)];

# Datos de la base de datos
db = mysql.connector.connect(   host="localhost",
                                user="zap2app",
                                passwd="zap2app",
                                db="zap2")


def esc_callback(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))

    try:
        cur = db.cursor()
        instruccion = """INSERT INTO `prueba`(`cadena`, `coma`) VALUES ('test', %f)"""
        datos = float(msg.payload.decode("utf-8"))
        print("QUERY: " + instruccion + "datos " + datos)
        cur.execute(instruccion, datos)
        print("Dato almacenado")

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:   
        cur.close()



def lec_callback(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    
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



def pub(topic, value):
    mqttclient.publish(topic, value, 0, True)





mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttclient = paho.Client(client_uniq, False) #nocleanstart
mqttclient.connect(broker, port, 60)

mqttclient.loop_start()
mqttclient.subscribe(MQTT_TOPICS)

mqttclient.message_callback_add("/esc", esc_callback)
mqttclient.message_callback_add("/lec", lec_callback)

print("Script is running, press Ctrl-C to quit...") 
while True:
    pass
