"""
23/03/2021
Medidor de temperatura do quarto utilizando Arduino UNO e LM35

Autores:  Victor Cordeiro de Arruda 
          Lucas Cordeiro de Arruda

"""

import serial
import re
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpl_patches
from datetime import datetime

def tempo_s_ms():
    curr_time = datetime.now()
    return curr_time.second + curr_time.microsecond/1000000

def insere_legendas(temp_min, temp_media, temp_max, temp_actual):
    #Create the legend without superposing the data in the plot :D

    # create a list with two empty handles (or more if needed)
    handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)] * 4

    # create the corresponding number of labels (= the text you want to display)
    labels = []
    labels.append("máx =  %.2f ºC" %temp_max)
    labels.append("média = %.2f ºC" %temp_media)
    labels.append("mín = %.2f ºC" %temp_min)
    labels.append("atual = %.2f ºC" %temp_actual)
    
    # create the legend, supressing the blank space of the empty line symbol and the
    # padding between symbol and label by setting handlelenght and handletextpad
    plt.legend(handles, labels, loc='best', fontsize='small', fancybox=True, framealpha=0.7, handlelength=0, handletextpad=0)


def animate(i):
    #obtém o valor da temperatura do quarto
    res = s.read(3)
    temperature.append((110/1023)*int(res.decode('utf-8')))
    
    #resolve o bug do primeiro valor em aproximadamente 26 graus
    if i==0:
        temperature.clear()
        x_vals.clear()
        plt.cla()
        
        #define o valor de início da aquisição de temperatura
        global start_time
        start_time = datetime.now()
        
        
    if i>0:
        temp_min = min(temperature)
        temp_max = max(temperature)
        temp_media = sum(temperature)/len(temperature)
        temp_atual = temperature[-1]
        plt.cla()
        plt.title('Temperatura x tempo (Início: %s)' %start_time.strftime("%Y-%m-%d %H:%M:%S"))
        plt.xlabel("Tempo (min)")
        plt.ylabel("Temperatura (ºC)")
        insere_legendas(temp_min, temp_media, temp_max, temp_atual)

        #calcula o tempo decorrido e converte para minutos
        tempo_agora = datetime.now()
        time_delta = tempo_agora - start_time
        total_seconds = time_delta.total_seconds()
        total_minutes = total_seconds/60
        x_vals.append(total_minutes)

        #plota os valores obtidos
        plt.plot(x_vals, temperature)
        

s = serial.Serial('COM3', 9600)

temperature = list()

x_vals = []
x_min = []

plt.style.use('dark_background')
index = count()

ani = FuncAnimation(plt.gcf(), animate, interval = 100)

plt.tight_layout()
plt.show()