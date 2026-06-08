#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# Programme principal
if __name__ == "__main__":

    z = np.array([5,7.5,10,12.5,15,20,25]) # m
    w = np.array([475,294,99.5,190,435,840,1270]) # m

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot()

    ax.errorbar(z,w,yerr=5,xerr=.5,label='exp')

    def f (z,w0,z0) : 
        zr = np.pi*w0**2/.532
        return w0*np.sqrt( 1 + ((z-z0)*10**4/zr)**2 )
    guess = [20,10]

    args, cov = curve_fit(f,z,w,guess)
    z = np.linspace(np.min(z),np.max(z),100)
    ax.plot(z,f(z,*args),label='fit')

    ax.plot(z,f(z,*guess),label='guess')

    print(*args)

    ax.legend()
    ax.set_xlabel('position (cm)')
    ax.set_ylabel('waist (um)')
    plt.show()