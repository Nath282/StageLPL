#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure, DataSet
from Measurement import Measure as M


# Programme principal
if __name__ == "__main__":

    
    #f1,f2,f3,f4,f5 = 'double_pass/FDEm2.DP.csv','double_pass/FDE.DP.csv', 'diffraction_efficiency/2Wm2.FDE.csv', 'diffraction_efficiency/2W.FDE.csv', 'diffraction_efficiency/2Wbis.FDE.csv'

    fig1, fig2 = plt.figure(figsize=(8,6)), plt.figure(figsize=(8,6))
    gs1, gs2 = fig1.add_gridspec(1,1), fig2.add_gridspec(1,1)
    ax1, ax2 = fig1.add_subplot(gs1[0]), fig2.add_subplot(gs2[0])

    # Double pass data
    rootpath, ext = '/Users/nathanleretif/StageLPL/data/double_pass/', '.DP.csv'
    files = {'FDE':'24/06 16h49', 'FDEm2':'24/06 17h06', 'FDEm3':'10/07 17h25'}
    for filename in files.keys() : 
        ds = DataSet.read_file(rootpath+filename+ext)
        try : 
            freq, I_diff, opt_pow, I_laser = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['Optimum displayed diffraction power'], ds['laser intensity']
            diff_eff = I_diff/I_laser*100
        except KeyError : 
            freq, I_diff, opt_pow = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['Optimum displayed diffraction power']
            I_laser = ds.metadata['Parameters']['laser intensity']
            diff_eff = I_diff/I_laser*100
        M.errorbar(ax1, freq, diff_eff, label='double pass '+files[filename], ls='', marker='s', color='C3')
        M.errorbar(ax2, freq, opt_pow, label=files[filename], ls='', marker='s')

    # Single pass data 
    rootpath, ext = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/', '.FDE.csv'
    files = {'2W':'single pass squared 16/06', '2Wbis':None, '2Wm2':'single pass squared 19/06'}
    colors = {'2W':'C4', '2Wbis':'C4', '2Wm2':'C5'}
    for filename in files.keys() :
        ds = DataSet.read_file(rootpath+filename+ext)
        freq, diff_eff, opt_pow = ds['RF displayed frequency'], (ds['Diffracted intensity']/ds.metadata['Parameters']['laser intensity'])**2*100, ds['Optimum displayed diffraction power']
        M.errorbar(ax1, freq, diff_eff, label=files[filename], color='C0', marker='D', ls='')
        M.errorbar(ax2, freq, opt_pow, label=files[filename], color=colors[filename], marker='s', ls='')

    ax1.set_xlim()
    ax1.set_ylim()
    ax1.fill_betweenx([-100,200],428-25,428+25,label='AOM labeled bandwidth', color='grey',alpha=.4)
    ax1.vlines(428,ymin=-100,ymax=200,label='428MHz',color='black',ls='--')
    ax1.set_xlabel("Frequency (MHz)")
    ax1.set_ylabel("Double pass diffraction efficiency")
    ax1.legend()
    ax1.grid(True)

    ax2.set_xlim()
    ax2.set_ylim()
    ax2.vlines(428,ymin=-20,ymax=0,label='428MHz',color='black',ls='--')
    ax2.set_xlabel("Frequency (MHz)")
    ax2.set_ylabel("Optimum RF power (dBm)")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
