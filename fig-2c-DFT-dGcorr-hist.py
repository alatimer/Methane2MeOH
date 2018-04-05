#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.stats import norm
from PointParameters import get_color

#Load DFT object
dco = pickle.load(open('dftobj.pkl','rb'))

#Filter out calculations that do not have vibrational analysis
dco = dco.filter(lambda x: x.vibs_ch4 !=None)

#Conditions at which to evaluate dGcorr
P = 101325
T=500

nbins=5

dGcorr_list = []
dGcorr_dict={}
for cat in dco.data:
    dGcorr = cat.get_dGcorr(T,P)
    dGcorr_list.append(dGcorr)
    print cat.cat, cat.cattype
    if cat.cattype in dGcorr_dict.keys():
        dGcorr_dict[cat.cattype]['dGcorrs'].append(dGcorr)
    else:
        dGcorr_dict[cat.cattype] = {}
        dGcorr_dict[cat.cattype]['dGcorrs'] = [dGcorr]
        dGcorr_dict[cat.cattype]['clr'] = get_color(cat.cattype)
    #print cat.cat,'/',cat.cattype,'/',cat.vibs_ch4,'/',cat.vibs_ch3oh
 
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-.75,0.25)

dGcorr_multi = []
labels=[]
colors=[]
for cattype in dGcorr_dict.keys():
    dGcorr_multi.append(np.array(dGcorr_dict[cattype]['dGcorrs']))
    labels.append(cattype)
    colors.append(dGcorr_dict[cattype]['clr'])

n,bins,patches = plt.hist(dGcorr_multi,nbins,normed=True,label=labels,color=colors,stacked=True)
mu,std = norm.fit(dGcorr_list)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)

ax.plot(x, p, 'k', linewidth=2)
title = r"Fit results: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std)
plt.title(title)
plt.ylabel('Counts')
plt.xlabel(r'$\Delta$ZPE + $T\Delta$S @ %i K (eV)'%(T))
plt.legend(fontsize=10)
plt.savefig('fig-2c-DFT-dGcorr-hist.pdf')
