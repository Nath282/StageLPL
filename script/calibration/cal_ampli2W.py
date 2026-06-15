#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure as M

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

def data_treatment (disp_pow, mes_pow) :
    inc_pow = disp_pow + M(-1.4,Delta=.1)
    out_pow = mes_pow + M(39.5,.3)
    gain = out_pow - inc_pow
    return inc_pow, out_pow, gain

# Programme principal
if __name__ == "__main__":

    d1 = M(np.linspace(-40,-2,20))
    m1 = M([-40.3,-38.2,-36,-34,-31.9,-29.9,-28,-25.9,-23.9,-22,-19.9,-17.9,-16,-14,-12,-10,-8.1,-6.3,-4.6,-3.2],Delta=.01) #11h12
    inc1,out1,gain1 = data_treatment(d1, m1)
    avg_gain = np.mean(gain1.value[:17])
    std_gain = np.sqrt(np.mean(gain1.value[:17]**2)-avg_gain**2)
    sigma_gain = np.sqrt(np.sum(gain1.sigma[:17]**2))
    print(avg_gain)
    print(std_gain,sigma_gain)

    d2 = M(np.linspace(-8,0,9))
    m2 = M([-8.4,-7.5,-6.6,-5.9,-5.2,-4.7,-4.2,-3.9,-3.6],Delta=.1)
    inc2,out2,gain2 = data_treatment(d2, m2)



    # Plotting initialisation
    plot_gain = True 
    fig = plt.figure(figsize=(8,6))
    if plot_gain :  
        gs = fig.add_gridspec(2,1)
        ax = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
    else : 
        gs = fig.add_gridspec(1,1)
        ax = fig.add_subplot(gs[0])

    # Plotting
    M.errorbar(ax,inc1,out1,ls='--',color='C0',label='amp signal 11h12',marker='.')
    M.errorbar(ax,inc2,out2,ls='--',color='C1',label='amp signal 11h39',marker='.')
    
    ax.set_xlabel("incoming power (dBm)")
    ax.set_ylabel("amplified signal power (dBm)")
    ax.legend()
    #ax.set_aspect('equal')
    ax.grid(True)

    secax = ax.secondary_xaxis('top',functions=(lambda x:x+1.4, lambda x:x-1.4))
    secax.set_xlabel('source displayed power')

    if plot_gain : 
        M.errorbar(ax2,inc1,gain1, ls='',color='C0', label='11h12')
        M.errorbar(ax2,inc2,gain2, ls='',color='C1', label='11h39')
        ax2.set_xlabel("incoming power (dBm)")
        ax2.set_ylabel("gain (dB)")
        ax2.legend()
        #ax.set_aspect('equal')
        ax2.grid(True)

    plt.tight_layout()
    plt.show()