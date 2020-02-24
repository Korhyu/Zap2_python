import time
import paho.mqtt.client as mqtt
from electric_data import electric_data

class mqtt_obj():
    def __init__(self):
        self.data = electric_data
        self.client = mqtt.Client()
        print("Servidor MQTT listo")

    def on_connect_server(self, client, userdata, flags, rc): 
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

        print("conectado a los topicos ", MQTT_TOPICS)
    

    def on_connect_cliente(self, client, userdata, flags, rc): 
        print("Connected with result code " + str(rc)) 
        MQTT_TOPICS = [ ("/test", 0),
                        ("/config/f_sampl", 0),
                        ("/config/t_muest", 0)]

        client.subscribe(MQTT_TOPICS)
        client.message_callback_add("/config/f_sampl", config_fsam)
        client.message_callback_add("/config/t_muest", config_tmuest)
        client.message_callback_add("/test", on_message_test)

        client.subscribe("/test")
        client.subscribe("/config/f_sampl")
        client.subscribe("/config/t_muest")

    def config_fsam(self, client, userdata, msg):
        pass

    def config_tmuest(self, client, userdata, msg):
        pass

    def on_message_test(self, client, userdata, msg): 
        print("Mensaje recibido: " + str(msg.payload))


    def on_message_server(self, client, userdata, msg): 
        print(msg.topic + " " + str(msg.payload)) 


    def on_message_tension(self, client, userdata, msg):
        print("msj atencion")
        try:
            valor = float(msg.payload)
            self.data.vec_tension.append()
            print(str(valor) + " [V]")
            cont = cont + 1
                    
        except ValueError:
            print("Fin de vector")
            flag_v = True
            cont = 0
 

    def on_message_corriente(self, client, userdata, msg):
        try:
            valor = float(msg.payload)
            self.data.vec_corriente.append()
            print(str(valor) + " [A]")
            cont = cont + 1      

        except ValueError:
            print("Fin de vector")
            flag_i = True
            cont = 0 

    def on_message_f_sampl(self, client, userdata, msg):
        electric_data.load_fs(float(msg.payload))

    def on_message_t_muest(self, client, userdata, msg):
        electric_data.load_tm(float(msg.payload))

    def connect_server(self, ip, puerto, tiempo):
        self.client.on_connect = self.on_connect_server 
        self.client.on_message = self.on_message_server
        self.client.connect(ip, puerto, tiempo)
        self.client.loop_start()
        return self.client

    def connect_cliente(self, ip, puerto, tiempo):
        self = mqtt.Client() 
        self.on_connect = on_connect_cliente 
        self.on_message = on_message
        self.connect(ip, puerto, tiempo)
        self.loop_start()
        return self
