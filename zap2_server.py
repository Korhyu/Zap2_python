
import paho.mqtt.client as mqtt
from mqtt_functions import mqtt_obj
from sql_functions import funcionesSQL


obj_mqtt = mqtt_obj()
obj_sql = funcionesSQL()


# Me conecto a todos los Topics e indico las funciones que atienden a cada topic
conex_mqtt = mqtt_obj.connect_server("localhost", 1883, 60)

# Pruebo la conexion a la db
conex_sql.test_db_conn()


