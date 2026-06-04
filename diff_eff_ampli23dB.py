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
    # /!\ soulève une erreur si une des valeurs est nulle
    odg = np.floor(np.log10(x))
    return np.floor(1+x*10**-odg)*10**odg


# Programme principal
if __name__ == "__main__":

    display_amp = np.linspace(-16,2,10) # dBm, u = 0
    amp, u_amp = display_amp - 2.7 + 24.3, .3 # dBm
    amp_mW = 10**(amp/10)
    u_amp_mW = .3 * 10/amp * 10**(amp/10)
    I, u_I = array([.97,1.36,1.99,2.97,4.48,6.77,10,15,21.4,29.1]), .1 # mW
    I_laser, u_I_laser = 77.3, 1 # mW
    eff = I/I_laser*100
    u_eff = round_inc(eff*sqrt( (.001/I)**2 + (.5/58.8)**2 ))
    

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,2)
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    ax1.errorbar(amp,eff,xerr=.3,yerr=u_eff,ls='',marker='o',markersize=5)
    ax1.set_xlabel("amplitude du signal en entrée de l'AOM (dBm)")
    ax1.set_ylabel("efficacité de diffraction (%)")
    ax1.grid(True)

    ax2.errorbar(amp_mW,eff,xerr=u_amp_mW,yerr=u_eff,ls='',marker='o',markersize=5)
    ax2.set_xlabel("amplitude du signal en entrée de l'AOM (mW)")
    ax2.set_ylabel("efficacité de diffraction (%)")
    ax2.grid(True)

    fig.tight_layout()
    fig.savefig('/Users/nathanleretif/Library/Mobile Documents/com~apple~CloudDocs/Administratif/ENSL/L3-Physique_25:26/StageLPL/data/eff_diffraction=f(rf_power)/eff_diff_ampli.png')

    plt.show()