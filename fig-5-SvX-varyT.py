#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
import math
from ase.units import kB
import numpy as np
from PointParameters import get_color,get_shape
from Selectivity import plot_sel

##### load exp data #########
expclassesobj = pickle.load(open('expobj.pkl','rb'))
#remove exp data where no methanol observed
expclassesobj = expclassesobj.classfilter(lambda x: x.sel!=0)
#only include what are believed to be single-atom catalysts
expclassesobj = expclassesobj.classfilter(lambda x: x.single_site=='yes')
#exclude exp MMO, diffusion limited
expclassesobj = expclassesobj.classfilter(lambda x: x.cattype!='MMO')
#expclassesobj = expclassesobj.classfilter(lambda x: x.rxntype!='aqueous')

print len(expclassesobj.data)

solv_corr=0.22
dEa_theory=0.55
#dGcorr = -4.191e-4*T_fix-0.0152 
sigma = 0.07  #put in temperature dependence, check dGa spread for real

size=(5,4)
fig = plt.figure(1,figsize=size)
ax = fig.add_subplot(111)

#### Plot Model selectivity ####
conv_vec = np.logspace(-8,-.01,num=1e2,base=10)
step = 50
Ts = np.arange(275,950,step)


def sel_fun(conv,dEa,T,error=None):
    m_err = 8.744e-05 
    b_err = 0.0886
    dGa = dEa - 4.191e-4*T - 0.0152
    if error==None:
        print 'T, dGa : ',T,dGa
    if error=='+':
        #dGa+=0.07
        dGa+=(m_err*T+b_err)
        print "upper bound: ",dGa
    elif error=='-':
        #dGa-=0.07
        dGa-=(m_err*T+b_err)
        print "lower bound:", dGa
    k2_k1 = math.exp(dGa/kB/T)
    sel = (1-conv-(1-conv)**(k2_k1))/(conv*(k2_k1-1))*100
    return sel #in percent

#### Experimental points #####
for T in Ts:
    if T<424:
        condns = ['aqueous','gas']
    else:
        condns = ['gas']
    for condn in condns:
        labels=[]
        if condn == 'aqueous':
            dEa = dEa_theory-solv_corr
        else:
            dEa = dEa_theory
        plt.close('all')
        fig = plt.figure(1,figsize=size)
        ax = fig.add_subplot(111)

        plot_sel(ax,conv_vec,dEa,T,T_low=T-step/2.,T_hi=T+step/2.,facecolor='c',color='c')
        #ax.plot(np.log10(conv_vec),sel_fun(conv_vec,dEa,T))
        #ax.fill_between(np.log10(conv_vec),sel_fun(conv_vec,dEa,T,error='-'),sel_fun(conv_vec,dEa,T,error='+'),alpha=0.2)
        #V old error V
        #ax.fill_between(np.log10(conv_vec),sel_fun(conv_vec,dEa+sigma,T),sel_fun(conv_vec,dEa-sigma,T),alpha=0.2)
        count = 0
        for cat in expclassesobj.data:
            if cat.T >= T-step/2. and cat.T<=T+step/2. and cat.rxntype == condn:
                count+=1
                label = '%s'%(cat.category)
                #if cat.rxntype=='aqueous':
                #    label = None
                if label in labels:
                    label = None
                else:
                    labels.append(label)
                #plot experimental data with extrapolated selectivity
                ax.plot(cat.log_conv,
                        cat.sel,
                        color=get_color(cat.category),
                        marker=get_shape(cat.rxntype),
                        label=label,
                        fillstyle='full',
                        markersize=10,
                        clip_on=False)
                #ax.text(cat.log_conv,cat.sel,str(cat.T))
        
        if 1==1:#count != 0:
            ax.legend(loc='best',fontsize=10)
            ax.set_xlabel(r'log(CH$_4$ conversion)')
            ax.set_ylabel(r'CH$_3$OH selectivity (%)')
            ax.set_title('T=%i+/-%i K; %s'%(int(T),math.ceil(step/2.),condn))
            plt.tight_layout()
            plt.savefig('figs/fig-5-SvX-T%i-%s.pdf'%(int(T),condn))
