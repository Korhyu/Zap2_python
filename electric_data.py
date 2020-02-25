import math
from functions import funciones
from scipy import signal


class electric_data(funciones):

    ts = 0
    tm = 0
    tfin = 0
    av = 0
    ai = 0
    phi = 0

    v = []                             #Vector de tension
    i = []                             #Vector de corriente
    t = []                             #Vector de tiempo

    flagV = False                      #Flag auxiliar de Tension
    flagI = False                      #Flag auxiliar de Corriente

    pp = [0]                           #Potencia activa
    pq = [0]                           #Potencia reactiva
    ps = [0]                           #Potencia aparente
    
    maxv_indx = 0                      #Indice de tension maxima
    maxi_indx = 0                      #Indice de corriente maxia
    cosfi = 0                          #Coseno fi
    powfac = 0                         #Factor de potencia
    freq = 0                           #Frecuencia medida
    freq_dat = 0                       #Frecuencia para generador

    V = []                             #Vector de tensiones fourier
    I = []                             #Vector de corriente fourier
    f = []                             #Vector de frecuencias fourier
    fp = 0                             #Frecuencia de paso del vector
    fs = 0                             #Frecuencia de muestreo

    magA = []                          #Magnitud de Armonicos
    freA = []                          #Frecuencia de Armonicos
    THD = 0                            #THD de senal

    a = []                             #Componentes del filtro
    b = []                             #Componentes del filtro
    filt = []                          #Senal Filtrada


    def __init__(self):
        pass

    def __init__(self, ts, tm, av, ai, freq, phi):
        self.ts = ts
        self.tm = tm
        self.tfin = math.ceil(tm / ts)
        self.av = av
        self.ai = ai
        self.phi = phi

        self.v = [] * self.tfin                 #Vector de tension
        self.i = [] * self.tfin                 #Vector de corriente
        self.t = [] * self.tfin                 #Vector de tiempo

        self.flagV = False                      #Flag auxiliar de Tension
        self.flagI = False                      #Flag auxiliar de Corriente

        self.pp = [0] * self.tfin               #Potencia activa
        self.pq = [0] * self.tfin               #Potencia reactiva
        self.ps = [0] * self.tfin               #Potencia aparente
        
        self.freq_dat = freq                    #Frecuencia para generador

        self.fs = 1/ts                          #Frecuencia de muestreo

    
    def __init__(self, ts, tm):
        self.ts = ts
        self.tm = tm
        self.tfin = math.ceil(tm / ts)

    def load_time(self, ts, tm):
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

    def load_voltage(self, vector_v):
        self.v = vector_v                       #Vector de tension

    def load_current(self, vector_i):
        self.i = vector_i                       #Vector de corriente

    def print_data(self):
        for j in range(len(self.v)):
            print(str(j) + "   " + str(self.v[j]) + "   " + str(self.i[j]))

    #Carga de frecuencia de muestreo
    def load_fs(self, f_samp):
        self.fs = f_samp

        #Calculo el tiempo final
        if self.ts is not 0 and self.tm is not 0:
            self.tfin = math.ceil(self.tm / self.ts)
            print("Tfin: " + str(self.tfin))
            self.ps = [0] * self.tfin
            self.pq = [0] * self.tfin
            self.pp = [0] * self.tfin


    #Carga de tiempo de muestreo
    def load_tm(self, t_muest):
        self.tm = t_muest

        #Calculo el tiempo final
        if self.ts is not 0 and self.tm is not 0:
            self.tfin = math.ceil(self.tm / self.ts)
            self.ps = [0] * self.tfin
            self.pq = [0] * self.tfin
            self.pp = [0] * self.tfin


    def analize(self):  
        self.fourier_data()                     #Calculo de Fourier

        self.flagI = False
        self.flagV = False

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

