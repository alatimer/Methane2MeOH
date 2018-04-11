#!/usr/bin/env python

from expclass import expclass,expclasses
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from PointParameters import get_color
from matplotlib.legend import Legend

solv_corr=0.22
dEa_guess=0.56
kb = 0.0000862
h = 4.14e-15
verbose=True
nbins=4
normed=True
expcolor='firebrick'
theorycolor='k'

catlistobj = pickle.load(open('expobj.pkl','rb'))
#don't fit selectivites of 0 or 100 (rate), sigmoid is not well defined
catlistobj = catlistobj.classfilter(lambda x: x.sel!=0)
catlistobj = catlistobj.classfilter(lambda x: x.sel!=100)
#Don't plot MMO enzyme points
catlistobj = catlistobj.classfilter(lambda x: x.cattype!='MMO')
#Only plot data known to be single site catalysts
catlistobj = catlistobj.classfilter(lambda x: x.single_site=='yes')

fig = plt.figure()
ax = fig.add_subplot(111)

######################        EXPERIMENTAL FITTING         #############################

exp_dEa_list = []
#Fit a dEa for every exp data point
for pt in catlistobj.data:
    pt.get_dEa(dEa_guess,pt.T,solv_corr=solv_corr)
    if verbose==True:
        print "Catalyst: %s ; exp dEa = %4.2f for S=%4.2f and X=%4.2f %4.2f"%(pt.cat+'-'+pt.cattype,pt.dEa,pt.sel,pt.log_conv,10**pt.log_conv)
    exp_dEa_list.append(pt.dEa)

dEa_multi = []
labels = []
colors = []
dEa_dict = {}
for pt in catlistobj.data:
    if pt.cat in dEa_dict.keys():
        dEa_dict[pt.cat].append(pt.dEa)
    else:
        dEa_dict[pt.cat] = [pt.dEa]
for cat in dEa_dict:
    dEa_multi.append(np.array(dEa_dict[cat]))
    labels.append(cat)
    colors.append(get_color(cat))
    #if cat in expclass.clr_dict.keys():
    #    colors.append(expclass.clr_dict[cat])
    #else:
    #    colors.append('grey')

n,bins,patches = plt.hist(exp_dEa_list,nbins,color=expcolor,normed=normed,alpha=0.5)#kwargs
#n,bins,patches = plt.hist(dEa_multi,nbins,label=labels,color=colors,stacked=True,normed=normed)#kwargs
plt.legend(fontsize=15,loc=2)
lines = []
mu,std = norm.fit(exp_dEa_list)
xmin, xmax = plt.xlim()
x = np.linspace(-.2, 2, 1000)
p = norm.pdf(x, mu, std)
h, = plt.plot(x, p, expcolor, linewidth=2)
lines.append(h)
ax.text(0.05,5.5,r"Experimental: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std),color=expcolor)

##########  LOAD THEORY FIT (from fig-2b)        ############3
dft_dEa_all = pickle.load(open('dEa_all.pkl','rb'))
dft_dEa_multi = pickle.load(open('dEa_multi.pkl','rb'))
dft_clrs = pickle.load(open('dEa_clrs.pkl','rb'))
#n,bins,patches = plt.hist(dft_dEa_multi,nbins,normed=1,label=labels,color = dft_clrs,stacked=True,alpha=0.2)
n,bins,patches = plt.hist(dft_dEa_all,nbins,normed=1,color = theorycolor,alpha=0.2)
mu,std = norm.fit(dft_dEa_all)
xmin, xmax = plt.xlim()
x = np.linspace(-.2, 2, 1000)
p = norm.pdf(x, mu, std)
h, = plt.plot(x, p, theorycolor,linestyle='-', linewidth=2)
lines.append(h)

leg = Legend(ax,lines,['Experiment','Theory'],loc='upper right')
ax.add_artist(leg);

ax.text(0.05,5.2,r"Theory: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std),color=theorycolor)

plt.text(-0.105,-0.7,'(b)',fontsize=30)
plt.ylabel(r'Counts')
#plt.xlabel(r'$\Delta E^a$ (eV)')
plt.xlabel(r'$\Delta E^a_{exp}$ (eV)',fontsize=20)
plt.xlim(0,1)
plt.ylim(0,6)
plt.tight_layout()
plt.savefig('fig-3b-EXP-dEa-hist.pdf')
