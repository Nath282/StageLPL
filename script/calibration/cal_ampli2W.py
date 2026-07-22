#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import numpy as np
from Measurement import Measure as M
from Plotting import Axes

# Programme principal
if __name__ == "__main__":

    marc_corr =  M(-1.4,.1)
    att_corr = M(39.5,.3)

    dis_pow1 = M(np.linspace(-40,-2,20))
    mes_pow1 = M([-40.3,-38.2,-36,-34,-31.9,-29.9,-28,-25.9,-23.9,-22,-19.9,-17.9,-16,-14,-12,-10,-8.1,-6.3,-4.6,-3.2],.01) #11h12
    inc1, out1 = dis_pow1 + marc_corr, mes_pow1 + att_corr
    gain1 = out1 - inc1

    dis_pow2 = M(np.linspace(-8,0,9))
    mes_pow2 = M([-8.4,-7.5,-6.6,-5.9,-5.2,-4.7,-4.2,-3.9,-3.6],.1)
    inc2, out2 = dis_pow2 + marc_corr, mes_pow2 + att_corr
    gain2 = out2 - inc2

    ax = Axes()

    M.errorbar(ax, inc1, out1, label="amplified signal power 11h12", ls=':',marker='.', color='C0')
    M.errorbar(ax, inc2, out2, label="amplified signal power 11h39", ls='-',marker='x', color='C0')

    M.errorbar(ax, inc1, gain1, label="gain 11h12", ls='', marker='.',color='C1')
    M.errorbar(ax, inc2, gain2, label="gain 11h39", ls='', marker='x', color='C1')

    ax.set_lims()
    mean_gain = M.MonteCarlo(np.mean, gain1[:17], N=500)
    M.hlines(ax, mean_gain, xmin=-50, xmax=10, label=f"average gain : {mean_gain}",color='C1',ls='-')
    ax.hlines(31.1,xmin=-50,xmax=10,label='1.3W', color='r')
    
    ax.set_xlabel("Incoming RF power (dBm)")
    ax.set_ylabel("amplified signal power/gain (dBm/dB)")

    secax = ax.secondary_xaxis('top', functions=(lambda x:x-marc_corr.value, lambda x:x+marc_corr.value))
    secax.set_xlabel("displayed incoming power (dBm)")

    ax.save('cal_ampli2W')
    Axes.show()