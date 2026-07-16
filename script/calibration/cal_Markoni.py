#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description du fichier 
"""

# Import des librairies
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from Measurement import Measure as M

# Paramètres globaux d'affichage
import matplotlib as mpl
mpl.rcParams['font.size'] = 16
mpl.rcParams['lines.linewidth'] = 1.5


# Programme principal
if __name__ == "__main__":

    disp_pow = M(np.linspace(2,13,12))
    mes_pow = M([-0.58,0.41,1.41,2.42,3.42,4.34,5.31,6.29,7.28,8.28,9.28,10.29],.01)
    diff = mes_pow-disp_pow

    # Plotting initialisation
    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0])

    M.errorbar(ax,mes_pow,diff,ls=':',label='experimental data')
    ax.set_xlim()
    ax.set_ylim()
    avg = diff.mean()
    M.hlines(ax,avg,-5,20,label=f"mean = {avg} dB",color='red')
    ax.set_xlabel("Mesured power (dBm)")
    ax.set_ylabel("Power difference (dB)")
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()
