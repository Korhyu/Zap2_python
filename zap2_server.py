import math
import paho.mqtt.client as mqtt 
import mysql.connector
from mysql.connector import Error
from mqtt_functions import mqtt_obj
from sql_functions import funcionesSQL
from electric_data import electric_data


if __name__ == "__main__":

    flag_v = False
    flag_i = False

    datos = electric_data(1, 0)

    

    # Me conecto a todos los Topics e indico las funciones que atienden a cada topic
    conn_mqtt = conexion_mqtt()

    # Pruebo la conexion a la db
    obj_sql = funcionesSQL()
    #obj_sql.test_db_conn()


    while True:
        if flag_v and flag_i is True:
            print("Vectores recibidos, comienza analisis...")
            flag_v = False
            flag_i = False
            datos.analize()



def on_message_f_sampl(self, client, userdata, msg):
    electric_data.load_fs(float(msg.payload))

def on_message_t_muest(self, client, userdata, msg):
    electric_data.load_tm(float(msg.payload))



def on_connect(client, userdata, flags, rc): 
    print("Connected with result code " + str(rc)) 
    MQTT_TOPICS = [ ("/test", 0),
                    ("/medicion/tension", 0),
                    ("/medicion/corriente", 0),
                    ("/config/f_sampl", 0),
                    ("/config/t_muest", 0)]

    client.subscribe(MQTT_TOPICS)
    client.message_callback_add("/medicion/tension", on_message_tension)
    client.message_callback_add("/medicion/corriente", on_message_corriente)
    client.message_callback_add("/medicion/f_sampl", on_message_f_sampl)
    client.message_callback_add("/medicion/t_muest", on_message_t_muest)
    client.message_callback_add("/test", on_message_test)

    print("Conectado a los topicos %s" % MQTT_TOPICS)


def on_message_test(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_message_tension(client, userdata, msg):
    try:
        valor = float(msg.payload)
        datos.v.append(valor)
        print(str(valor) + " [V]")
        cont = cont + 1      

    except ValueError:
        print("Fin de vector")
        flag_v = True
        cont = 0 

def on_message_corriente(client, userdata, msg):
    try:
        valor = float(msg.payload)
        datos.i.append(valor)
        print(str(valor) + " [A]")
        cont = cont + 1      

    except ValueError:
        print("Fin de vector")
        flag_i = True
        cont = 0 

def conexion_mqtt():
    client = mqtt.Client() 
    client.on_connect = on_connect 
    #client.on_message = on_message 
    client.connect('localhost', 1883, 60)
    client.loop_start()
