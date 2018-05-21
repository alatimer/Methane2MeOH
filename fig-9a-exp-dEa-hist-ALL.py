#!/usr/bin/env python

from expclass import expclass,expclasses
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

solv_corr=0.22
dEa_guess=0.55
kb = 0.0000862
h = 4.14e-15
verbose=True
nbins=6
normed=True

catlistobj = pickle.load(open('expobj.pkl','rb'))
catlistobj = catlistobj.classfilter(lambda x: x.sel!=0)
catlistobj = catlistobj.classfilter(lambda x: x.sel!=100)
catlistobj = catlistobj.classfilter(lambda x: x.cattype!='MMO')

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

exp_dEa_list = []
for pt in catlistobj.data:
    pt.get_dEa(dEa_guess,pt.T,solv_corr=solv_corr)
    if verbose==True:
        print "exp dEa = %4.2f for S=%4.2f and X=%4.2f %4.2f"%(pt.dEa,pt.sel,pt.log_conv,10**pt.log_conv)
    exp_dEa_list.append(pt.dEa)


dEa_multi = []
labels = []
colors = ['grey','c']
dEa_dict={'yes':[],'no':[]}
for pt in catlistobj.data:
    dEa_dict[pt.single_site].append(pt.dEa)
for ss in dEa_dict:
    dEa_multi.append(np.array(dEa_dict[ss]))
    labels.append(ss)
n,bins,patches = plt.hist(dEa_multi,nbins,label=labels,color=colors,stacked=True,normed=normed)#kwargs
#plt.legend(fontsize=10)

plt.text(0.1,-0.7,'(a)',fontsize=25)
plt.ylabel(r'Counts')
plt.xlabel(r'$\Delta E^a_{exp}$ (eV)')
#plt.xlabel(r'$E^a_{CH_4} - E^a_{CH_3OH}$ (eV)')
#plt.xlim(0,1)
plt.ylim(0,4)
plt.tight_layout()
plt.text(0.2,-0.4,'(a)',fontsize=30)
plt.savefig('fig-9a-exp-dEa-hist-ALL.pdf')
