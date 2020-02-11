import random
import math
import numpy

from scipy import signal

from matplotlib import pyplot as plt

def design_filter(self, tipo, ripple_BP, frec_corte, orden=None):
        '''Devuelve los coeficientes del filtro especificado
        tipo: "C1" chevy1, "C2" chevy2 o "B" butter, si no se especifica usa butter por defecto
        orden: Orden del filtro
        ripple_BP: Ripple permitido en la banda de paso
        frec_corte: vector con las frecuencias de corte y paso
        '''
        if orden is None:
            if tipo == 'C1':
                orden = signal.cheb1ord(frec_corte[0], frec_corte[1], ripple_BP, 60)
                #b, a = signal.cheby1(orden, ripple_BP, frec_corte, 'low')
                self.b, self.a = signal.cheby1(orden[0], ripple_BP, orden[1], 'low')
                print(self.a, self.b)

            elif tipo == 'C2':
                orden = signal.cheb2ord(frec_corte[0], frec_corte[1], ripple_BP, 60)
                self.b, self.a = signal.cheby2(orden, ripple_BP, frec_corte, 'low')

            else:
                orden = signal.butord(frec_corte[0], frec_corte[1], ripple_BP, 60)
                self.b, self.a = signal.butter(orden, ripple_BP, frec_corte, 'low')


        else:
            if tipo == 'C1':
                self.b, self.a = signal.cheby1(orden, ripple_BP, frec_corte, 'low')

            elif tipo == 'C2':
                self.b, self.a = signal.cheby2(orden, ripple_BP, frec_corte, 'low')

            else:
                self.b, self.a = signal.butter(orden, ripple_BP, frec_corte, 'low')
