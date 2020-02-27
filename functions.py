import random
import math
import numpy
import datetime

from scipy import signal

#from matplotlib import pyplot as plt

'''
to do
Funcion de calculo de potencias
Funcion de calculo de THD
'''


class funciones:
    def __init__ (self):
        pass

    def find_zero(self, vec, nz):
        """Recibe el vector (vec) y el numero de cero a encontrar (nz) y devuelve el indice del numero inmediato anterior al cero.
        Cuenta cada "cero" cada vez que pasa desde negativo a positivo"""
        zf = 0
        for j in range(len(vec)):
            #print(str(j) + " " + str(vec[j]))
            if vec[j] < 0 and vec[j+1] > 0:
                zf = zf + 1
            if zf >= nz:
                return j

    def get_cosfi(self):
        iv = self.find_zero(self.v, 1)
        ii = self.find_zero(self.i, 1)

        return self.index2cosfi(ii, iv)

    def index2cosfi (self, iv, ii):
        td = (iv - ii) * self.ts

        cosfi = math.cos(self.t2rad(td, self.freq))
        
        return cosfi

    def t2rad (self, t, f):
        """Convierte el tiempo recibido a radianes, de la frecuencia recivida"""
        phi = t * math.pi * 2 * f
        
        return phi

    def get_freq(self, vec, ts):
        index1 = self.find_zero(vec, 1)
        index2 = self.find_zero(vec, 2)

        T = (index2 - index1) * ts
        return 1/T

    def ins2eff(self, vec):
        vec2 = 0
        for j in range(len(vec)):
            vec2 = vec2 + math.pow(vec[j],2)
        
        vec2 = vec2 / len(vec)
        vec2 = math.sqrt(vec2)

        return vec2

    def generate_signal(self, arm_div = None, arm_freq = None):
        '''Si se especifica arm_div y arm_freq se crearan armonicos usando
        div como divisor de amplitud y freq como multiplicador de frecuencia'''
        self.t = [0] * self.tfin              #Tiempo
        self.v = [0] * self.tfin              #Tension
        self.i = [0] * self.tfin              #Corriente    

        for j in range(self.tfin):
                n = 0.0 * random.random()
                self.t[j] = self.ts * j
                self.v[j] = self.av * math.sin(2*math.pi*self.freq_dat*self.t[j]) + n * self.av
                self.i[j] = self.ai * math.sin(2*math.pi*self.freq_dat*self.t[j] + self.phi) + n * self.ai

        if arm_div is not None or arm_freq is not None:
            for j in range(self.tfin):
                for k in range(len(arm_div)):
                    #Los armonicos solo aparecen en corriente, no en tension
                    #self.v[j] = self.v[j] + self.av / arm_div[k] * math.sin(2*math.pi*self.freq*self.t[j] * arm_freq[k])
                    self.i[j] = self.i[j] + self.ai / arm_div[k] * math.sin(2*math.pi*self.freq_dat*self.t[j] * arm_freq[k] + self.phi)

    def power_calc(self):
        for j in range(len(self.v)):
            self.ps[j] = self.v[j] * self.i[j] / 1000
            self.pq[j] = self.v[j] * self.i[j] * math.sin(self.phi) / 1000
            self.pp[j] = self.v[j] * self.i[j] * math.cos(self.phi) / 1000
            #print(str(j) + " " + str(self.pp[j]) + " " + str(self.ps[j]) + " " + str(self.pq[j]))

    def init_vect(self):
        #print("tm: " + str(self.tm) + "   ts: " + str(self.ts) + "   tfin: " + str(self.tfin) )
        
        self.tfin = math.ceil(self.tm / self.ts)

        self.t = [0] * self.tfin              #Vector de tiempo
        self.pp = [0] * self.tfin             #Vector de Potencia Activa
        self.ps = [0] * self.tfin             #Vector de Potencia Aparente
        self.pq = [0] * self.tfin             #Vector de Potencia Reactiva


    def fourier_data(self, vec = None):
        '''Si se recibe un vector se calcula todo en funcion al vector recibido.
        Si no se recibe, se calcula fourier de los vectores tension y corriente'''

        if vec is None:
            self.V = abs(numpy.fft.rfft(self.v))
            self.I = abs(numpy.fft.rfft(self.i))

            self.V = self.V / len(self.V)
            self.I = self.I / len(self.I)

            self.f = [0] * len(self.V)              #Frecuencias
            self.fp = self.fs / (2 * len(self.f))

            for j in range(len(self.f)):
                self.f[j] = self.fp * j

        else:
            res = abs(numpy.fft.rfft(vec))
            res = res / len(res)
            
            self.f = [0] * len(vec)                 #Frecuencias
            self.fp = self.fs / (2 * len(self.f))

            for j in range(len(self.f)):
                self.f[j] = self.fp * j

            return vec


    def find_armonics(self, vec):
        '''Encuentra los mayores componenetes armonicos'''
        ref = max(vec) / 100
        #print(ref)

        for j in range(len(self.f) - 2):
            if vec[j] < vec[j+1] > vec[j+2] and vec[j+1] > ref:
                self.magA.append(vec[j+1])
                self.freA.append((j+1) * self.fp)

    def THD_cal(self, vec = None):
        '''Calcula el THD del vector recibido y si no se recibe ningun vector calcula sobre magA'''
        if vec is None:
            num = 0
            for j in range(1,len(self.magA)):
                num = num + math.pow(self.magA[j], 2)
            
            self.THD = (math.pow(num, 0.5) / self.magA[0]) * 100

            #self.THD = (num / self.magA[0]) * 100

        else:
            num = 0
            for j in range(1,len(vec)):
                num = num + vec[j]
            
            self.THD = (num / vec[0]) * 100

    def PF_cal(self, vec = None):
        '''Calculo del power factor de la senal'''
        self.powfac = self.cosfi / math.pow(1 + math.pow(self.THD/100,2), 0.5)

    def printdata (self):
        #print("\tCoeficientes de b \t\t",self.b)
        #print("\tCoeficientes de a \t\t",self.a)
        print("\tTension eficaz \t\t", float("{0:.2f}".format(self.ins2eff(self.v) )))
        print("\tTension maxima \t\t", float("{0:.2f}".format(self.v[self.v.index(max(self.v))] )))
        print("\tCorriente eficaz \t", float("{0:.2f}".format(self.ins2eff(self.i))))
        print("\tCorriente maxima \t", float("{0:.2f}".format(self.i[self.i.index(max(self.i))] )))
        print("\tFrecuencia \t\t", float("{0:.1f}".format(self.freq)))
        print("\tCoseno fi \t\t", float("{0:.2f}".format(self.cosfi)))
        #print("\tAmplitud armonicos \t\t", self.magA)
        #print("\tFrecuenc armonicos \t\t", self.freA)
        #print("\tTHD \t\t\t" + str(float("{0:.2f}".format(self.THD)) + "%"))
        print("\tPower Factor \t\t", float("{0:.2f}".format((self.powfac))))
        

    def design_filter(self, tipo, ripple_BP, frec_corte, sb_att, orden=None, plot=None):
        '''
        Devuelve los coeficientes del filtro especificado
        tipo: "C1" chevy1, "C2" chevy2 o "B" butter, si no se especifica usa butter por defecto
        orden: Orden del filtro
        ripple_BP: Ripple permitido en la banda de paso
        frec_corte: vector con las frecuencias de corte y paso
        '''

        if orden is None:
            if tipo == 'C1':
                orden = signal.cheb1ord(frec_corte[0], frec_corte[1], ripple_BP, sb_att)
                self.b, self.a = signal.cheby1(orden[0], ripple_BP, orden[1], 'low')

                w, n  = signal.freqz(self.b, self.a)
                
                for j in range(len(n)):
                    n[j] = 10 * math.log10(abs(n[j]))
                    w[j] = w[j] * 2000 / 3.14151 

            elif tipo == 'C2':
                orden = signal.cheb2ord(frec_corte[0], frec_corte[1], ripple_BP, sb_att)
                self.b, self.a = signal.cheby2(orden[0], ripple_BP, orden[1], 'low')
            
            elif tipo == 'B':
                orden = signal.buttord(frec_corte[0], frec_corte[1], ripple_BP, sb_att)
                self.b, self.a = signal.butter(orden[0], orden[1], 'low')

            else:
                orden = signal.buttord(frec_corte[0], frec_corte[1], ripple_BP, sb_att)
                self.b, self.a = signal.butter(orden[0],  orden[1], 'low')


        else:
            if tipo == 'C1':
                self.b, self.a = signal.cheby1(orden, ripple_BP, frec_corte, 'low')

            elif tipo == 'C2':
                self.b, self.a = signal.cheby2(orden, ripple_BP, frec_corte, 'low')

            else:
                self.b, self.a = signal.butter(orden, ripple_BP, frec_corte, 'low')


    def filtrado(self, vec):
        self.filt = signal.lfilter(self.b, self.a, vec)

        vecf = abs(numpy.fft.rfft(vec))
        vecf = vecf / len(vecf)

        filtf = abs(numpy.fft.rfft(self.filt))
        filtf = filtf / len(filtf)


    def get_hora(self):
        return str(datetime.datetime.now())[:19]
