#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5

# Variables globales : 
lamb = 532e-9 # nm


# Definition des fonctions

def gaussian_parameters (z,z0,w0) : 
    zc = z-z0
    zr = np.pi/lamb * w0**2
    w = w0 * np.sqrt( 1 + (zc/zr)**2 )
    Rc = zc * ( 1 + (zr/zc)**2 )
    q = 1/Rc + 1j*lamb/(np.pi*1*w**2)
    return w, Rc, q

def lens_action (f,zf,q) :
    new_q = f*q/(f-q)
    Rc = 1/new_q.real
    X = 1/new_q.imag
    alpha = Rc/X
    z0 = zf - Rc/(1+alpha**2)
    w0 = lamb/np.pi * alpha/(1+alpha**2) * Rc
    return new_q, z0, w0


# Programme principal
if __name__ == "__main__":

    # Definition des variables :
    # z=0 : 
    z0 = -10e-2
    w0 = 420e-6
    print(z0*10**2,w0*10**6)

    # first lens :
    f1 = 150e-3 #m
    zf1 = 10e-2 #m
    _,_,q = gaussian_parameters(zf1,z0,w0)
    _,z1,w1 = lens_action(f1,zf1,q)
    print(z1*10**2,w1*10**6)

    # second lens : 
    f2 = -50e-3
    zf2 = 10e-2 + zf1
    _,_,q = gaussian_parameters(zf2,z1,w1)
    _,z2,w2 = lens_action(f2,zf2,q)
    print(z2*10**2,w2*10**6)




    N = 1000
    length = 40e-2
    dx = length/N

    z = np.linspace(0,length,N)
    w = np.zeros_like(z)

    k0,k1 = 0,int(z1/dx)
    k2,k3 = k1+1,int(z2/dx)
    k4,k5 = k3+1,N-1

    w[k0:k1],_,_ = gaussian_parameters(z[k0:k1],z0,w0)
    w[k2:k3],_,_ = gaussian_parameters (z[k2:k3],z1,w1)
    w[k4:k5],_,_ = gaussian_parameters (z[k4:k5],z2,w2)

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    ax.plot(z*10**2,w*10**6)

    plt.show()

    




    pass