#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from numpy import array, cos, sin, pi, sqrt, exp
from scipy.optimize import curve_fit

from Measurement import Measure as M

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

# Programme principal
if __name__ == "__main__":

    z = M([5,7.5,10,15,20,25,30,35,40,45,50],1,unit='cm')
    two_w = M([810,824,827,827,834,840,843,850,858,881,892],10,unit='um')
    w = two_w/2

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])
    print(type(ax))
    M.errorbar(ax, z, w, ls='', label='data')

    def waist (z,w0,z0) : 
        zr = np.pi*(w0*1e-6)**2/(532e-9) *1e2
        return w0*np.sqrt( 1 + ((z-z0)/zr)**2 )
    def estimator (z,w,func=waist, guess=[400,-10]) :
        args, _ = curve_fit(func,z,w,guess)
        return args

    [w0,z0] = M.MonteCarlo(estimator, z, w, N=100)
    zr = pi*(w0*1e-6)**2/(532e-9)*1e2
    print(f"w0 = {w0} um, z0 = {z0} cm, zr = {zr} cm")
    z = np.linspace(np.min(z.value),np.max(z.value),100)

    ax.plot(z, waist(z,w0,z0), label='fit')
    ax.legend()
    ax.set_xlabel('position (cm)')
    ax.set_ylabel('waist (um)')
    ax.grid(True)
    plt.show()