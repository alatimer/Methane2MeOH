#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
import math
from ase.units import kB
import numpy as np
from selclass import selclass
from Selectivity import sel_fun,plot_sel

##### load exp data #########
expclassesobj = pickle.load(open('expobj.pkl','rb'))
#remove exp data where no methanol observed
expclassesobj = expclassesobj.classfilter(lambda x: x.sel!=0)
#only include what are believed to be single-atom catalysts
#expclassesobj = expclassesobj.classfilter(lambda x: x.single_site=='yes')
#exclude exp MMO, diffusion limited
expclassesobj = expclassesobj.classfilter(lambda x: x.cattype!='MMO')

solv_corr=0.22
dEa_guess=0.55
T_fix=700
P = 101325

size=(7,5)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)

#### Experimental points #####
labels=[]
for cat in expclassesobj.data:
    if cat.single_site=='yes':
        clr='grey'
        label="single site"
    else:
        clr='c'
        label = "non-single site"
    if label in labels:
        label = None
    else:
        labels.append(label)
    cat.get_dEa(dEa_guess,cat.T,solv_corr=solv_corr)
    #extrapolate selectivity
    modelsel = cat.sel_fun(T_fix) 
    #plot experimental data with extrapolated selectivity
    ax.plot(cat.log_conv,
            modelsel,
            color=clr,
            marker='o',
            label=label,
            fillstyle='full',
            markersize=10,
            clip_on=False)

#### Plot Model selectivity ####
conv_vec = np.logspace(-5,-.01,num=1e2,base=10)
plot_sel(ax,conv_vec,0.55,T_fix,facecolor='k',color='k')

plt.text(-5.7,-12,'(b)',fontsize=30)
ax.legend(loc='best',fontsize=14)
ax.set_xlabel(r'log(CH$_4$ conversion)')
ax.set_ylabel(r'CH$_3$OH selectivity (%)')
plt.tight_layout()
plt.savefig('fig-9b-extrap-ss-nss.pdf')
