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
dEa_theory=0.46
sigma = 0.08
P = 101325

size=(8,6)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)

def sel_fun(conv,dEa,T):
    dGa = dEa - 4.191e-4*T - 0.0152
    k2_k1 = math.exp(dGa/kB/T)
    sel = (1-conv-(1-conv)**(k2_k1))/(conv*(k2_k1-1))*100
    return sel #in percent

labels=[]
for obj in expclassesobj.data:
    if obj.rxntype=='aqueous':
        dEa = dEa_theory-solv_corr
    else:
        dEa = dEa_theory
    label=obj.category
    if label in labels:
        label=None
    else:
        labels.append(label)
    sel_pred = sel_fun(obj.conv,dEa,obj.T)
    print obj.sel,sel_pred
    #xerr=math.log((-sel_pred+sel_fun(obj.conv,dEa-sigma,obj.T))*0.01,10)
    xerr=0
    ax.errorbar(math.log(sel_pred*.01,10),math.log(obj.sel*.01,10),xerr=xerr,marker='o',label=label,color=get_color(obj.category))

ax.plot(np.arange(-6,1,1),np.arange(-6,1,1))
ax.set_title(r'$\Delta E^a_{theory} = %4.2f$'%(dEa_theory))
ax.set_ylim([-3,0])
ax.set_xlim([-3,0])
ax.set_ylabel('Experimental log(Selectivity)')
ax.set_xlabel('Model log(Selectivity)')
ax.legend(loc='best',fontsize=9)
plt.savefig('parity-dEa-%4.2f.pdf'%(dEa_theory))
