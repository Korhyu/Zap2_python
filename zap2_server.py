
import paho.mqtt.client as mqtt
import math
from mqtt_functions import mqtt_obj
from sql_functions import funcionesSQL
from electric_data import electric_data


def on_connect(client, userdata, flags, rc): 
    print("Connected with result code " + str(rc)) 
    # Subscribing in on_connect() means that if we lose the connection and 
    # reconnect then subscriptions will be renewed.
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


def on_message_tension(client, userdata, msg, datos):
    if float(msg.payload) is 9999:
        flag_v = True
        cont = 0

        if flag_v and flag_i is True:
            flag_v = False
            flag_i = False
            datos.load_data(vec_tension, vec_corriente)

    else:
        vec_tension.append(float(msg.payload))
        cont = cont + 1


def on_message_corriente(self, client, userdata, msg):
    if float(msg.payload) is 9999:
        self.flag_i = True
        self.cont = 0

        if self.flag_v and self.flag_i is True:
            self.flag_v = False
            self.flag_i = False
            datos = electric_data(self.vec_tension, self.vec_corriente)
            datos.analize()

    else:
        self.vec_corriente.append(float(msg.payload))
        self.cont = self.cont + 1

def on_message_f_sampl(self, client, userdata, msg):
    electric_data.load_fs(float(msg.payload))

def on_message_t_muest(self, client, userdata, msg):
    electric_data.load_tm(float(msg.payload))



def main():

    tm = 2                      #Tiempo de muestreo
    fs = 40000                  #Frecuencia de muestreo
    ts = 1/fs                   #Periodo de muestreo
    vec_tension = [0] * math.ceil(tm / ts)
    vec_corriente = [0] * math.ceil(tm / ts)

    datos = electric_data(ts, tm)


    obj_mqtt = mqtt_obj()
    obj_sql = funcionesSQL()

    # Me conecto a todos los Topics e indico las funciones que atienden a cada topic
    server = obj_mqtt.connect_server('localhost', 1883, 60)

    # Pruebo la conexion a la db
    conex_sql.test_db_conn()


