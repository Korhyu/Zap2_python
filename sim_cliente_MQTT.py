# Simulacro de cliente MQTT
# Debe generar datos y enviarlos por MQTT al servidor y ver si este
# los carga en la base de datos

import random
import time
import paho.mqtt.client as mqtt
from mqtt_functions import mqtt_obj

conexion = mqtt_obj()
conexion.connect_cliente('192.168.0.21', 1883, 60)

while True:
    time.sleep(10)

    for j in 40000:
        num = 220 + random.randint(-1001,1001)/100
        conexion.publish(topic='medicion/tension', payload=num, qos=0, retain=False)
    
    conexion.publish(topic='medicion/tension', payload=9999, qos=0, retain=False)
