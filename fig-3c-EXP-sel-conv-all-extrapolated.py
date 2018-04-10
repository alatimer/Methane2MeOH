#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
import math
from ase.units import kB
import numpy as np
from selclass import selclass
from PointParameters import get_color,get_shape
from Selectivity import plot_sel

### load DFT data ######3
# For performance, can just use vibrations from Ni-BN since it is ~ average
dftobj = pickle.load(open('dftobj.pkl','rb'))
dftobj = dftobj.filter(lambda x: x.vibs_ch4!=None)
dftobj = dftobj.filter(lambda x: x.cat=='Ni')
dftobj = dftobj.filter(lambda x: x.cattype=='Boron-nitride')

##### load exp data #########
expclassesobj = pickle.load(open('expobj.pkl','rb'))
#remove exp data where no methanol observed
expclassesobj = expclassesobj.classfilter(lambda x: x.sel!=0)
#only include what are believed to be single-atom catalysts
expclassesobj = expclassesobj.classfilter(lambda x: x.single_site=='yes')
#exclude exp MMO, diffusion limited
expclassesobj = expclassesobj.classfilter(lambda x: x.cattype!='MMO')

solv_corr=0.22
dEa_guess=0.55
T_fix=700
P = 101325
dGcorr = -4.191e-4*T_fix-0.0152 #dftobj.fun_dGcorr(T_fix,101325)
err = 0.07

size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)

#### Plot Model selectivity ####
conv_vec = np.logspace(-5,-.01,num=1e2,base=10)
#selobj = selclass(conv_vec,dftobj,color='k')
#selobj.fun_err(ax,err,dEa_guess,T_fix,P)
plot_sel(ax,conv_vec,0.55,T_fix,facecolor='k',color='k')

#### Experimental points #####
labels=[]
for cat in expclassesobj.data:
    label = '%s-%s, %s'%(cat.cat,cat.cattype,cat.author)
    label = '%s'%(cat.category)
    #if cat.rxntype=='aqueous':
    #    label = None
    if label in labels:
        label = None
    else:
        labels.append(label)
    cat.get_dEa(dEa_guess,cat.T,dftobj,solv_corr=solv_corr)
    #extrapolate selectivity
    modelsel = cat.sel_fun(T_fix,P,dftobj) #rethink, plots model
    #plot experimental data with extrapolated selectivity
    ax.plot(cat.log_conv,
            modelsel,
            color=get_color(cat.category),
            marker=get_shape(cat.rxntype),
            label=label,
            fillstyle='full',
            markersize=10,
            clip_on=False)



ax.legend(loc=3,fontsize=10)
ax.set_xlabel(r'log(CH$_4$ conversion)')
ax.set_ylabel(r'CH$_3$OH selectivity (%)')
plt.savefig('fig-3c-EXP-sel-conv-all-extrapolated.pdf')
