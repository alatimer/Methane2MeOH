#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy.stats import norm
import pickle
from PointParameters import get_color

#Read in all DFT data (this work)
dftobj = pickle.load(open('dftobj.pkl','rb'))

#Can filter out HSE, or certain catalysts
#dftobj = dftobj.filter(lambda x: 'HSE' not in x.tag)
#dftobj = dftobj.filter(lambda x: x.cat=='RuO2')

dEa_dict={}
dEa_all = []
scaled=False

nbins = 5

for mat in dftobj.data:
    # Ensure material has CH4 Ea provided
    if mat.ets_ch4 !=None:
        # Can choose whether to get the distribution using the
        # true scaling (EaCH3OH = 0.94EaCH4+0.58) or approximate
        # slope = 1.  In pub, we approximate slope=1.
        if scaled == False:
            dEa = mat.ets_ch4 - mat.ets_ch3oh
        elif scaled == True:
            dEa = (mat.ets_ch3oh*0.94+0.58) - mat.ets_ch3oh
        mclass = mat.cattype
        if 'HSE' in mat.tag:
            mclass=mclass+'-HSE'
        if mclass in dEa_dict.keys():
            dEa_dict[mclass]['dEas'].append(dEa)
        else:
            dEa_dict[mclass] = {}
            dEa_dict[mclass]['dEas'] = [dEa]
            dEa_dict[mclass]['clr'] = get_color(mat.cattype)
            #dEa_dict[mclass]['clr'] = mat.color
        dEa_all.append(dEa)
        #print mat.cat,mat.cattype, mat.ets_ch4,mat.ets_ch3oh,dEa

dEa_multi = []
labels = []
colors=[]
hatches=[]
for mclass in dEa_dict:
    dEa_multi.append(np.array(dEa_dict[mclass]['dEas']))
    labels.append(mclass)
    colors.append(dEa_dict[mclass]['clr'])
    hatches.append('/')
n,bins,patches = plt.hist(dEa_multi,nbins,normed=1,label=labels,color = colors,stacked=True)
mu,std = norm.fit(dEa_all)
plt.xlim(0,1)
#  plt.ylim(0,8)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = r"Fit results: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std)
plt.ylabel(r'Counts')
plt.xlabel(r'$E^a_{CH_4} - E^a_{CH_3OH}$ (eV)')
plt.text(-0.1,-0.7,'(B)',fontsize=30)
plt.title(title)
plt.tight_layout()
plt.legend(fontsize=14,loc=2)

plt.savefig('fig-2b-DFT-dEa-hist.pdf')
