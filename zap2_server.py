

from mqtt_functions import mqtt_obj
from sql_functions import funcionesSQL


conex_mqtt = mqtt_obj()
conex_sql = funcionesSQL()


# Me conecto a todos los Topics e indico las funciones que atienden a cada topic
conex_mqtt.on_connect()

# Pruebo la conexion a la db
conex_sql.test_db_conn()


