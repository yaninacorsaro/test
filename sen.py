import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sp


def mi_funcion_sen( vmax , dc , ff , ph, nn , fs ):
     
    tt = np.linspace( start= 0, stop= (nn-1)/fs ,num = nn)
    xx = vmax*np.sin(tt*2*np.pi*ff+ph) + dc
    return tt, xx

def mi_funcion_sawtooth( vmax , dc , ff , ph, nn , fs ):
     
    tt = np.linspace( start= 0, stop= (nn-1)/fs ,num = nn)
    xx = vmax*sp.sawtooth(tt*2*np.pi*ff+ph) + dc
    return tt, xx

'''
# test
tt, xx = mi_funcion_sen( vmax = 2 , dc = 0 , ff = 1 , ph = 0, nn = 1000 , fs=100 )
fig, ax = plt.subplots()
ax.plot(tt, xx)
ax.set(xlabel='time (s)', ylabel='voltage (V)',title='sen function')
ax.grid()
plt.show()


tt, xx = mi_funcion_sawtooth( vmax = 2 , dc = 0 , ff = 1 , ph = 0, nn = 1000 , fs=100 )
fig, ax = plt.subplots()
ax.plot(tt, xx)
ax.set(xlabel='time (s)', ylabel='voltage (V)',title='sawtooth function')
ax.grid()
plt.show()
'''