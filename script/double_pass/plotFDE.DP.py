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
import os

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5


# Programme principal
if __name__ == "__main__":

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    # Files extracting
    dir, ext = '/Users/nathanleretif/StageLPL/data/FDE/', '.csv'
    files = ['SP3', 'DP1', 'DP2', 'DP3']  # ['SP1', 'SP2', 'SP3', 'SP4', 'DP1', 'DP2', 'DP3']

    # Colormap setup :
    import matplotlib.colors as cl
    cmin, cmax = 0,8
    cm = plt.get_cmap('magma')
    cnorm = cl.Normalize(vmin=cmin,vmax=cmax)
    value = [1,4,5,6]
    colors = [cm(cnorm(x)) for x in value]

    # Plotting kwargs :
    files = {'SP3' : {'label':'single pass squared', 'color':cm(cnorm(1)), 'ls':'--'},
             'DP1' : {'label':'double pass 1', 'color':cm(cnorm(4)), 'ls':''},
             'DP2' : {'label':'double pass 2', 'color':cm(cnorm(5)), 'ls':''},
             'DP3' : {'label':'double pass 3', 'color':cm(cnorm(6)), 'ls':''}
             }

    for filename,kwargs in files.items() : 
        ds = DataSet.read_file(dir+filename+ext)
        freq, I_diff = ds['RF displayed frequency'], ds['Diffracted intensity']
        try : 
            I_laser = ds['laser intensity']
        except KeyError : 
            I_laser = ds.metadata['Parameters']['laser intensity']

        diff_eff = I_diff/I_laser
        x_max = freq[diff_eff.argmax()].value
        if filename == 'SP3' :     
            freq -= x_max-428+10
        else : 
            freq -= x_max-428
        perm = np.argsort(freq)
        freq = freq[perm]
        diff_eff = diff_eff[perm]

        if filename[0:2] == 'SP' :
            diff_eff = diff_eff**2*100
        else : 
            diff_eff = diff_eff*100

        kwargs['label'] = kwargs['label'] + f', max = {diff_eff.max()} %'

        M.errorbar(ax, freq, diff_eff, errors=True, marker='s', **kwargs)

        """f = lambda x,a,b,c : a*x**2 + b*x + c
        idmax = diff_eff.argmax()
        bw = 3
        args = M.curve_fit(f, freq[idmax-bw:idmax+bw], diff_eff[idmax-bw:idmax+bw], guess=[.0001,.0001,.0001], ax=None, N=100)
        X = np.linspace(freq[idmax-bw],freq[idmax+bw])
        Y = f(X,*args)
        ax.plot(X, Y, color=c)"""
        

    ax.set_xlim()
    ax.set_ylim()
    ax.fill_betweenx([-100,200],428-25,428+25,label='AOM labeled bandwidth', color='grey',alpha=.4)
    ax.vlines(428,ymin=-100,ymax=200,label='428MHz',color='black',ls=':')
    ax.set_xlabel("Recentered Frequency (MHz)")
    ax.set_ylabel("Max Diffraction efficiency (%)")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()
