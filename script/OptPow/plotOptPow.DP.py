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


if __name__ == "__main__": 

    ax = Axes()
    # Files extracting
    dir, ext = '/Users/nathanleretif/StageLPL/data/FDE/', '.csv'
    files = ['SP1', 'SP2', 'DP1', 'DP2', 'DP3']
    colors = Axes.colormap(0,len(files))

    # Data extraction : 
    for filename, color in zip(files,colors) :
        ds = DataSet.read_file(dir+filename+ext)
        freq, opt_pow = ds['RF displayed frequency'], ds['Optimum displayed diffraction power']
        M.errorbar(ax, freq, opt_pow, label=filename, color=color, ls='', marker='s')

    ax.set_labels("RF frequency (MHz)", "Optimum displayed RF power (dBm)")
    ax.save('OptPow')
    Axes.show()

