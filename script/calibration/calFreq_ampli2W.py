#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure as M
from Measurement import DataSet


# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

if __name__=='__main__' :
    rootpath = '/Users/nathanleretif/StageLPL/data/calibration/'
    files = {'ampli2W.FreqCal.csv':'15h37','ampli2Wm2.FreqCal.csv':'16h19'}

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    for filename in files.keys() :
        ds = DataSet.read_file(rootpath+filename,section_delimiters=('--','--,'))
        params = ds.metadata['Parameters']
        freq, mes_power = ds['RF frequency'], ds['RF power']
        rf_pow = mes_power + params['attenuation']
        M.errorbar(ax, freq, rf_pow, label=files[filename], ls='',marker='s')

    ax.set_ylim()
    ax.set_xlim()
    ax.vlines(428,10,40,ls='--',color='black',label='428MHz')
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("RF signal power (dBm)")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()
