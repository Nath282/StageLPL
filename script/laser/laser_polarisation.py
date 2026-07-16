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

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

def R(t) : 
    return array([[cos(t),-sin(t)],[sin(t),cos(t)]])


# Programme principal
if __name__ == "__main__":

    theta0 = 65 /360*2*pi # position de l'axe principale de la lame demi-onde quand elle est aligné avec la polarisation du laser
    theta = np.linspace(65,110,10) # degré, Delta=1
    u_theta = 1/sqrt(3)
    P = np.array([50.8,49.7,45.9,40.3,32.8,25.1,17,11.39,7.22,5.56]) #mW, Delta = 1
    r = P/55.9
    u_r = r*sqrt( (1/P)**2 + (1/55.9)**2 ) / sqrt(3)

    
    def Intensity (theta,alpha,phi) : 
        
        t = theta /360*2*pi - theta0
        x0,y0 = alpha, sqrt(1-alpha**2)*exp(1j*phi)
        x1, y1 = cos(t)*x0+sin(t)*y0, -sin(t)*x0+cos(t)*y0
        x2, y2 = x1, -y1
        _, y3 = cos(t)*x2-sin(t)*y2, sin(t)*x2+cos(t)*y2
        return np.abs(y3)**2

    guess = [.05,2.3]
    args,cov = curve_fit(Intensity, theta, r, p0=guess)
    print(*args)

    fig1 = plt.figure(figsize=(8,6))
    ax1 = fig1.add_subplot()

    ax1.errorbar(theta, r, u_r, u_theta, label='data',ls='')
    theta = np.linspace(65,110,100)
    ax1.plot(theta, Intensity(theta, *args), label='fit')
    #ax1.plot(theta, Intensity(theta, *guess), label='guess')
    ax1.set_xlabel('Half-waveplate angle (degrees)')
    ax1.set_ylabel('Power ratio (%)')
    ax1.legend()
    ax1.grid(True)
    
 
    fig2 = plt.figure(figsize=(8,6))
    ax2 = fig2.add_subplot()

    def polarisation(t, alpha, phi) :
        beta = sqrt(1-alpha**2)
        return array([alpha*cos(t+theta0), beta*cos(t+phi+theta0)])

    t = np.linspace(0,2*pi,100)
    [x,y] = polarisation(t, *args)
    ax2.plot(x,y, label=f'pol', color='green')
    #ax2.hlines(0,-1,1,color='black',ls='--')
    #ax2.vlines(0,-1,1,color='black',ls='--')
    ax2.hlines(0,xmin=-.95,xmax=+.95,linewidth=0)
    ax2.set_title('Polarisation')
    #ax2.legend()
    ax2.set_aspect('equal')
    
    #plt.grid(True)
    plt.show()







    