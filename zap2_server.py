import math
import mysql.connector
from mysql.connector import Error
from mqtt_functions import mqtt_obj
from sql_functions import funcionesSQL
from electric_data import electric_data


if __name__ == "__main__":

    flag_v = False
    flag_i = False

    print("punto 0")

    tm = 2                      #Tiempo de muestreo
    fs = 20000                  #Frecuencia de muestreo
    ts = float(1/fs)            #Periodo de muestreo

    vec_tension = [0] * math.ceil(tm / ts)
    vec_corriente = [0] * math.ceil(tm / ts)

    datos = electric_data(ts, tm)

    print("punto 1")

    obj_mqtt = mqtt_obj()
    obj_sql = funcionesSQL()

    # Me conecto a todos los Topics e indico las funciones que atienden a cada topic
    server = obj_mqtt.connect_server('localhost', 1883, 60)

    print("punto 1.5")

    # Pruebo la conexion a la db
    #obj_sql.test_db_conn()

    print("punto 2")

    while True:

        if flag_v and flag_i is True:
            flag_v = False
            flag_i = False
            datos.analize()




def on_message_tension(client, userdata, msg, datos):
    try:
        valor = float(msg.payload)
        flag_v = True
        cont = 0            

    except ValueError:
        print("Fin de vector")
        datos.vec_tension.append()
        cont = cont + 1


def on_message_corriente(client, userdata, msg, datos):
    try:
        valor = float(msg.payload)
        flag_i = True
        cont = 0            

    except ValueError:
        print("Fin de vector")
        datos.vec_corriente.append()
        cont = cont + 1

def on_message_f_sampl(self, client, userdata, msg):
    electric_data.load_fs(float(msg.payload))

def on_message_t_muest(self, client, userdata, msg):
    electric_data.load_tm(float(msg.payload))





