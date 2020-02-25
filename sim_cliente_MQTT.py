# Simulacro de cliente MQTT
# Debe generar datos y enviarlos por MQTT al servidor y ver si este
# los carga en la base de datos

import random
import time
import paho.mqtt.client as mqtt
import math
from mqtt_functions import mqtt_obj


obj_mqtt = mqtt_obj()
server = obj_mqtt.connect_server('192.168.0.28', 1883, 60)

obj_mqtt.data.fs = 2000
obj_mqtt.data.ts = 1/obj_mqtt.data.fs
obj_mqtt.data.tm = 2
vp = 311




#server.publish(topic='/test', payload='sim cliente', qos=0, retain=False)
print("Empienza el envio de datos")

for j in range(obj_mqtt.data.fs * obj_mqtt.data.tm):
    n = random.randint(-100,100)
    num = vp * math.sin(2 * math.pi* 50 * j/obj_mqtt.data.fs)
    server.publish(topic='/medicion/tension', payload=num, qos=0, retain=False)

    if (j % 100) is 0:
        print("Enviado mensaje n " + str(j))
    
    time.sleep(0.01)


server.publish(topic='/medicion/tension', payload='EoV', qos=0, retain=False)
