#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure as M


# Programme principal
if __name__ == "__main__":

    filename = '/Users/nathanleretif/PythonProjects/StageLPL/diffraction_efficiency/data_diff_intensity_amp2W.csv'
    data = np.genfromtxt(filename,delimiter=',',skip_header=21)
    inc_pow = M(data[:,0],Delta=.1) - 1.4 + M(40.9,.2)
    diff_I = M(data[:,1],Delta=.1)
    inc_laser_I = M(69.5,.7)
    diff_eff = diff_I/inc_laser_I
    k = np.argmax(diff_eff.value)
    print(diff_eff[k])

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    M.errorbar(ax, inc_pow, diff_eff, ls='--',marker='.')
    ax.set_xlabel("incoming RF power (dBm)")
    ax.set_ylabel("diffraction efficiency (%)")
    ax.grid(True)

    secax = ax.secondary_xaxis('top',functions=(lambda x:x+1.4-40.9, lambda x:x-1.4+40.9))
    secax.set_xlabel("displayed RF power (dBm)")

    fig.tight_layout()
    fig.savefig('/Users/nathanleretif/Library/Mobile Documents/com~apple~CloudDocs/Administratif/ENSL/L3-Physique_25:26/StageLPL/data/eff_diffraction=f(rf_power)/eff_diff_ampli.png')

    plt.show()