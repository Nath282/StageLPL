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

    disp_pow = M(np.linspace(2,13,12))
    mes_pow = M([-0.58,0.41,1.41,2.42,3.42,4.34,5.31,6.29,7.28,8.28,9.28,10.29],.01)
    diff = mes_pow-disp_pow

    ax = Axes()
    M.errorbar(ax,mes_pow,diff,ls=':',label='experimental data')
    ax.set_lims()
    avg = diff.mean()
    M.hlines(ax,avg,-5,20,label=f"mean = {avg} dB",color='red',alpha=.1)
    ax.set_labels('Mesured power (dBm)', 'Power difference (dB)')
    ax.save('cal_Markoni')
    Axes.show()
