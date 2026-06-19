#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure, DataSet


# Programme principal
if __name__ == "__main__":

    rootpath = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/'
    ext = '.FDE.csv'
    filenames = ['2W','2Wbis','2Wm2']

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    fig2 = plt.figure(figsize=(8,6))
    gs2 = fig2.add_gridspec(1,1)
    ax2 = fig2.add_subplot(gs2[0])

    for filename in filenames : 
        ds = DataSet.read_file(rootpath+filename+ext)
        params = ds.metadata['Parameters']
        Freq, diff_eff, opt_pow = ds['RF displayed frequency(Mhz)'], ds['Diffracted intensity (mW)']/params['laser intensity'], ds['Optimum displayed diffraction power(dBm)']
        Measure.errorbar(ax, Freq, diff_eff, label=filename, ls='--', marker='.')
        Measure.errorbar(ax2, Freq, opt_pow,label=filename, ls='--', marker='.')

    ax.set_xlabel("Frequency (Mhz)")
    ax.set_ylabel("Diffraction efficiency (%)")
    ax.legend()
    ax.grid(True)

    ax2.set_xlabel("Frequency (Mhz)")
    ax2.set_ylabel("Optimum Diffraction power (dBm)")
    ax2.legend()
    ax2.grid(True)

    # Mesure efficacité 428Mhz Type B : 
    i = np.array([34.1,34.0,33.8,33.6,33.8,33.7,33.1,33.1,32.9,32.9])
    laser = np.array([39.4,39.7,38.7,38.4,38.6,38.9,38.7,38.3,39,37.8])
    print(f"max efficiency ={Measure(i/laser,type='a')}")

    fig.savefig('/Users/nathanleretif/StageLPL/figures/fig2W.FDE.png')
    plt.show()