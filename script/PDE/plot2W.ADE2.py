#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
from Measurement import Measure, DataSet
from Plotting import Axes

if __name__=='__main__' : 

    rootpath, ext = '/Users/nathanleretif/StageLPL/data/PDE/', '.csv'
    files = {'2W.ADE2.csv':'2th order','2Wm2.ADE.csv':'1st order'}
    #files = {'2W.ADE2.csv':'2th order'}

    ax = Axes()

    ds = DataSet.read_file(rootpath+'2W.SPO2'+ext)
    params = ds.metadata['Parameters']
    disp_pow, diff_eff = ds['RF displayed signal power'], (ds['Diffracted intensity'] / params['laser intensity'])*100
    Measure.errorbar(ax,disp_pow,diff_eff,ls='',marker='s',label='2nd order')
    #print(f"max diffraction efficiency for {filename} : {diff_eff.max()*100}")

    ds = DataSet.read_file(rootpath+'2W.SP2'+ext)
    params = ds.metadata['Parameters']
    disp_pow, diff_eff = ds['RF displayed signal power'], (ds['Diffracted intensity'] / params['laser intensity'])*100
    Measure.errorbar(ax,disp_pow,diff_eff,ls='',marker='s',label='1st order')
    Measure.errorbar(ax,disp_pow,diff_eff**2*1e-2, ls='', marker='s', label='1st order squared')
    #print(f"max diffraction efficiency for {filename} : {diff_eff.max()*100}")

    ax.set_labels('Displayed RF power (dBm)', '2nd order diffraction efficiency (%)')
    ax.save('ADE.SO.SP')
    Axes.show()
