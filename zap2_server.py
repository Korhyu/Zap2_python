import math
import struct
import time
import paho.mqtt.client as mqtt 
import mysql.connector
from mysql.connector import Error
from mqtt_functions import mqtt_obj
from sql_functions import funcionesSQL
from electric_data import electric_data
from ast import literal_eval
from codecs import decode


# Variables Globales
datos = electric_data(1, 0)
vector_V = []
vector_I = []



def on_message_f_sampl(client, userdata, msg):
    global datos
    valor = float(msg.payload.decode("utf-8"))
    datos.ts = (1/valor)
    print("Frecuencia de muestreo modificada: " + str(1/datos.ts))

def on_message_t_muest(client, userdata, msg):
    global datos
    valor = float(msg.payload.decode("utf-8"))
    datos.tm = valor
    print("Tiempo de muestreo modificado: " + str(datos.tm))



def on_connect(client, userdata, flags, rc): 
    print("Connected with result codess " + str(rc)) 
    MQTT_TOPICS = [ ("/test", 0),
                    ("/medicion/tension", 0),
                    ("/medicion/corriente", 0),
                    ("/medicion/f_sampl", 0),
                    ("/medicion/t_muest", 0)
                    ("/medicion/time", 0)]

    client.subscribe(MQTT_TOPICS)
    client.message_callback_add("/medicion/tension", on_message_tension)
    client.message_callback_add("/medicion/corriente", on_message_corriente)
    client.message_callback_add("/medicion/f_sampl", on_message_f_sampl)
    client.message_callback_add("/medicion/t_muest", on_message_t_muest)
    client.message_callback_add("/medicion/time", on_message_time)
    client.message_callback_add("/test", on_message_test)

    print("Conectado a los topicos:" )
    for j in range(len(MQTT_TOPICS)):
        print("\t" + str(MQTT_TOPICS[j][0]))


def on_message_test(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_message_time(client, userdata, msg):
    tag = str(msg.payload.decode("utf-8"))


def on_message_tension(client, userdata, msg):
    global datos
    global vector_V
    global vector_I

    try:
        valor = float(msg.payload.decode("utf-8"))
        vector_V.append(valor)
        #print(str(valor) + " [V]")   

    except ValueError:
        print("Fin de vector Tension")
        datos.flagV = True
        datos.load_voltage(vector_V)

def on_message_corriente(client, userdata, msg):
    global datos
    global vector_V
    global vector_I

    try:
        valor = float(msg.payload.decode("utf-8"))
        vector_I.append(valor)
        #print(str(valor) + " [A]")     

    except ValueError:
        print("Fin de vector Corriente")
        datos.flagI = True
        datos.load_current(vector_I)         

def conexion_mqtt(self):
    client = mqtt.Client() 
    client.on_connect = self.on_connect 
    #client.on_message = on_message 
    client.connect('localhost', 1883, 60)
    client.loop_start()


if __name__ == "__main__":

    # Me conecto a todos los Topics e indico las funciones que atienden a cada topic
    conn_mqtt = conexion_mqtt()

    # Pruebo la conexion a la db
    obj_sql = funcionesSQL()
    #obj_sql.test_db_conn()


    while True:
        time.sleep(2)

        #print("datos.flagV: " + str(datos.flagV) + "  datos.flagI: " + str(datos.flagI))

        if datos.flagV is True and datos.flagI is True:
            print("Vectores recibidos, comienza analisis...")
            datos.load_data(vector_V, vector_I)
            #datos.print_data()
            vector_V = []
            vector_I = []
            datos.analize()
