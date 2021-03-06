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
dco = dco.filter(lambda x: x.vibs_ch3oh !=None)
#dco = dco.filter(lambda x: x.ets_ch3oh !=None)

#Conditions at which to evaluate dGcorr
P = 101325
T=300

plttype='$\Delta$ZPE' 
#plttype='$\Delta$G' 
#plttype='$\Delta$S' 
#plttype='$\Delta$C' 

nbins=6

dGcorr_list = []
dGcorr_dict={}
for cat in dco.data:
    #dGcorr =  -T*cat.get_dS(T) + cat.ets_ch4 - cat.ets_ch3oh
    
    if plttype=='$\Delta$ZPE' :
        dGcorr=cat.get_dZPE() #+ cat.ets_ch4 - cat.ets_ch3oh
        lims=[-0.2,0.2]
    if plttype=='$\Delta$G' :
        dGcorr = cat.ets_ch4 - cat.ets_ch3oh + cat.get_dGcorr(T,P) 
        lims=[-0.5,1]
    if plttype=='$\Delta$S' :
        dGcorr = cat.get_dS(T) 
        lims=[-0.0002,0.0011]
    if plttype=='$\Delta$C' :
        dGcorr = cat.get_dC(T) 
        lims=[-0.05,0.05]

    dGcorr_list.append(dGcorr)
    print cat.cat, cat.cattype
    if cat.cattype in dGcorr_dict.keys():
        dGcorr_dict[cat.cattype]['dGcorrs'].append(dGcorr)
    else:
        dGcorr_dict[cat.cattype] = {}
        dGcorr_dict[cat.cattype]['dGcorrs'] = [dGcorr]
        dGcorr_dict[cat.cattype]['clr'] = get_color(cat.cattype)
    #print cat.cat,'/',cat.cattype,'/',cat.vibs_ch4,'/',cat.vibs_ch3oh
 
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
#ax.set_xlim(-.75,0.25)
ax.set_xlim(lims)

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
plt.xlabel(r'%s'%(plttype)+'@ %i K'%(T))
#plt.xlabel(r'$\Delta$ZPE + $T\Delta$S @ %i K (eV)'%(T))
plt.legend(loc='best',fontsize=10)
plt.tight_layout()
plt.savefig('fig-S1-DFT-dGcorr-hist.pdf')
