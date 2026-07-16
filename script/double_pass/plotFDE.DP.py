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

# Colormap setup :
cmin, cmax = 0,10
cm = plt.get_cmap('magma')
cnorm = cl.Normalize(vmin=cmin,vmax=cmax)
colors = {x : cm(cnorm(x)) for x in range(cmin,cmax+1)}

# Programme principal
if __name__ == "__main__":

    
    #f1,f2,f3,f4,f5 = 'double_pass/FDEm2.DP.csv','double_pass/FDE.DP.csv', 'diffraction_efficiency/2Wm2.FDE.csv', 'diffraction_efficiency/2W.FDE.csv', 'diffraction_efficiency/2Wbis.FDE.csv'

    fig1, fig2 = plt.figure(figsize=(8,6)), plt.figure(figsize=(8,6))
    gs1, gs2 = fig1.add_gridspec(1,1), fig2.add_gridspec(1,1)
    ax1, ax2 = fig1.add_subplot(gs1[0]), fig2.add_subplot(gs2[0])

    # Single pass data 
    rootpath, ext = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/', '.FDE.csv'
    files = {'2W':'single pass squared 16/06', '2Wbis':None, '2Wm2':'single pass squared 19/06'}
    colorsp = {'2W':7, '2Wbis':7, '2Wm2':8}
    for filename in files.keys() :
        ds = DataSet.read_file(rootpath+filename+ext)
        freq, diff_eff, opt_pow = ds['RF displayed frequency'], (ds['Diffracted intensity']/ds.metadata['Parameters']['laser intensity'])**2*100, ds['Optimum displayed diffraction power']
        color = colors[colorsp[filename]]
        M.errorbar(ax1, freq, diff_eff, label=files[filename], color=color, marker='D', ls='')
        M.errorbar(ax2, freq, opt_pow, label=files[filename], color=color, marker='s', ls='')

    # Double pass data
    rootpath, ext = '/Users/nathanleretif/StageLPL/data/double_pass/', '.DP.csv'
    files = {'FDE':'24/06 16h49', 'FDEm2':'24/06 17h06', 'FDEm3':'10/07 17h25'}
    colordp = {'FDE':2, 'FDEm2':3, 'FDEm3':4}
    for filename in files.keys() : 
        ds = DataSet.read_file(rootpath+filename+ext)
        try : 
            freq, I_diff, opt_pow, I_laser = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['Optimum displayed diffraction power'], ds['laser intensity']
            diff_eff = I_diff/I_laser*100
        except KeyError : 
            freq, I_diff, opt_pow = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['Optimum displayed diffraction power']
            I_laser = ds.metadata['Parameters']['laser intensity']
            diff_eff = I_diff/I_laser*100
        color = colors[colordp[filename]]
        M.errorbar(ax1, freq, diff_eff, label='double pass '+files[filename], ls='', marker='s', color=color)
        M.errorbar(ax2, freq, opt_pow, label=files[filename], ls='', marker='s',color=color)

    

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
