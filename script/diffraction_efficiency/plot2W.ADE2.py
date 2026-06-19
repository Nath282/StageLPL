#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
from Measurement import Measure, DataSet

if __name__=='__main__' : 

    rootpath = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/'
    filenames = ['2W.ADE2.csv','2W.ADE.csv']

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    for filename in filenames : 
        ds = DataSet.read_file(rootpath+filename)
        params = ds.metadata['Parameters']
        disp_pow, diff_eff = ds['RF displayed signal power(dBm)'], ds[' Diffracted intensity (mW)'] / params['laser intensity']
        Measure.errorbar(ax,disp_pow,diff_eff,ls='--',marker='.',label=filename)
        print(f"max diffraction efficiency for {filename} : {diff_eff.max()*100}")

    ax.set_xlabel('Displayed RF power (dBm)')
    ax.set_ylabel('2nd order diffraction efficiency (%)')
    ax.grid(True)
    ax.legend()

    fig.savefig('/Users/nathanleretif/StageLPL/figures/fig2W.ADE2+1.png')
    plt.show()