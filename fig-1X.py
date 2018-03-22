#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm
from ase.units import kB,_hplanck
from selclass import selclass
import pickle

##### PARAMETERS ######
sigma = 0.07
err = sigma #change for desired uncertainty percentage
dEa = 0.55
solv_corr = 0.22
P=101325
plttype = 'vary_T'#'vary_dGa' #gas,aq

### INITIALIZE PLOT #####
size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)
ptsize = 15 #size of markers
#font params?

### Conversion Vector ###
conv_vec = np.logspace(-10,-.01,num=1e2,base=10)

### Import DFT Data #######
dftobj = pickle.load(open('dftclasses_obj.pkl','rb'))
dftobj = dftobj.filter(lambda x: x.vibs_ch4!=None)

###### Model Selectivity #######
if plttype == 'vary_T':
    condns = {}
    condns['300']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.4}
    condns['400']={'T':[400,400],'line':'-','color':'k','solv_corr':0,'dGa':0.4}
    condns['500']={'T':[500,500],'line':'-','color':'k','solv_corr':0,'dGa':0.4}
    condns['600']={'T':[600,600],'line':'-','color':'k','solv_corr':0,'dGa':0.4}
    condns['700']={'T':[700,700],'line':'-','color':'k','solv_corr':0,'dGa':0.4}

elif plttype == 'vary_dGa':
    condns = {}
    condns['1e-5']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':1e-5}
    condns['0.1']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.1}
    condns['0.2']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.2}
    condns['0.3']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.3}
    condns['0.4']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.4}
   # condns['0.5']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.5}
   # condns['0.6']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.6}
   # condns['0.7']={'T':[300,300],'line':'-','color':'k','solv_corr':0,'dGa':0.7}

elif plttype == 'vary_both':
    condns={}
    temps = [300,700]
    dGas = [0.00001,0.2,0.3]
    clrs = ['c','b','g','m']
    for temp,clr in zip(temps,clrs):
        for dGa in dGas:
            condns[str(dGa)+str(temp)]={'T':[temp,temp],'line':'-','color':clr,'solv_corr':0,'dGa':dGa}
    print temps,dGas

for cond in condns:
    T_low = condns[cond]['T'][0]
    T_hi = condns[cond]['T'][1]
    T_av = np.array(condns[cond]['T']).mean()
    clr = condns[cond]['color']
    solv_corr = condns[cond]['solv_corr']
    selobj = selclass(conv_vec,dftobj,color=clr)
    dGa=condns[cond]['dGa']
    sel_vec = selobj.sel_fun(dEa,T_av,P,dGa=dGa)
    ax.plot(np.log10(conv_vec),sel_vec,color=clr)


###### PLOT PARAMETERS #####
if plttype == 'gas':
    ax.set_xlim(-6,0)
else:
    ax.set_xlim(-8,0)
#plt.legend(loc=3,fontsize=10)
ax.set_ylim(0,100)
ax.set_xlabel(r'log(CH$_4$ conversion)')
ax.set_ylabel(r'CH$_3$OH selectivity (%)')
plt.tight_layout()
plt.savefig('fig-1X.pdf')
