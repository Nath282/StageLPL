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
import math 

def round_inc (x) :
    # fonction d'arrondi au supérieur au premier chiffre significatif
    if x == 0 : 
        return 0.0
    else : 
        odg = int(np.log10(x))
        return int(1+x*10**-odg)*10**odg


# Programme principal
if __name__ == "__main__":

    display_power = array([-16,-14,-12,-10,-8,-7,-6,-5,-4,-3,-2,0,2,4,6,8,10]) # dBm, u=0
    inc_power, u_inc_power = display_power - 2.7, .1
    mes_power, u_mes_power = array([-44,-41,-38.5,-35.8,-30.4,-25,-18,-13.6,-9.2,-7.3,-5.6,-3.7,-2.3,-1.8,-1.7,-1.9,-2.2]), .1
    ampli_power, u_ampli_power = mes_power + 39.5, sqrt(u_mes_power**2 + .6**2)
    gain, u_gain = ampli_power - inc_power, sqrt(u_ampli_power**2 + u_inc_power**2)
    
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot()

    ax.errorbar(inc_power,ampli_power,xerr=round_inc(u_inc_power),yerr=round_inc(u_ampli_power),label='signal amplifié',ls='',color='C0')
    ax.errorbar(inc_power,gain,xerr=round_inc(u_inc_power),yerr=round_inc(u_gain),label='gain',ls='',color='C1')

    ax.legend()
    ax.set_xlabel("amplitude du signal d'entré (dBm)")
    ax.set_ylabel('amplitude/gain (dBm/dB)')
    #ax.set_aspect('equal')
    #ax.set_box_aspect(1)
    ax.grid(True)
    fig.savefig('/Users/nathanleretif/Library/Mobile Documents/com~apple~CloudDocs/Administratif/ENSL/L3-Physique_25:26/StageLPL/data/cal_ampli1W.png')
    
    fig1 = plt.figure(figsize=(8,6))
    ax1 = fig1.add_subplot()
    ax1.plot(display_power, ampli_power)
    ax1.set_xlabel('displayed incoming power')
    ax1.set_ylabel('signal power after amplification')
    ax1.set_title('Puissance nécessaire pour 1.3W après amplification')
    ax1.hlines(31,-16,10,linestyles='--')
    ax1.grid(True)

    plt.show()