import serial
import re
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpl_patches


def insere_legendas(temp_min, temp_media, temp_max):
    #Create the legend without superposing the data in the plot :D

    # create a list with two empty handles (or more if needed)
    handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)] * 3

    # create the corresponding number of labels (= the text you want to display)
    labels = []
    labels.append("máx =  %.2f ºC" %temp_max)
    labels.append("média = %.2f ºC" %temp_media)
    labels.append("mín = %.2f ºC" %temp_min)

    # create the legend, supressing the blank space of the empty line symbol and the
    # padding between symbol and label by setting handlelenght and handletextpad
    plt.legend(handles, labels, loc='best', fontsize='small', fancybox=True, framealpha=0.7, handlelength=0, handletextpad=0)


s = serial.Serial('COM3', 9600)

temperature = list()

x_vals = []

plt.style.use('dark_background')
index = count()


def animate(i):

    #obtém o valor da temperatura do quarto
    res = s.read(3)
    temperature.append((110/1023)*int(res.decode('utf-8')))
    x_vals.append(next(index))
    
    #resolve o bug do primeiro valor em aproximadamente 26 graus
    if i==0:
        temperature.clear()
        x_vals.clear()

    if i>0:
        temp_min = min(temperature)
        temp_max = max(temperature)
        temp_media = sum(temperature)/len(temperature)
        plt.cla()
        plt.title('Temperatura do quarto x tempo')
        plt.xlabel("Tempo (s)")
        plt.ylabel("Temperatura (ºC)")
        insere_legendas(temp_min, temp_media, temp_max)
        plt.plot(x_vals, temperature)

       
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)

plt.tight_layout()
plt.show()