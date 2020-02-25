import math
import mysql.connector
from mysql.connector import Error
from mqtt_functions import mqtt_obj
from sql_functions import funcionesSQL
from electric_data import electric_data


if __name__ == "__main__":

    flag_v = False
    flag_i = False

    vec_tension = []
    vec_corriente = []

    obj_mqtt = mqtt_obj()
    datos = electric_data(1,1)
    obj_mqtt.data = datos
    

    # Me conecto a todos los Topics e indico las funciones que atienden a cada topic
    server = obj_mqtt.connect_server('localhost', 1883, 60)

    # Pruebo la conexion a la db
    obj_sql = funcionesSQL()
    #obj_sql.test_db_conn()


    while True:
        if flag_v and flag_i is True:
            print("Vectores recividos, comienza analisis...")
            flag_v = False
            flag_i = False
            datos.analize()



def on_message_f_sampl(self, client, userdata, msg):
    electric_data.load_fs(float(msg.payload))

def on_message_t_muest(self, client, userdata, msg):
    electric_data.load_tm(float(msg.payload))
