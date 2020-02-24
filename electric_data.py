import math
from functions import funciones
from scipy import signal


#from mqtt_functions import mqtt_obj
#from matplotlib import pyplot as plt


class electric_data(funciones):
    def __init__(self, ts, tm, av, ai, freq, phi):
        self.ts = ts
        self.tm = tm
        self.tfin = math.ceil(tm / ts)
        self.av = av
        self.ai = ai
        self.phi = phi

        self.v = []                             #Vector de tension
        self.i = []                             #Vector de corriente
        self.t = []                             #Vector de tiempo

        self.pp = [0] * self.tfin               #Potencia activa
        self.pq = [0] * self.tfin               #Potencia reactiva
        self.ps = [0] * self.tfin               #Potencia aparente
        
        self.maxv_indx = 0                      #Indice de tension maxima
        self.maxi_indx = 0                      #Indice de corriente maxia
        self.cosfi = 0                          #Coseno fi
        self.powfac = 0                         #Factor de potencia
        self.freq = 0                           #Frecuencia medida
        self.freq_dat = freq                    #Frecuencia para generador

        self.V = [0]                            #Vector de tensiones fourier
        self.I = [0]                            #Vector de corriente fourier
        self.f = [0]                            #Vector de frecuencias fourier
        self.fp = 0                             #Frecuencia de paso del vector
        self.fs = 1/ts                          #Frecuencia de muestreo

        self.magA = []                          #Magnitud de Armonicos
        self.freA = []                          #Frecuencia de Armonicos
        self.THD = 0                            #THD de senal

        self.a = []                             #Componentes del filtro
        self.b = []                             #Componentes del filtro
        self.filt = []                          #Senal Filtrada
    
    def __init__(self, ts, tm):
        self.ts = ts
        self.tm = tm
        self.tfin = math.ceil(tm / ts)

    def gen_data(self, arm_div = None, arm_freq = None):  
        if arm_div is not None and arm_freq is not None:
            self.generate_signal(arm_div, arm_freq)
        
        else:
            self.generate_signal()

    def load_data(self, vector_v, vector_i):
        self.v = vector_v                       #Vector de tension
        self.i = vector_i                       #Vector de corriente


    #Carga de frecuencia de muestreo
    def load_fs(self, f_samp):
        self.fs = f_samp

        #Calculo el tiempo final
        if self.ts is not 0 and self.tm is not 0:
            self.tfin = math.ceil(self.tm / self.ts)


    #Carga de tiempo de muestreo
    def load_tm(self, t_muest):
        self.tm = t_muest

        #Calculo el tiempo final
        if self.ts is not 0 and self.tm is not 0:
            self.tfin = math.ceil(self.tm / self.ts)


    def analize(self):  
        self.fourier_data()                     #Calculo de Fourier

        self.design_filter('C1', 1, [100*self.ts, 200*self.ts], 60)
        self.filtrado(self.i)
        
        self.power_calc()                               #Calculo de potencias
        self.freq = self.get_freq(self.i, self.ts)      #Calculo de frecuencia
        self.cosfi = self.get_cosfi()                   #Calculo de coseno fi
        self.find_armonics(self.I)                      #Cargado de vector de armonicos
        self.THD_cal()                                  #Calculo THD
        self.PF_cal()                                   #Calculo del power factor


    def show_data(self):
        self.plot_data()

