#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
from Measurement import Measure, DataSet

# Programme principal
if __name__ == "__main__":

    rootpath = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/'
    ext = '.ADE.csv'
    filenames = ['2W','2Wm2','23dB']

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    for filename in filenames : 
        ds = DataSet.read_file(rootpath+filename+ext)
        params = ds.metadata['Parameters']
        inc_pow, diff_eff = ds['RF displayed signal power(dBm)'] + params['RF_correction'], ds[' Diffracted intensity (mW)'] / params['laser intensity']
        Measure.errorbar(ax,inc_pow,diff_eff,ls='--',marker='.',label=filename)
        print(f"max diffraction efficiency for {filename} : {diff_eff.max()*100}")
    
    ax.set_xlabel("incoming RF power (dBm)")
    ax.set_ylabel("diffraction efficiency (%)")
    ax.legend()
    ax.grid(True)

    secax = ax.secondary_xaxis('top',functions=(lambda x:x+1.4-40.9, lambda x:x-1.4+40.9))
    secax.set_xlabel("displayed RF power (dBm)")

    fig.savefig('/Users/nathanleretif/StageLPL/figures/fig2W.ADE.png')
    plt.tight_layout()
    plt.show()