#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure as M
from Measurement import DataSet 

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

def format_data(ds : DataSet) :
    params = ds.metadata['Parameters']
    Freq, diff_eff, opt_pow = ds['RF displayed frequency'], ds['Diffracted intensity']/params['laser intensity']*100, ds['Optimum displayed diffraction power']
    return Freq, diff_eff, opt_pow

# Programme principal
if __name__ == "__main__":

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    # Files extracting
    dir, ext = '/Users/nathanleretif/StageLPL/data/FDE/', '.csv'
    files = ['SP2', 'SP3', 'SP4']  # ['SP1', 'SP2', 'SP3', 'SP4', 'DP1', 'DP2', 'DP3']

    # Colormap setup :
    import matplotlib.colors as cl
    cmin, cmax = 0,len(files)
    cm = plt.get_cmap('magma')
    cnorm = cl.Normalize(vmin=cmin,vmax=cmax)
    colors = [cm(cnorm(x)) for x in range(cmin,cmax)]

    for filename,c in zip(files,colors): 
        ds = DataSet.read_file(dir+filename+ext)
        freq, I_diff = ds['RF displayed frequency'], ds['Diffracted intensity']
        try : 
            I_laser = ds['laser intensity']
        except KeyError : 
            I_laser = ds.metadata['Parameters']['laser intensity']
        diff_eff = (I_diff/I_laser)*100
        x_max = freq[diff_eff.argmax()].value
        #freq -= x_max-428
        M.errorbar(ax, freq, diff_eff, color=c, label=filename, ls='', marker='s',errors=True)

    ax.set_xlim()
    ax.set_ylim()
    ax.fill_betweenx([-100,200],428-25,428+25,label='AOM labeled bandwidth', color='grey',alpha=.4)
    ax.vlines(428,ymin=-100,ymax=200,label='428MHz',color='black',ls='--')
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Max Diffraction efficiency (%)")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()


    """
    # Mesure efficacité 428Mhz Type B : 
    i = np.array([34.1,34.0,33.8,33.6,33.8,33.7,33.1,33.1,32.9,32.9])
    laser = np.array([39.4,39.7,38.7,38.4,38.6,38.9,38.7,38.3,39,37.8])
    print(f"max efficiency ={M(i/laser,unc_type='a')}")
"""
    


    
    
    