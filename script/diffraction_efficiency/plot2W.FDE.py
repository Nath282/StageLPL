#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from Measurement import Measure as M
from Measurement import DataSet 

def format_data(ds : DataSet) :
    params = ds.metadata['Parameters']
    Freq, diff_eff, opt_pow = ds['RF displayed frequency'], ds['Diffracted intensity']/params['laser intensity']*100, ds['Optimum displayed diffraction power']
    return Freq, diff_eff, opt_pow

# Programme principal
if __name__ == "__main__":

    rootpath = '/Users/nathanleretif/StageLPL/data/diffraction_efficiency/'
    ext = '.FDE.csv'
    filenames = ['2W','2Wbis','2Wm2']

    fig1, fig2 = plt.figure(figsize=(8,6)), plt.figure(figsize=(8,6))
    gs1, gs2 = fig1.add_gridspec(1,1), fig2.add_gridspec(1,1)
    ax1, ax2 = fig1.add_subplot(gs1[0]), fig2.add_subplot(gs2[0])

    # 2W : 
    ds = DataSet.read_file(rootpath+'2W'+ext)
    freq, diff_eff, opt_pow = format_data(ds)
    M.errorbar(ax1, freq, diff_eff, label='16/06', color='C0', ls='',marker='s')
    M.errorbar(ax2, freq, opt_pow, label='16/06', color='C0', ls=':')

    # 2Wbis : 
    ds = DataSet.read_file(rootpath+'2Wbis'+ext)
    freq, diff_eff, opt_pow = format_data(ds)
    M.errorbar(ax1, freq, diff_eff, color='C0', ls='',marker='s')
    M.errorbar(ax2, freq, opt_pow, color='C0', ls=':')

    # 2Wm2 : 
    ds = DataSet.read_file(rootpath+'2Wm2'+ext)
    freq, diff_eff, opt_pow = format_data(ds)
    M.errorbar(ax1, freq, diff_eff, label='19/06', color='C1', ls='',marker='s')
    M.errorbar(ax2, freq, opt_pow, label='19/06', color='C1', ls=':')

    ax1.set_xlim()
    ax1.set_ylim()
    ax1.fill_betweenx(y=[0,150],x1=428-25,x2=428+25,label="AOM theoritical bandwidth",alpha=.3, color='grey')
    ax1.vlines(428,-15,150,ls='--',color='black',label='428MHz')
    ax1.set_xlabel("Frequency (MHz)")
    ax1.set_ylabel("Diffraction efficiency (%)")
    ax1.legend()
    ax1.grid(True)

    ax2.set_xlim()
    ax2.set_ylim()
    ax2.vlines(428,-15,5,ls='--',color='black',label='428MHz')
    ax2.set_xlabel("Frequency (MHz)")
    ax2.set_ylabel("Optimum RF power")
    ax2.legend()
    ax2.grid(True)

    # Mesure efficacité 428Mhz Type B : 
    i = np.array([34.1,34.0,33.8,33.6,33.8,33.7,33.1,33.1,32.9,32.9])
    laser = np.array([39.4,39.7,38.7,38.4,38.6,38.9,38.7,38.3,39,37.8])
    print(f"max efficiency ={M(i/laser,unc_type='a')}")

    #plt.tight_layout()
    plt.show()


    
    
    