#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import numpy as np
from Measurement import Measure as M
from Measurement import DataSet 
from Plotting import Axes

# Programme principal
if __name__ == "__main__":

    # Files extracting
    dir, ext = '/Users/nathanleretif/StageLPL/data/FDE/', '.csv'
    filename = 'SP2'  # ['SP1', 'SP2', 'SP3', 'SP4', 'DP1', 'DP2', 'DP3']
    
    ax = Axes()
    ds = DataSet.read_file(dir+filename+ext)
    freq, I_diff = ds['RF displayed frequency'], ds['Diffracted intensity']
    I_laser = ds['laser intensity']
    diff_eff = (I_diff/I_laser)*100
    M.errorbar(ax, freq, diff_eff, color='C1', label='data', ls='', marker='s')

    ax.set_lims()
    ax.fill_betweenx([-100,200],428-25,428+25,label='AOM specified bandwidth (50MHz)', color='grey',alpha=.2)
    ax.vlines(428,ymin=-100,ymax=200,label='AOM specified frequency (428MHz)',color='black',ls='--')
    ax.set_labels("Frequency (MHz)","Max Diffraction efficiency (%)")

    ax.save('FDE.SP')
    Axes.show()


    """
    # Mesure efficacité 428Mhz Type B : 
    i = np.array([34.1,34.0,33.8,33.6,33.8,33.7,33.1,33.1,32.9,32.9])
    laser = np.array([39.4,39.7,38.7,38.4,38.6,38.9,38.7,38.3,39,37.8])
    print(f"max efficiency ={M(i/laser,unc_type='a')}")
"""
    


    
    
    