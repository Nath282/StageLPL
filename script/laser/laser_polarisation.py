#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from numpy import array, cos, sin, pi, sqrt, exp
from Plotting import Axes
from Measurement import Measure as M 



# Programme principal
if __name__ == "__main__":

    theta0 = M(65 /360*2*pi)
    theta = M(np.linspace(65,110,10), 1)
    P = M([50.8,49.7,45.9,40.3,32.8,25.1,17,11.39,7.22,5.56], 1, unit='mW')
    r = P/55.9

    def Intensity (theta,alpha,phi) : 
        if isinstance(theta, M) : theta = theta.value
        if isinstance(alpha, M) : alpha = alpha.value
        if isinstance(phi, M) : phi = phi.value
        t = theta /360*2*pi - theta0
        x0,y0 = alpha, sqrt(1-alpha**2)*exp(1j*phi)
        x1, y1 = cos(t)*x0+sin(t)*y0, -sin(t)*x0+cos(t)*y0
        x2, y2 = x1, -y1
        _, y3 = cos(t)*x2-sin(t)*y2, sin(t)*x2+cos(t)*y2
        return np.abs(y3)**2
    
    def polarisation(t, alpha, phi) :
        beta = sqrt(1-alpha**2)
        return array([alpha*cos(t+theta0), beta*cos(t+phi+theta0)])
    
    ax1 = Axes()
    M.errorbar(ax1, theta, r, label='data', ls='', marker='s')
    args = M.curve_fit(Intensity, theta, r, guess=[.31,1.63], N=100, ax=ax1)
    ax1.set_labels('Half-waveplate angle (degrees)', 'Power ratio (%)')
    ax1.save('fit_pol_laser',bbox_inches="tight",pad_inches=0.05)

    ax2 = Axes()
    t = np.linspace(0,2*pi,100)
    [x,y] = polarisation(t, *args)
    ax2.plot(x,y, color='green')
    ax2.hlines(0,xmin=-.95,xmax=+.95,linewidth=0)
    #ax2.set_title('Polarisation')
    ax2.set_aspect('equal')
    ax2.save('pol_laser')

    Axes.show()






    