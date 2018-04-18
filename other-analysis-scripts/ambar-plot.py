#!/usr/bin/env python

import numpy as np
from scipy.optimize import newton_krylov
from numpy import cosh, zeros_like, mgrid, zeros
import matplotlib.pyplot as plt
import math
import pickle

target_sel = 50 # in percent

##### load exp data #########
expclassesobj = pickle.load(open('expobj.pkl','rb'))
#remove exp data where no methanol observed
expclassesobj = expclassesobj.classfilter(lambda x: x.sel!=0)
#only include what are believed to be single-atom catalysts
expclassesobj = expclassesobj.classfilter(lambda x: x.single_site=='yes')
#exclude exp MMO, diffusion limited
expclassesobj = expclassesobj.classfilter(lambda x: x.cattype!='MMO')
expclassesobj = expclassesobj.classfilter(lambda x: x.sel>target_sel)
expclassesobj = expclassesobj.classfilter(lambda x: x.rxntype!='aqueous')

def selectivity(x,T, deltaG):
    kb = 8.617E-5 # in eV
    k_ratio = math.exp(deltaG/kb/T)
    y = 100*(1 - x - (1-x)**k_ratio)/(x*(k_ratio - 1))
    return y

# Given a deltaG and T, plot sel vs. conv.
deltaG = 0.40
max_conv = []
T_range = []

for T in np.linspace(300,700,50):
    T_range.append(T)
    found_max = False
    conv = []
    sel = []

    for i, x in enumerate(np.linspace(-8,0,100)):
        i_conv = np.power(10,x)
        i_sel = selectivity(i_conv,T,deltaG)
        conv.append(i_conv)
        sel.append(i_sel)

        if i_sel <= target_sel and sel[i-1] > target_sel and found_max==False:
            max_conv.append(i_conv)
            print i_conv, T
            found_max = True
    plt.semilogx(conv,sel)


plt.figure()
plt.semilogy(T_range,max_conv)

for cat in expclassesobj.data:
    plt.plot(cat.T,cat.conv,'ok')

plt.ylim([10e-8,10e-2])
plt.xlabel('Temperature')
plt.ylabel('Max conversion to get 80pc selectivity')

plt.show()
