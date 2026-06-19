#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure as M
from pathlib import Path

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

if __name__=='__main__' :

    rootPath = Path('/Users/nathanleretif/StageLPL/data/calibration')
    filenames = ['ampli2W','ampli2Wm2']
    ext = '.FreqCal.csv'

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    for filename in filenames : 
        metadata,data,_ = M.read_csv(rootPath/(filename+ext),sections=['Time','Parameters'])
        param = metadata['Parameters']

        freq = M(data[:,0])
        rf_corr = M(param['rf_corr'],param['u_rf_corr'])
        rf_pow = M(data[:,1],.2) + rf_corr

        M.errorbar(ax,freq,rf_pow,ls='--',marker='.',label=metadata['Time']['Start of Measurement'])
    ax.set_xlabel("RF frequency (Mhz)")
    ax.set_ylabel("RF power (dBm)")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()
