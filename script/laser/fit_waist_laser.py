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
from Plotting import Axes

def waist (z,w0,z0) : 
        zr = np.pi*(w0*1e-6)**2/(532e-9) *1e2
        return w0*np.sqrt( 1 + ((z-z0)/zr)**2 )

# Programme principal
if __name__ == "__main__":

    

    z = M([5,7.5,10,15,20,25,30,35,40,45,50],1,unit='cm')
    two_w = M([810,824,827,827,834,840,843,850,858,881,892],10,unit='um')
    w = two_w/2

    ax = Axes()
    M.errorbar(ax, z, w, ls='', label='data', marker='s')
    args = M.curve_fit(waist, z, w, guess=[400,-10], ax=ax, N=100)
    [w0,z0] = args
    zr = pi*(w0*1e-6)**2/(532e-9)*1e2
    print(f"w0 = {w0} um, z0 = {z0} cm, zr = {zr} cm")
    z = np.linspace(np.min(z.value),np.max(z.value),100)
    ax.set_labels('position (cm)', 'waist (um)')
    ax.save('fit_waist_laser')
    Axes.show()