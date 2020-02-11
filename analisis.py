import sqlobject as SO

from electric_data import electric_data
from mqtt_functions import on_connect
from mqtt_functions import on_message

import paho.mqtt.client as mqtt
from scipy.signal import blackman
from scipy.fftpack import fft

# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running 
# this script and the MQTT server. 
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 
client.connect('localhost', 1883, 60) 

# Connect to the MQTT server and process messages in a background thread. 
client.loop_start() 


tm = 2                      #Tiempo de muestreo
fs = 20000                  #Frecuencia de muestreo
ts = 1/fs                   #Periodo de muestreo

av = 311                    #Amplitud de tension
ai = 2.4                    #Amplitud de corriente
freq = 50                   #Frecuencia de la senal
tc = 1/freq                 #Tiempo de ciclo
phi = 0.471

div_arm = [20, 30, 40, 50, 60, 70, 80]
mul_fre = [3, 5, 7, 9, 11, 13, 15]

datos = electric_data(ts, tm, av, ai, freq, phi)
datos.gen_data(div_arm, mul_fre)
#datos.gen_data()
datos.analize()
datos.printdata()
#datos.show_data()


