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
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5


# Programme principal
if __name__ == "__main__":

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])
    
    #f1,f2,f3,f4,f5 = 'double_pass/FDEm2.DP.csv','double_pass/FDE.DP.csv', 'diffraction_efficiency/2Wm2.FDE.csv', 'diffraction_efficiency/2W.FDE.csv', 'diffraction_efficiency/2Wbis.FDE.csv'


    """# Single pass data 
    rootpath, ext = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/', '.FDE.csv'
    files = {'2W':'single pass squared 16/06', '2Wbis':None, '2Wm2':'single pass squared 19/06'}
    colorsp = {'2W':7, '2Wbis':7, '2Wm2':8}
    for filename in files.keys() :
        ds = DataSet.read_file(rootpath+filename+ext)
        freq, diff_eff, opt_pow = ds['RF displayed frequency'], (ds['Diffracted intensity']/ds.metadata['Parameters']['laser intensity'])**2*100, ds['Optimum displayed diffraction power']
        color = colors[colorsp[filename]]
        M.errorbar(ax1, freq, diff_eff, label=files[filename], color=color, marker='D', ls='')
        M.errorbar(ax2, freq, opt_pow, label=files[filename], color=color, marker='s', ls='')"""

    # Double pass data
    rootpath, ext = '/Users/nathanleretif/StageLPL/data/double_pass/', '.csv'
    files = {'FDEm2.SP':'aprem', 'FDEm3.DP':''}
    #colordp = {'FDE':2, 'FDEm2':3, 'FDEm3':4}
    for filename in files.keys() : 
        ds = DataSet.read_file(rootpath+filename+ext)
        try : 
            freq, I_diff, I_laser = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['laser intensity']
            if filename in ['FDE.SP','FDEm2.SP'] : 
                diff_eff = (I_diff/I_laser)**2*100
                
            else : 
                diff_eff = I_diff/I_laser*100
        except KeyError : 
            freq, I_diff= ds['RF displayed frequency'], ds['Diffracted intensity']
            I_laser = ds.metadata['Parameters']['laser intensity']
            diff_eff = I_diff/I_laser*100
        #color = colors[colordp[filename]]
        M.errorbar(ax, freq, diff_eff, label=filename, ls='', marker='s')

    

    ax.set_xlim()
    ax.set_ylim()
    ax.fill_betweenx([-100,200],428-25,428+25,label='AOM labeled bandwidth', color='grey',alpha=.4)
    ax.vlines(428,ymin=-100,ymax=200,label='428MHz',color='black',ls='--')
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Double pass diffraction efficiency")
    ax.legend()
    ax.grid(True)



    plt.tight_layout()
    plt.show()
