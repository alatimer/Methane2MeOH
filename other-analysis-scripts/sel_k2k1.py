#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
import math
from ase.units import kB
import numpy as np
from selclass import selclass
from PointParameters import get_color

##### load exp data #########
expclassesobj = pickle.load(open('expobj.pkl','rb'))
#remove exp data where no methanol observed
expclassesobj = expclassesobj.classfilter(lambda x: x.sel!=0)
#only include what are believed to be single-atom catalysts
#expclassesobj = expclassesobj.classfilter(lambda x: x.single_site=='yes')
#exclude exp MMO, diffusion limited
expclassesobj = expclassesobj.classfilter(lambda x: x.cattype!='MMO')

solv_corr=0.22
dEa_theory=0.55
P = 101325

size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)

def ln_sel(k2_k1,T,conv):
    sel = (1-conv-(1-conv)**(k2_k1))/(conv*(k2_k1-1))*100
    return np.log(sel) #in percent

k2_k1=np.arange(-100,1,1)

ax.plot(k2_k1,ln_sel(k2_k1,500,1e-5))

#ax.set_ylabel('Experimental Selectivity')
#ax.set_xlabel('Model Selectivity')
plt.savefig('lnsel.pdf')
