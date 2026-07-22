#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Affichage de la courbe d'efficacité de diffraction pour l'ampli 23dB
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure, DataSet


# Programme principal
if __name__ == "__main__":

    rootpath = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/'
    filename = '23dB'
    ext = '.ADE.csv'

    ds = DataSet.read_file(rootpath+filename+ext)
    params = ds.metadata['Parameters']
    rf_corr = params['Marconi correction'] + params['ampli gain']
    inc_pow, diff_eff = ds['RF displayed signal power(dBm)'] + rf_corr, ds['Diffracted intensity (mW)'] / params['laser intensity']
    print(diff_eff.max()*100)

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    Measure.errorbar(ax,inc_pow,diff_eff,ls='--',marker='.')
    ax.set_xlabel("Incoming RF power (dBm)")
    ax.set_ylabel("Diffraction efficiency (%)")
    ax.grid(True)
    #ax.set_title('ampli23dB')

    secax = ax.secondary_xaxis('top',functions=(lambda x:x-rf_corr[0].value, lambda x:x+rf_corr[0].value))
    secax.set_xlabel('displayed RF power (dBm)')

    plt.tight_layout()
    plt.show()
