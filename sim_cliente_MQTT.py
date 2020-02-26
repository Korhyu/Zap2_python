# Simulacro de cliente MQTT
# Debe generar datos y enviarlos por MQTT al servidor y ver si este
# los carga en la base de datos

import random
import time
import math
import paho.mqtt.client as mqtt
from mqtt_functions import mqtt_obj


obj_mqtt = mqtt_obj()
server = obj_mqtt.connect_server('192.168.0.28', 1883, 60)

obj_mqtt.data.fs = 10000
obj_mqtt.data.ts = float(1/obj_mqtt.data.fs)
obj_mqtt.data.tm = 0.5
vp = 311
ap = 2


print("Empienza el envio de datos")
time.sleep(0.5)

server.publish(topic='/medicion/f_sampl', payload=obj_mqtt.data.fs, qos=0, retain=False)
server.publish(topic='/medicion/t_muest', payload=obj_mqtt.data.tm, qos=0, retain=False)

#Datos de tension
for j in range(math.ceil(obj_mqtt.data.fs * obj_mqtt.data.tm)):
    n = random.randint(-100,100)/10000
    num = vp * math.sin(2 * math.pi* 50 * j * obj_mqtt.data.ts) + vp * n
    num = float("{0:.3f}".format(num))
    server.publish(topic='/medicion/tension', payload=num, qos=0, retain=False)

    if (j % 100) is 0:
        print("Enviado mensaje n " + str(j))
    
    time.sleep(0.01)

msj_fin = "EoV"
print("Enviado mensaje " + msj_fin)
server.publish(topic='/medicion/tension', payload=msj_fin, qos=0, retain=False)

time.sleep(2)

#Datos de corriente
for j in range(math.ceil(obj_mqtt.data.fs * obj_mqtt.data.tm)):
    n = random.randint(-100,100)/10000
    num = ap * math.sin(2 * math.pi* 50 * j * obj_mqtt.data.ts) + ap * n
    num = float("{0:.3f}".format(num))
    server.publish(topic='/medicion/corriente', payload=num, qos=0, retain=False)

    if (j % 100) is 0:
        print("Enviado mensaje n " + str(j))
    
    time.sleep(0.01)

msj_fin = "EoV"
print("Enviado mensaje " + msj_fin)
server.publish(topic='/medicion/corriente', payload=msj_fin, qos=0, retain=False)


time.sleep(2)