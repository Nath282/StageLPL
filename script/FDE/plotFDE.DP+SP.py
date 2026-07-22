#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import numpy as np
from Measurement import DataSet
from Measurement import Measure as M
from Plotting import Axes

# Programme principal
if __name__ == "__main__":

    ax = Axes()
    # Files extracting
    dir, ext = '/Users/nathanleretif/StageLPL/data/FDE/', '.csv'
    files = ['SP3', 'DP1', 'DP2', 'DP3']  # ['SP1', 'SP2', 'SP3', 'SP4', 'DP1', 'DP2', 'DP3'] 

    # Colormap setup :
    colors = Axes.colormap(0,8)

    # Plotting kwargs :
    files = {'SP3' : {'label':'single pass squared', 'color':colors[1], 'ls':''},
             #'DP1' : {'label':'double pass 1', 'color':colors[4], 'ls':''},
             #'DP2' : {'label':'double pass 2', 'color':colors[5], 'ls':''},
             'DP3' : {'label':'double pass 3', 'color':colors[6], 'ls':''}
             }
    
    for filename,kwargs in files.items() : 
        ds = DataSet.read_file(dir+filename+ext)
        freq, diff_eff = ds['RF displayed frequency'], ds['Diffracted intensity']/ds['laser intensity']
        x_max = freq[diff_eff.argmax()].value
        if filename[0:2] == 'SP' : 
            diff_eff = diff_eff**2*100
            freq -= x_max-428+10
        else :
            freq -= x_max-428
            diff_eff = diff_eff*100
        print( kwargs['label'] + f', max = {diff_eff.max()} %')
        M.errorbar(ax, freq, diff_eff, marker='s', **kwargs)

    ax.set_lims()
    ax.fill_betweenx([-100,200],428-25,428+25,label='AOM specified bandwidth (50MHz)', color='grey',alpha=.2)
    ax.vlines(428,ymin=-100,ymax=200,label='AOM specified frequency (428MHz)',color='black',ls=':')
    ax.set_labels("Recentered Frequency (MHz)","Max Diffraction efficiency (%)")

    ax.save('FDE.DP+SP')
    Axes.show()
