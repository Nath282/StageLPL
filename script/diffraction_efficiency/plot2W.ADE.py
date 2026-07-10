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
    files = {'2W.ADE.csv':"ampli 2W 15/06", '23dB.ADE.csv':'ampli 23dB', '2Wm2.ADE.csv':"ampli 2W 16/06"} # {filename : label}

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    for filename in files.keys() : 
        ds = DataSet.read_file(rootpath+filename)
        params = ds.metadata['Parameters']
        if filename == '23dB.ADE.csv' :
            rf_corr = params['Marconi correction'] + params['ampli gain']
        else : 
            rf_corr = params['RF_correction']
        inc_pow, diff_eff = ds['RF displayed signal power(dBm)'] + rf_corr, ds['Diffracted intensity (mW)'] / params['laser intensity']
        Measure.errorbar(ax,inc_pow,diff_eff,ls='--',marker='.',label=files[filename])
        print(f"max diffraction efficiency for {filename} : {diff_eff.max()*100} at {inc_pow[np.argmax(diff_eff)]}")
        if filename == '2Wm2.ADE.csv' :
            _diff_eff, _inc_pow = diff_eff, inc_pow

    
    ax.set_ylim()
    ax.set_xlim()
    idmax = np.argmax(_diff_eff)
    max_eff = _diff_eff[idmax]
    id = np.argmin(np.abs(_diff_eff-max_eff/np.sqrt(2)))
    ax.fill_betweenx([-1,2],x1=_inc_pow[id],x2=2*_inc_pow[np.argmax(_diff_eff)]-_inc_pow[id],alpha=.2,label='bandwidth',color='C2')
    ax.vlines(29.6,-1,2,colors='black',linestyles='--',label="theoritical optimum power")

    ax.set_xlabel("incoming RF power (dBm)")
    ax.set_ylabel("diffraction efficiency (%)")
    ax.legend()
    ax.grid(True)

    secax = ax.secondary_xaxis('top',functions=(lambda x:x+1.4-40.9, lambda x:x-1.4+40.9))
    secax.set_xlabel("displayed RF power (dBm)")

    fig.savefig('/Users/nathanleretif/StageLPL/figures/fig2W.ADE.png')
    plt.tight_layout()
    plt.show()