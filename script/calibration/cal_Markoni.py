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
    mes_pow = M([-0.58,0.41,1.41,2.42,3.42,4.34,5.31,6.29,7.28,8.28,9.28,10.29],Delta=.01)
    print(disp_pow)
    print(mes_pow)

    # Plotting initialisation
    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1,2)
    ax = fig.add_subplot(gs[0])

    # Plotting
    M.errorbar(ax,disp_pow,mes_pow, marker='.',color='C1',label='experimental data')
    ax.plot(disp_pow.value,disp_pow.value,color='C0',label='y=x')
    ax.set_xlabel("display power (dBm)")
    ax.set_ylabel("mesured power (dBm)")
    ax.set_aspect('equal')
    ax.grid(True)

    ax2 = fig.add_subplot(gs[1])
    M.errorbar(ax2,disp_pow,mes_pow-disp_pow,label='experimental data')
    avg = np.mean(mes_pow.value-disp_pow.value)
    ax2.hlines(avg,2,12,ls='--',label=f'average={avg:.2f}')
    ax2.legend()
    ax2.set_xlabel("displayed power (dBm)")
    ax2.set_ylabel("power difference between display and mesures (dB)")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
