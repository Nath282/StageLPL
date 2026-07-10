#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from numpy import array, sqrt
from scipy.optimize import curve_fit
from Measurement import Measure

# Programme principal
if __name__ == "__main__":

    disp_pow = Measure(np.linspace(2,13,12),.1,'unchanged')
    corr_pow = disp_pow - 2.7
    mes_pow = Measure([-40.3, -38.5,-36.5,-34,-31.3,-28.4,-25.2,-21.9,-18.5,-14.6,-10,-6.9],.3)
    amp_pow = mes_pow + Measure(39.5,.6)

    disp_pow2 = Measure(np.linspace(11,13,11),.1)
    corr_pow2 = disp_pow2 - 2.7
    mes_pow2 = Measure([-16.2,-15.4,-14.5,-13.6,-12.6,-11.8,-10.6,-9.7,-8.9,-8.2,-7.7],.3)
    amp_pow2 = mes_pow2 + Measure(39.5,.6)

    disp_pow3 = Measure(np.linspace(11,13,5),.1)
    corr_pow3 = disp_pow3 - 2.7
    mes_pow3 = Measure([-18.5,-15.7,-13.3,-11.2,-9.5],.3)
    amp_pow3 = mes_pow3 + Measure(39.5,.6)
    amp_pow4 = Measure([-15.8,-13.4,-11.3,-9.5,-8.1], .3) + Measure(39.5,.6)
    amp_pow5 = Measure([-14.9,-12.6,-10.6,-9,-7.7], .3) + Measure(39.5,.6)
    amp_pow6 = Measure([-14.9,-12.6,-10.7,-9,-7.8],.3) + Measure(39.5,.6)



    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot()
    ls = '--'
    errors = True
    Measure.errorbar(ax,disp_pow,amp_pow,ls=ls,label='data1', errors=errors)
    Measure.errorbar(ax, disp_pow2,amp_pow2, ls=ls, label='data12h', errors=errors)
    Measure.errorbar(ax, disp_pow3,amp_pow3, ls=ls, label='data13h55', errors=errors)
    Measure.errorbar(ax, disp_pow3,amp_pow4, ls=ls, label='data15h16', errors=errors)
    Measure.errorbar(ax, disp_pow3,amp_pow5, ls=ls, label='data16h45', errors=errors)
    Measure.errorbar(ax, disp_pow3,amp_pow6, ls=ls, label='data2', errors=errors)
    secax = ax.secondary_xaxis('top', functions=(lambda x:x-2.7,lambda x:x+2.7))
    
    ax.set_xlabel("amplitude affichée de la source (dBm)")
    secax.set_xlabel("amplitude en sortie de la source (dBm)")
    ax.set_ylabel("amplitude du signal sortant de l'ampli (dBm)")
    ax.legend()
    ax.grid(True)
    

    plt.show()