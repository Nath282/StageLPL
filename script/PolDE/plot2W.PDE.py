#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mesure de l'efficacité de diffraction en fonction de la polarisation
"""

# Import des librairies
import numpy as np
from Measurement import Measure, DataSet
from Plotting import Axes


# Programme principal
if __name__ == "__main__":

    rootpath, ext = '/Users/nathanleretif/StageLPL/data/PolDE/', '.csv'
    filename = '2W.PDE'

    ds = DataSet.read_file(rootpath+filename+ext)
    params = ds.metadata['Parameters']
    angle, diff_eff = 2*(ds['Half waveplate angle'] - params['fast axis angle']), ds['Diffracted intensity (mW)'] / params['laser intensity']

    ax = Axes()
    Measure.errorbar(ax,angle,diff_eff,ls='',marker='s',color='C0',label='data')

    f = lambda x,x0,A,w,B : A*np.cos(w*(x-x0))+B
    args = Measure.curve_fit(f, angle, diff_eff, guess=[0,.015,.03,.85], N=100, ax=ax, plot_fit_unc=False)
    print(*args)
    print(diff_eff.max()*diff_eff.min())
    ax.set_labels("Polarisation angle (degrees)", "Diffraction efficiency (%)")
    
    ax.save('PolDE.SP')
    Axes.show()
