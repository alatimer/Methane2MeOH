#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm
from ase.units import kB,_hplanck
import pickle
from Selectivity import sel_fun,plot_sel

##### PARAMETERS ######
solv_corr = 0.22
plttype = 'vary_T'#'vary_dGa' #gas,aq

### INITIALIZE PLOT #####
size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)
ptsize = 15 #size of markers

### Conversion Vector ###
conv_vec = np.logspace(-10,-.01,num=1e2,base=10)

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

for cond in condns:
    T_low = condns[cond]['T'][0]
    T_hi = condns[cond]['T'][1]
    T_av = np.array(condns[cond]['T']).mean()
    clr = condns[cond]['color']
    solv_corr = condns[cond]['solv_corr']
    dGa=condns[cond]['dGa']
    ax.plot(np.log10(conv_vec),sel_fun(conv_vec,T_av,dGa=dGa),color=clr)
    #plot_sel(ax,conv_vec,dEa,T_av,facecolor='w',color='k')

###### PLOT PARAMETERS #####
if plttype == 'gas':
    ax.set_xlim(-6,0)
else:
    ax.set_xlim(-8,0)
ax.set_ylim(0,100)
ax.set_xlabel(r'log(CH$_4$ conversion)')
ax.set_ylabel(r'CH$_3$OH selectivity (%)')
plt.tight_layout()
plt.savefig('fig-1X.pdf')
