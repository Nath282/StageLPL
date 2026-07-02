#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure, DataSet


# Programme principal
if __name__ == "__main__":

    rootpath = '/Users/nathanleretif/StageLPL/data/'
    f1,f2,f3,f4,f5 = 'double_pass/FDEm2.DP.csv','double_pass/FDE.DP.csv', 'diffraction_efficiency/2Wm2.FDE.csv', 'diffraction_efficiency/2W.FDE.csv', 'diffraction_efficiency/2Wbis.FDE.csv'
    plot_optimum_power = True

    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    if plot_optimum_power : 
        fig2 = plt.figure(figsize=(8,6))
        gs2 = fig2.add_gridspec(1,1)
        ax2 = fig2.add_subplot(gs2[0])

    # Treatment of file 1
    ds = DataSet.read_file(rootpath+f1)
    Freq, I_diff, opt_pow, I_laser = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['Optimum displayed diffraction power'], ds['laser intensity']
    diff_eff = I_diff/I_laser
    Measure.errorbar(ax, Freq, diff_eff, label='FDEm2.DP', ls='-', marker='.',color='C0')
    if plot_optimum_power : Measure.errorbar(ax2, Freq, opt_pow, label='FDEm2.DP', ls='-', marker='.',color='C0')

    # Treatment of file 2
    ds = DataSet.read_file(rootpath+f2)
    params = ds.metadata['Parameters']
    Freq, I_diff, opt_pow, I_laser = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['Optimum displayed diffraction power'], params['laser intensity']
    diff_eff = I_diff/I_laser
    Measure.errorbar(ax, Freq, diff_eff, label='FDE.DP', ls='-', marker='.',color='C1')
    if plot_optimum_power : Measure.errorbar(ax2, Freq, opt_pow, label='FDE.DP', ls='-', marker='.',color='C1')

    # Tretment of file 3
    ds = DataSet.read_file(rootpath+f3)
    params = ds.metadata['Parameters']
    Freq, I_diff, opt_pow, I_laser = ds['RF displayed frequency'], ds['Diffracted intensity'], ds['Optimum displayed diffraction power'], params['laser intensity']
    diff_eff = (I_diff/I_laser)**2
    Measure.errorbar(ax, Freq, diff_eff, label='2Wm2.FDE**2', ls='-', marker='.',color='C2')
    if plot_optimum_power : Measure.errorbar(ax2, Freq, opt_pow, label='2Wm2.FDE', ls='-', marker='.',color='C2')

    # Treatment of file 4,5
    ds1, ds2 = DataSet.read_file(rootpath+f4), DataSet.read_file(rootpath+f5)
    params1,params2 = ds1.metadata['Parameters'],ds2.metadata['Parameters']
    Freq1, I_diff1, opt_pow1, I_laser1 = ds1['RF displayed frequency'], ds1['Diffracted intensity'], ds1['Optimum displayed diffraction power'], params1['laser intensity']
    diff_eff1 = I_diff1/I_laser1
    Freq2, I_diff2, opt_pow2, I_laser2 = ds2['RF displayed frequency'], ds2['Diffracted intensity'], ds2['Optimum displayed diffraction power'], params2['laser intensity']
    diff_eff2 = I_diff2/I_laser2
    #Measure.errorbar(ax, Freq1, diff_eff1, label='2W.FDE', ls='-', marker='.',color='C5')
    #Measure.errorbar(ax, Freq2, diff_eff2, ls='-', marker='.',color='C5')
    if plot_optimum_power : Measure.errorbar(ax2, Freq1, opt_pow1, label='FDEm2.DP', ls='-', marker='.',color='C5')
    if plot_optimum_power : Measure.errorbar(ax2, Freq2, opt_pow2, ls='-', marker='.',color='C5')


    ax.vlines(428,ymin=.25,ymax=.8,color='red',label='428Mhz',ls='--')
    ax.set_xlabel("Frequency (Mhz)")
    ax.set_ylabel("Diffraction efficiency (%)")
    ax.legend()
    ax.grid(True)

    if plot_optimum_power :  
        ax2.set_xlabel("Frequency (Mhz)")
        ax2.set_ylabel("Optimum Diffraction power (dBm)")
        ax2.legend()
        ax2.grid(True)

    plt.show()