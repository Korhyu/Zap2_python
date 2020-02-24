import time
import paho.mqtt.client as mqtt
from electric_data import electric_data

class mqtt_obj():
    def __init__(self):
        pass

    def on_connect(self, client, userdata, flags, rc): 
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
    

    def on_connect_cliente(self, client, userdata, flags, rc): 
        print("Connected with result code " + str(rc)) 

        client.subscribe("/test")
        client.subscribe("/config/f_sampl")
        client.subscribe("/config/t_muest")

    def on_message_test(self, client, userdata, msg): 
        print("Mensaje recibido: " + str(msg.payload))

    # The callback for when a PUBLISH message is received from the server. 
    def on_message(self, client, userdata, msg): 
        print(msg.topic + " " + str(msg.payload)) 

    def on_message_tension(self, client, userdata, msg):
        if float(msg.payload) is 9999:
            self.flag_v = True
            self.cont = 0

            if self.flag_v and self.flag_i is True:
                self.flag_v = False
                self.flag_i = False
                datos = electric_data(self.vec_tension, self.vec_corriente)

        else:
            self.vec_tension.append(float(msg.payload))
            self.cont = self.cont + 1
 

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

    def connect_server(self, ip, puerto, tiempo):
        self = mqtt.Client() 
        self.on_connect = self.on_connect 
        self.on_message = self.on_message 
        self.connect(ip, puerto, tiempo)
        self.loop_start()
        return self

    def connect_cliente(self, ip, puerto, tiempo):
        self = mqtt.Client() 
        self.on_connect = on_connect_cliente 
        self.on_message = on_message 
        self.connect(ip, puerto, tiempo)
        self.loop_start()
        return self
