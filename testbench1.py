#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on ...

@author: ...

Descripción:
------------

Este testbench sigue con el ejemplo del "testbench0" pero agrega algunas funcionalidades
como la posibilidad de ejecutarlo a través de la consola, haciendo algún parseo de argumentos.

"""

# Ejemplificaremos el uso de las herramientas que utilizaremoos frecuentemente 

# Importación de módulos que utilizaremos en nuesto testbench:
# Una vez invocadas estas funciones, podremos utilizar los módulos a través del identificador que indicamos luego de "as". 
# Por ejemplo np.linspace() -> función linspace dentro e NumPy
import numpy as np
#import scipy.signal as sig
import matplotlib as mpl
# la siguiente línea solo afecta en caso que lo quisiéramos correr desde la línea de comandos
mpl.use('Qt5Agg')

import matplotlib.pyplot as plt
import pdsmodulos as pds


###################################
## Formas de incluir comentarios ##
###################################

# Comentarios con "#"

""" Bloques de comentario
    bla bla bla
    bla ...
"""

#%% Separación de bloques de código para ordenar tu trabajo "#%%"

#%%  Inicialización

#%%  Generación de señales de prueba

#%%  Presentación de resultados


#%%  Inicialización de librerías

# Setup inline graphics
mpl.rcParams['figure.figsize'] = (10,10)

#%%  Testbench: creamos una función que no recibe argumentos para asegurar que siempre encontraremos nuestro espacio de variables limpio.
# Prestar atención al indentado, ya que Python interpreta en función del indentado !!

def my_testbench( sig_type ):
    
    # Datos generales de la simulación
    fs = 1000.0 # frecuencia de muestreo (Hz)
    N = 1000   # cantidad de muestras
    
    ts = 1/fs # tiempo de muestreo
    df = fs/N # resolución espectral
    
    # grilla de sampleo temporal
    tt = np.linspace(0, (N-1)*ts, N).flatten()
    
    # grilla de sampleo frecuencial
    ff = np.linspace(0, (N-1)*df, N).flatten()

    # Concatenación de matrices:
    # guardaremos las señales creadas al ir poblando la siguiente matriz vacía
    x = np.array([], dtype=np.float).reshape(N,0)
    ii = 0
    
    # estructuras de control de flujo
    if sig_type['tipo'] == 'senoidal':
    
        
        # calculo cada senoidal de acuerdo a sus parámetros
        for this_freq in sig_type['frecuencia']:
            # prestar atención que las tuplas dentro de los diccionarios también pueden direccionarse mediante "ii"
            aux = sig_type['amplitud'][ii] * np.sin( 2*np.pi*this_freq*tt + sig_type['fase'][ii] )
            # para concatenar horizontalmente es necesario cuidar que tengan iguales FILAS
            x = np.hstack([x, aux.reshape(N,1)] )
            ii += 1
    
    elif sig_type['tipo'] == 'ruido':
        
        # calculo cada señal de ruido incorrelado (blanco), Gausiano de acuerdo a sus parámetros
        # de varianza
        for this_var in sig_type['varianza']:
            aux = np.sqrt(this_var) * np.random.randn(N,1)
            # para concatenar horizontalmente es necesario cuidar que tengan iguales FILAS
            x = np.hstack([x, aux] )
        
        # Podemos agregar algún dato extra a la descripción de forma programática
        # {0:.3f} significa 0: primer argunmento de format
        # .3f formato flotante, con 3 decimales
        # $ ... $ indicamos que incluiremos sintaxis LaTex: $\hat{{\sigma}}^2$
        sig_props['descripcion'] = [ sig_props['descripcion'][ii] + ' - $\hat{{\sigma}}^2$ :{0:.3f}'.format( np.var(x[:,ii]))  for ii in range(0,len(sig_props['descripcion'])) ]
    
    else:
        
        print("Tipo de señal no implementado.")        
        return
        
    #%% Presentación gráfica de los resultados
    
    plt.figure(1)
    line_hdls = plt.plot(tt, x)
    plt.title('Señal: ' + sig_type['tipo'] )
    plt.xlabel('tiempo [segundos]')
    plt.ylabel('Amplitud [V]')
    #    plt.grid(which='both', axis='both')
    
    # presentar una leyenda para cada tipo de señal
    axes_hdl = plt.gca()
    
    # este tipo de sintaxis es *MUY* de Python
    axes_hdl.legend(line_hdls, sig_type['descripcion'], loc='upper right'  )
    
    plt.show()


#%% Comienzo de nuestro script
    ##########################
    
import argparse as ap

parser = ap.ArgumentParser(description='Ejemplo de testbench utilizado en la materia Procesamiento Digital de Señales.')
parser.add_argument( 'signal_type', 
                     metavar='tipo_de_señal', 
                     choices=['senoidal', 'ruido'], 
                     default='senoidal', 
                     type=str, 
                     help='Identificador de la señal a generar')


args = parser.parse_args()
        
# Uso de diferentes tipos de datos en Python            

if args.signal_type == 'senoidal':
    
    ## tipo de variable diccionario. Puedo crearlo iniciándolo mediante CONSTANTES
    sig_props = { 'tipo': 'senoidal', 
                  'frecuencia': (3, 10, 20), # Uso de tuplas para las frecuencias 
                  'amplitud':   (1, 1,  1),
                  'fase':       (0, 0,  0)
                 } 
    # Como también puedo agregar un campo descripción de manera programática
    # este tipo de sintaxis es *MUY* de Python
    sig_props['descripcion'] = [ str(a_freq) + ' Hz' for a_freq in sig_props['frecuencia'] ]


elif args.signal_type == 'ruido':
    

    # Usar CTRL+1 para comentar o descomentar el bloque de abajo.
    sig_props = { 'tipo': 'ruido', 
                  'varianza': (1, 1, 1) # Uso de tuplas para las frecuencias 
                 } 
    sig_props['descripcion'] = [ '$\sigma^2$ = ' + str(a_var) for a_var in sig_props['varianza'] ]

else:

    print("Tipo de señal no implementado.")        
    exit(1)
    
# Invocamos a nuestro testbench exclusivamente: 
my_testbench( sig_props )
exit(0)
    

