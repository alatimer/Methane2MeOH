#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
import math
from ase.units import kB
import numpy as np
from PointParameters import get_color,get_shape
from Selectivity import plot_sel,sel_fun

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

size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)

#### Plot Model selectivity ####
conv_vec = np.logspace(-5,-.01,num=1e2,base=10)
plot_sel(ax,conv_vec,0.55,T_fix,facecolor='k',color='k')

#### Plot Experimental points #####
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

    #assign cat object a dEa
    cat.get_dEa(dEa_guess,cat.T,solv_corr=solv_corr)
    
    #plot experimental data with extrapolated selectivity
    modelsel = sel_fun(cat.conv,T_fix,dEa=cat.dEa,dGa=None,error=None)
    ax.plot(cat.log_conv,
            modelsel,
            color=get_color(cat.category),
            marker=get_shape(cat.rxntype),
            label=label,
            fillstyle='full',
            markersize=10,
            clip_on=False)


ax.set_title('T=%i K; all data (extrapolated)'%(int(T_fix)))
ax.legend(loc=3,fontsize=15)
ax.set_xlabel(r'log(CH$_4$ conversion)')
ax.set_ylabel(r'CH$_3$OH selectivity (%)')
plt.savefig('fig-5-main-SvX-extrapolated.pdf')
