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

    disp_pow = M(np.linspace(-18,12,16),unit='dBm')
    mes_pow = M([-41.4,-34.6,-32.3,-30.2,-28.1,-25.6,-23.6,-21.6,-19.6,-17.6,-15.8,-13.9,-13,-12.7,-12.5,-12.5],.3,unit='dBm')
    rf_corr = M(-2.65,.02,unc_type='unchanged')
    attenuator = M(40,.5)
    inc_pow = disp_pow + rf_corr
    amp_pow = mes_pow + attenuator
    gain = amp_pow-inc_pow
    typ_gain = gain[1:11].mean()
    
    ax = Axes()
    M.errorbar(ax, inc_pow, amp_pow, label='amplified signal', ls='', marker='s')
    M.errorbar(ax, inc_pow, gain, label='gain', ls='',marker='s')
    ax.set_lims()
    M.hlines(ax, typ_gain, -30, 30, label=f'gain typique = {typ_gain} dB',ls='--',color='C1')
    ax.set_labels("amplitude du signal d'entré (dBm)", 'amplitude/gain (dBm/dB)')
    ax.save('cal_ampli23dB')
    Axes.show()