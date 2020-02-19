import time
import paho.mqtt.client as mqtt
from electric_data import electric_data

class mqtt_obj():
    def __init__(self):
        cont = 0
        vec_tension = []
        vec_corriente = []
        flag_v = False
        flag_i = False

    def connect_server(self, ip, puerto, tiempo):
        self = mqtt.Client() 
        self.on_connect = on_connect 
        self.on_message = on_message 
        self.connect(ip, puerto, tiempo)
        self.client.loop_start()  

    def connect_cliente(self, ip, puerto, tiempo):
        self = mqtt.Client() 
        self.on_connect = on_connect_cliente 
        self.on_message = on_message 
        self.connect(ip, puerto, tiempo)
        self.client.loop_start()  

    # Setup callback functions that are called when MQTT events happen like 
    # connecting to the server or receiving data from a subscribed feed. 
    def on_connect(self, client, userdata, flags, rc): 
        print("Connected with result code " + str(rc)) 
        # Subscribing in on_connect() means that if we lose the connection and 
        # reconnect then subscriptions will be renewed. 
        client.subscribe("/led")
        client.subscribe("/test")
        client.subscribe("/medicion/tension")
        client.subscribe("/medicion/corriente")
        client.subscribe("/medicion/f_sampl")
        client.subscribe("/medicion/t_muest")
        client.message_callback_add("/medicion/tension", on_message_tension)
        client.message_callback_add("/medicion/corriente", on_message_corriente)
        client.message_callback_add("/medicion/f_sampl", on_message_f_sampl)
        client.message_callback_add("/medicion/t_muest", on_message_t_muest)
    
    def on_connect_cliente(self, client, userdata, flags, rc): 
        print("Connected with result code " + str(rc)) 

        client.subscribe("/test")
        client.subscribe("/config")


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
        if float(msg.payload) is "999":
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
