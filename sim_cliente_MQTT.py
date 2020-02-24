# Simulacro de cliente MQTT
# Debe generar datos y enviarlos por MQTT al servidor y ver si este
# los carga en la base de datos

import random
import time
import paho.mqtt.client as mqtt
import math
from mqtt_functions import mqtt_obj


conexion = mqtt_obj()
conexion.connect_cliente('192.168.0.28', 1883, 60)

fs = 20000
ts = 2
vp = 311

while True:
    time.sleep(1)

    conexion.publish(topic='test', payload='sim cliente', qos=0, retain=False)

    for j in (fs * ts):
        n = 0.01 * random.randint(-100,100)
        num = vp * math.sin(2*math.pi*50*(1/fs)* j) + n * vp
        conexion.publish(topic='medicion/tension', payload=num, qos=0, retain=False)
   
    conexion.publish(topic='medicion/tension', payload=9999, qos=0, retain=False)
