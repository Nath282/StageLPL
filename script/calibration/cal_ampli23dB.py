#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from numpy import array, sqrt
from Measurement import Measure as M

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

# Programme principal
if __name__ == "__main__":

    disp_pow = M(np.linspace(-18,12,16),unit='dBm')
    mes_pow = M([-41.4,-34.6,-32.3,-30.2,-28.1,-25.6,-23.6,-21.6,-19.6,-17.6,-15.8,-13.9,-13,-12.7,-12.5,-12.5],.3,unit='dBm')
    rf_corr = M(-2.65,.02,unc_type='unchanged')
    attenuator = M(40,.5)
    inc_pow = disp_pow + rf_corr
    amp_pow = mes_pow + attenuator
    gain = amp_pow-inc_pow
    typ_gain = gain[1:11].mean()
    
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot()

    M.errorbar(ax, inc_pow, amp_pow, label='amplified signal', ls=':')
    M.errorbar(ax, inc_pow, gain, label='gain', ls='')
    ax.set_xlim()
    ax.set_ylim()
    M.hlines(ax, typ_gain, -30, 30, label=f'gain typique = {typ_gain} dB',ls='--',color='C1')

    ax.legend()
    ax.set_xlabel("amplitude du signal d'entré (dBm)")
    ax.set_ylabel('amplitude/gain (dBm/dB)')
    #ax.set_aspect('equal')

    plt.grid(True)
    plt.show()