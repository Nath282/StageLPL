#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mesure de l'efficacité de diffraction en fonction de la polarisation
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure, DataSet
from scipy.stats import linregress
from scipy.optimize import curve_fit


# Programme principal
if __name__ == "__main__":

    rootpath = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/'
    filename = '2W'
    ext = '.PDE.csv'

    ds = DataSet.read_file(rootpath+filename+ext)
    params = ds.metadata['Parameters']
    angle, diff_eff = ds['Half waveplate angle'] - params['fast axis angle'], ds['Diffracted intensity (mW)'] / params['laser intensity']

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    Measure.errorbar(ax,angle,diff_eff,ls='',marker='s',color='C0',label='data')

    angle = angle.value
    f = lambda x,x0,A,w,B : A*np.cos(w*(x-x0))**2+B
    guess = [0,.015,.07,.85]
    args, _ = curve_fit(f,angle,diff_eff.value,p0=guess)
    #ax.plot(angle,f(angle,*guess),label='guess',ls='--',color='C2')
    angle = np.linspace(min(angle),max(angle),200)
    ax.plot(angle,f(angle,*args),label='fit',ls='-',color='C1')
    #print(*args)
    dmin,dmax = np.min(f(angle,*args)),np.max(f(angle,*args))
    #print(dmin,dmax)
    

    """
    angle2, diff_eff2 = angle[:9], diff_eff[:9]
    line = linregress(angle2.value,diff_eff2.value)
    a, b = line.slope, line.intercept
    print(a,b)
    diff_double_pass = diff_eff2 * diff_eff2.flip()
    Measure.errorbar(ax,angle2,diff_eff2,ls='',marker='.',label='single pass')
    ax.plot(angle2.value, a*angle2.value+b, ls='--', label='fit lineaire')
    Measure.errorbar(ax,angle2,diff_double_pass,ls='--',marker='.',label='double pass')
    ax.hlines(.815**2,angle2.min().value,angle2.max().value)
    """

    ax.legend()
    ax.set_xlabel("half waveplate angle")
    ax.set_ylabel("Diffraction efficiency (%)")
    ax.grid(True)



    #fig.savefig('/Users/nathanleretif/StageLPL/figures/fig23dB.ADE.png')
    plt.tight_layout()
    plt.show()
