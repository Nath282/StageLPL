#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import jv as bessel
from scipy.optimize import curve_fit
from Measurement import Measure, DataSet

def format_file(filename, rootpath, ax) :
    ds = DataSet.read_file(rootpath+filename)
    params = ds.metadata['Parameters']
    disp_pow, diff_eff = ds['RF displayed signal power(dBm)'], ds[' Diffracted intensity (mW)'] / params['laser intensity']
    Measure.errorbar(ax,disp_pow,diff_eff,ls='',marker='.',label='data order')
    x, y = disp_pow.value, diff_eff.value
    return x,y 


if __name__=='__main__' : 

    rootpath = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/'
    filenames = ['2W.ADE2.csv','2W.ADE.csv']
    polyfit = True
    gaussian = False
    bessel = False

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    x1, y1 = format_file('2W.ADE.csv', rootpath, ax)
    x2, y2 = format_file('2W.ADE2.csv', rootpath, ax)
    X = np.linspace(-35, 10, 500)

    # Polyfit 
    if polyfit : 
        p = np.polyfit(x1,y1,deg=5)
        ax.plot(X, np.polyval(p, X), label='polyfit 1st')
        f = lambda x,x0,A,B : A*np.polyval(p,(x-x0)*B)
        guess = [10,.8,1.2]
        args_pol,_ = curve_fit(f, x2, y2, guess)
        ax.plot(X, f(X,*guess),label='guess')
        ax.plot(X, f(X,*args_pol), label='fit')

    # Gaussian fit
    if gaussian : 
        gauss = lambda x,x0,A,sigma : A*np.exp(-(x-x0)**2/(2*sigma**2))
        args1, _ = curve_fit(gauss, x1, y1, p0=[-10,0.68,10])
        args2, _ = curve_fit(gauss, x2, y2, p0=args1)
        ax.plot(X, gauss(X,*args1), label='fit gaussien 1st')
        ax.plot(X, gauss(X,*args2), label='fit gaussien 2nd')
    
    # Bessel functions -> marche vraiment pas bien
    if bessel : 
        func = lambda x,x0,A,B : A*bessel(1,(x-x0)/B)
        guess = [-35,.7,10]
        args, _ = curve_fit(func, x1, y1, guess)
        ax.plot(X,func(X,*guess),label='guess')
        ax.plot(X,func(X,*args),label='fit')
        #ax.plot(X,bessel(1,X),label='bessel order 1')
        #ax.plot(X,bessel(2,X),label='bessel order 2')
    
    ax.set_xlabel('Displayed RF power (dBm)')
    ax.set_ylabel('diffraction efficiency (%)')
    ax.set_ylim(-2,4)
    ax.grid(True)
    ax.legend()

    #fig.savefig('/Users/nathanleretif/StageLPL/figures/.png')
    plt.show()