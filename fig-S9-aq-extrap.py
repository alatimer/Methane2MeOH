#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
import math
from ase.units import kB
import numpy as np
from selclass import selclass
from PointParameters import get_color
from Selectivity import plot_sel,sel_fun

### load DFT data ######3
# For performance, can just use vibrations from Ni-BN since it is ~ average
dftobj = pickle.load(open('dftobj.pkl','rb'))
dftobj = dftobj.filter(lambda x: x.vibs_ch4!=None)
dftobj = dftobj.filter(lambda x: x.cat=='Ni')
dftobj = dftobj.filter(lambda x: x.cattype=='BN')

##### load exp data #########
expclassesobj = pickle.load(open('expobj.pkl','rb'))
#remove exp data where no methanol observed
expclassesobj = expclassesobj.classfilter(lambda x: x.sel!=0)
#only include what are believed to be single-atom catalysts
expclassesobj = expclassesobj.classfilter(lambda x: x.rxntype=='aqueous')
#exclude exp MMO, diffusion limited
expclassesobj = expclassesobj.classfilter(lambda x: x.cattype!='MMO')

solv_corr=0.22
dEa_guess=0.35
T_fix=323
P = 101325
dGcorr = dftobj.fun_dGcorr(T_fix,101325)
err = 0.07

size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)

#### Experimental points #####
labels=[]
for cat in expclassesobj.data:
    label = '%s-%s, %s'%(cat.cat,cat.cattype,cat.author)
    label = '%s'%(cat.cat)
    if label in labels:
        label = None
    else:
        labels.append(label)
    dEa = cat.get_dEa(dEa_guess,cat.T,dftobj,solv_corr=0)
    #extrapolate selectivity
    modelsel = cat.sel_fun(T_fix,P,dftobj) #rethink, plots model
    print modelsel
    #plot experimental data with extrapolated selectivity
    ax.plot(cat.log_conv,
            modelsel,
            color=get_color(cat.category),
            marker='o',
            label=label,
            fillstyle='full',
            markersize=15,
            clip_on=False)

#### Plot Model selectivity ####
conv_vec = np.logspace(-8,-.01,num=1e2,base=10)
selobj = selclass(conv_vec,dftobj,color='c')
selobj.fun_err(ax,err,dEa_guess-solv_corr,T_fix,P)
plot_sel(ax,conv_vec,0.55-solv_corr,T_fix,facecolor='c',color='c')

ax.legend(loc=3,fontsize=10)
ax.set_xlabel(r'log(CH$_4$ conversion)')
ax.set_ylabel(r'CH$_3$OH selectivity (%)')
ax.set_xlim([-8,0])
plt.savefig('fig-S9-aq-extrap.pdf')
