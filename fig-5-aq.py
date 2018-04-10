#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
from expclass import *
from scipy.optimize import minimize
from scipy.stats import norm
from ase.units import kB,_hplanck
from selclass import selclass
from PointParameters import get_color

##### PARAMETERS ######
sigma = 0.07
err = sigma #change for desired uncertainty percentage
dEa = 0.55
solv_corr = 0.22
P=101325

### INITIALIZE PLOT #####
size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)
ptsize = 15 #size of markers

### Conversion Vector ###
conv_vec = np.logspace(-10,-.01,num=1e2,base=10)

### Import DFT Data #######
dftobj = pickle.load(open('dftobj.pkl','rb'))
dftobj = dftobj.filter(lambda x: x.vibs_ch4!=None)

##### Import Exp Data ######
catlistobj = pickle.load(open('expobj.pkl','rb'))
catlistobj = catlistobj.classfilter(lambda x: x.single_site =='yes')
catlistobj = catlistobj.classfilter(lambda x: x.rxntype =='aqueous')

###### Model Selectivity #######
plugerr=err
condns={}

condns['323']={'T':[323,323],'line':'-','color':'c','solv_corr':solv_corr}
condns['323g']={'T':[323,323],'line':'-','color':'b','solv_corr':0}
 
for cond in condns:
    T_low = condns[cond]['T'][0]
    T_hi = condns[cond]['T'][1]
    T_av = np.array(condns[cond]['T']).mean()
    clr = condns[cond]['color']
    solv_corr = condns[cond]['solv_corr']
    selobj = selclass(conv_vec,dftobj,color=clr)
    selobj.fun_err(ax,plugerr,dEa-solv_corr,T_av,T_low=T_low,T_hi=T_hi)

######## Plot EXPERIMENTAL DATA ######
catlistobj = catlistobj.classfilter(lambda x: x.cattype !='MMO')
labels=[]
for pt in catlistobj.data:
    #label = '%s-%s, %s'%(pt.cat,pt.cattype,pt.author)
    label = pt.category
    if label in labels:
        label = None
    else:
        labels.append(label)
    ax.plot(pt.log_conv,pt.sel,'o',color=get_color(pt.category),marker='o',label=label,fillstyle='full',markersize=ptsize,clip_on=False)
    ax.text(pt.log_conv,pt.sel,str(pt.T),fontsize=7,ha='center',va='center',color='k')

###### PLOT PARAMETERS #####

ax.set_xlim(-8,0)
plt.legend(loc=3,fontsize=10)
ax.set_ylim(0,100)
ax.set_xlabel(r'log(CH$_4$ conversion)')
ax.set_ylabel(r'CH$_3$OH selectivity (%)')
plt.tight_layout()
plt.savefig('fig-5-aq.pdf')
