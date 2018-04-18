#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plt
from expclass import *
from scipy.optimize import minimize
from scipy.stats import norm
from ase.units import kB,_hplanck
from selclass import selclass

##### PARAMETERS ######
sigma = 0.07
err = sigma #change for desired uncertainty percentage
dEa = 0.55
solv_corr = 0.22
P=101325
plttype = 'gas'#'vary_dGa' #gas,aq

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

##### Import Exp Data ######
catlistobj = pickle.load(open('expclasses_obj.pkl','rb'))
#catlistobj = catlistobj.classfilter(lambda x: x.oxidant =='O2')
#catlistobj = catlistobj.classfilter(lambda x: x.single_site =='yes')
#catlistobj = catlistobj.classfilter(lambda x: x.sel !=0)
#catlistobj = catlistobj.classfilter(lambda x: x.author =='Panov')

#catlistobj = catlistobj.classfilter(lambda x: x.T <= 700 )
#catlistobj = catlistobj.classfilter(lambda x: x.T >= 540 )
#catlistobj = catlistobj.classfilter(lambda x: x.cattype == 'MMO' )
catlistobj = catlistobj.classfilter(lambda x: x.cat != 'Rh' )

###### Model Selectivity #######
if plttype == 'gas':
    plugerr=err
    catlistobj = catlistobj.classfilter(lambda x: x.rxntype =='gas')
    catlistobj = catlistobj.classfilter(lambda x: x.author =='Panov')
    condns = {}
    condns['panov']={'T':[543,573],'line':'-','color':'k','solv_corr':0}
    #condns['548']={'T':[540,700],'line':'-','color':'k','solv_corr':0}

elif plttype == 'aq':
    plugerr=err
    catlistobj = catlistobj.classfilter(lambda x: x.rxntype =='aqueous')
    condns={}

    condns['323']={'T':[323,323],'line':'-','color':'c','solv_corr':solv_corr}
    condns['323g']={'T':[323,323],'line':'-','color':'b','solv_corr':0}
 
elif plttype == 'mmo':
    plugerr=err
    catlistobj = catlistobj.classfilter(lambda x: x.cattype =='MMO')
    condns={}

    condns['323']={'T':[303,303],'line':'-','color':'c','solv_corr':0,'dGa':0.05}
    #condns['dalton']=[300,0.00,'-','m']
    lim_sel = -(1-conv_vec)*np.log(1-conv_vec)/conv_vec 
    ax.plot(np.log10(conv_vec),lim_sel*100,color='m',ls='-',label=None)

elif plttype == 'vary_T':
    condns = {}
    #condns['panov']={'T':[543,573],'line':'-','color':'k','solv_corr':0}
    condns['300']={'T':[300,300],'line':'-','color':'k','solv_corr':0}
    condns['400']={'T':[400,400],'line':'-','color':'k','solv_corr':0}
    condns['500']={'T':[500,500],'line':'-','color':'k','solv_corr':0}
    condns['600']={'T':[600,600],'line':'-','color':'k','solv_corr':0}
    condns['700']={'T':[700,700],'line':'-','color':'k','solv_corr':0}

elif plttype == 'vary_dGa':
    condns = {}
    #condns['panov']={'T':[543,573],'line':'-','color':'k','solv_corr':0}
    #condns['-0.1']={'T':[500,500],'line':'-','color':'k','solv_corr':0}
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
    if plttype == 'gas' or plttype=='aq':# or plttype=='mmo':
        selobj.fun_err(ax,plugerr,dEa-solv_corr,T_av,T_low=T_low,T_hi=T_hi)
    else:
        dGa=condns[cond]['dGa']
        if plttype == 'vary_dGa' or plttype == 'vary_both' or plttype=='mmo':
            sel_vec = selobj.sel_fun(dEa,T_av,P,dGa=dGa)
        else:
            sel_vec = selobj.sel_fun(dEa-solv_corr,T_av,P,dGa=0.4)
        #print sel_vec
        ax.plot(np.log10(conv_vec),sel_vec,color=clr)

######## Plot EXPERIMENTAL DATA ######
if 1==1:#plttype == 'aq' or plttype=='gas':
    catlistobj = catlistobj.classfilter(lambda x: x.cattype !='MMO')
    labels=[]
    for pt in catlistobj.data:
        #label = '%s-%s, %s'%(pt.cat,pt.cattype,pt.author)
        label = pt.cat
        if label in labels:
            label = None
        else:
            labels.append(label)
        ax.plot(pt.log_conv,pt.sel,'o',color=pt.clr,marker='o',label=label,fillstyle=pt.fill,markersize=ptsize,clip_on=False)
        ax.text(pt.log_conv,pt.sel,str(pt.T),fontsize=7,ha='center',va='center',color='k')

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
plt.savefig('fig-sel-conv.pdf')
