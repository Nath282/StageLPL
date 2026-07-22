#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from numpy import array, sqrt
from Measurement import Measure as M
from Plotting import Axes


# Programme principal
if __name__ == "__main__":

    ax = Axes()

    dis_pow = M(array([-16,-14,-12,-10,-8,-7,-6,-5,-4,-3,-2,0,2,4,6,8,10]),unit='dBm')
    mes_pow = M(array([-44,-41,-38.5,-35.8,-30.4,-25,-18,-13.6,-9.2,-7.3,-5.6,-3.7,-2.3,-1.8,-1.7,-1.9,-2.2]),.1)
    marconi_corr = M(-2.65,.02,unc_type='unchanged')
    att_corr = M(-40,1)

    inc_power = dis_pow + marconi_corr
    out_pow = mes_pow - att_corr
    gain = out_pow-inc_power
    print(gain.max())

    M.errorbar(ax,inc_power,out_pow,label='amplified signal',color='C0',ls='--')
    M.errorbar(ax,inc_power,gain,label='gain',color='C1',ls=':')
    ax.set_lims()
    ax.hlines(31.1,xmin=-30,xmax=20,label='1.3W', color='r')
    ax.set_labels("incoming power (dBm)", "amplified power/gain (dBm/dB)")

    secax = ax.secondary_xaxis('top', functions=(lambda x:x-marconi_corr.value, lambda x:x+marconi_corr.value))
    secax.set_xlabel("displayed source power (dBm)")

    ax.save('cal_ampli1W')
    Axes.show()