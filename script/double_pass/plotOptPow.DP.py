#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import DataSet
from Measurement import Measure as M

# Paramètres globaux d'affichage
import matplotlib as mpl
import matplotlib.colors as cl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

if __name__ == "__main__": 

    # Plotting initialisation
    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    # File extracting : 
    # Files extracting
    dir, ext = '/Users/nathanleretif/StageLPL/data/FDE/', '.csv'
    files = ['SP1', 'SP2', 'DP1', 'DP2', 'DP3']


    # Colormap setup :
    cmin, cmax = 0,len(files)
    cm = plt.get_cmap('magma')
    cnorm = cl.Normalize(vmin=cmin,vmax=cmax)
    colors = {x : cm(cnorm(x)) for x in range(cmin,cmax)}

    # Data extraction : 
    for filename, color in zip(files,colors.values()) :
        ds = DataSet.read_file(dir+filename+ext)
        freq, opt_pow = ds['RF displayed frequency'], ds['Optimum displayed diffraction power']
        M.errorbar(ax, freq, opt_pow, label=filename, color=color, ls='', marker='s')

    ax.set_xlabel("RF frequency (MHz)")
    ax.set_ylabel("Optimum displayed RF power (dBm)")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()

