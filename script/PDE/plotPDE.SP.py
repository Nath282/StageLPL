#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import numpy as np
from Measurement import Measure, DataSet
from Plotting import Axes

# Programme principal
if __name__ == "__main__":

    ax = Axes()
    rootpath, ext = '/Users/nathanleretif/StageLPL/data/PDE/', '.csv'
    files = {'23dB.SP':'ampli 23dB', '2W.SP2':"ampli 2W"} # {filename : label}

    for filename in files.keys() : 
        ds = DataSet.read_file(rootpath+filename+ext)
        params = ds.metadata['Parameters']
        if filename == '23dB.SP' :
            rf_corr = params['Marconi correction'] + params['ampli gain']
        else : 
            rf_corr = params['RF_correction']
        inc_pow, diff_eff = ds['RF displayed signal power'] + rf_corr, ds['Diffracted intensity'] / params['laser intensity']
        Measure.errorbar(ax,inc_pow,diff_eff,ls='',marker='s',label=files[filename])
        print(f"max diffraction efficiency for {filename} : {diff_eff.max()*100} at {inc_pow[np.argmax(diff_eff)]}")

    ax.set_lims()
    ax.vlines(29.6,-1,2,colors='black',linestyles='--',label="AOM specified optimum power (29.63dBm)")
    ax.set_xlabel("incoming RF power (dBm)")
    ax.set_ylabel("diffraction efficiency (%)")
    secax = ax.secondary_xaxis('top',functions=(lambda x:x+1.4-40.9, lambda x:x-1.4+40.9))
    secax.set_xlabel("displayed RF power (dBm)")

    ax.save('PDE.SP')
    Axes.show()
