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





# Programme principal
if __name__ == "__main__":

    display_amp = np.linspace(-18,12,16) # dBm, Delta = 0
    mesured_amp = array([-41.4,-34.6,-32.3,-30.2,-28.1,-25.6,-23.6,-21.6,-19.6,-17.6,-15.8,-13.9,-13,-12.7,-12.5,-12.5]) # dBm, Delta = .2
    incoming_amp = display_amp - 2.7 # Delta = .3
    amplified_amp = mesured_amp + 39.5 # Delta = 1
    gain = amplified_amp - incoming_amp # Delta = 1
    mean_gain = np.mean(gain[1:11])

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot()

    ax.errorbar(incoming_amp,amplified_amp,xerr=.3/sqrt(3),yerr=1/sqrt(3),label='signal amplifié',ls='')
    ax.errorbar(incoming_amp,gain,xerr=.3/sqrt(3),yerr=1/sqrt(3),label='gain',ls='',color='C1')
    ax.hlines(mean_gain,1.05*np.min(incoming_amp),1.05*np.max(incoming_amp),label=f'gain typique = {mean_gain} dB',ls='--',color='C1')

    ax.legend()
    ax.set_xlabel("amplitude du signal d'entré (dBm)")
    ax.set_ylabel('amplitude/gain (dBm/dB)')
    ax.set_aspect('equal')

    plt.grid(True)
    plt.show()