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




# Programme principal
if __name__ == "__main__":

    z = np.array([5,7.5,10,15,20,25,30,35,40,45,50]) # cm, Delta=1cm
    two_w = np.array([810,824,827,827,834,840,843,850,858,881,892]) # um, Delta=10um
    w = two_w/2
    u_z, u_w = 1/sqrt(3), 5/sqrt(3)

    def waist (z,w0,z0) : 
        zr = np.pi*w0**2/.532
        return w0*np.sqrt( 1 + ((z-z0)*10**4/zr)**2 )
    
    guess = [400,-10]
    args, cov = curve_fit(waist,z,w,guess)
    print(*args)
    zr = pi*(args[0])**2/.532
    print(f'zr={zr:.4f}')
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot()

    ax.errorbar(z,w,yerr=5,xerr=.5,label='data',ls='')

    z = np.linspace(np.min(z),np.max(z),100)
    ax.plot(z,waist(z,*args),label='fit')
    #ax.plot(z,waist(z,*guess),label='guess')

    ax.legend()
    ax.set_xlabel('position (cm)')
    ax.set_ylabel('waist (um)')
    plt.show()