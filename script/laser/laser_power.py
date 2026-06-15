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

# Programme principal
if __name__ == "__main__":

    # laser intensity as a function of time
    t = M(np.linspace(0,10,21),0)
    I = M([45.1,44.9,44.7,44.6,44.5,44.4,44.3,44.3,35.8,34.9,34.2,33.6,33.2,32.6,32.1,31.6,31.3,31,30.7,30.2,29.7])

    # transmission efficiency measure
    I_tot = np.array([60.8,60.4,60.5,60.4,60.5,60.3,60.3,60.1])
    I_trans = np.array([6.94,7.01,6.99,6.97,6.91,6.88,6.91,6.86])
    ratio = I_trans/I_tot
    avg_ratio = np.mean(ratio)
    sigma_ratio = np.sqrt(np.mean(ratio**2)-avg_ratio**2)/np.sqrt(len(ratio))
    #print(avg_ratio, sigma_ratio)

    #
    filename = '/Users/nathanleretif/StageLPL/data/laser_intensity_14h59_15d06.csv'
    data = np.genfromtxt(filename,skip_header=23,delimiter=',')
    t, I = data[:,0]*10**-3/60, data[:,1]*10**3
    Is, N = np.copy(I), len(I)
    smooth_L = 50
    for k in range(1,N+1) : 
        deltak = np.min([smooth_L//2, k, N-k])
        if deltak>0 : Is[k] = np.mean(I[k-deltak:k+deltak])
    avg_pow = np.mean(I)
    std = np.sqrt(np.mean(I**2)-avg_pow**2)
    print(avg_pow, std)


    # Plotting initialisation
    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    # Plotting
    #M.errorbar(ax,t,I,ls='--',color='C0',marker='.')
    ax.plot(t,Is)
    ax.set_xlabel("temps (min)")
    ax.set_ylabel("Intensité (mW)")
    #ax.set_aspect('equal')
    ax.grid(True)

    plt.tight_layout()
    plt.show()