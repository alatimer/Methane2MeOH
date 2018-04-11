#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy.stats import norm
import pickle
from PointParameters import get_color

#mat_list = collect()
#print len(mat_list)

dftobj = pickle.load(open('dftobj.pkl','rb'))
#dftobj = dftobj.filter(lambda x: x.tag!='surface-stabilized')
#dftobj = dftobj.filter(lambda x: 'HSE' not in x.tag)
dftobj = dftobj.filter(lambda x: x.cat=='Ru')
dftobj = dftobj.filter(lambda x: x.cattype=='Rutile(110)')

print len(dftobj.data)

dEa_dict={}
dEa_all = []

nbins = 5

nbins = 20
Ea_ch3oh = []
Ea_ch4 = []

for mat in dftobj.data:
    dEa = mat.ets_ch4 - mat.ets_ch3oh
    mclass = mat.cattype
    if mclass in dEa_dict.keys():
        dEa_dict[mclass]['dEas'].append(dEa)
    else:
        dEa_dict[mclass] = {}
        dEa_dict[mclass]['dEas'] = [dEa]
        dEa_dict[mclass]['clr'] = get_color(mat.cattype)
    for b_ch4,b_ch3oh in zip(mat.beef_ets_ch4,mat.beef_ets_ch3oh):
        dEa_dict[mclass]['dEas'].append(b_ch4-b_ch3oh)
        dEa_all.append(b_ch4-b_ch3oh)
        Ea_ch4.append(b_ch4)
        Ea_ch3oh.append(b_ch3oh)
    dEa_all.append(dEa)
    print mat.cat,mat.cattype, mat.ets_ch4,mat.ets_ch3oh,dEa


labels = []
colors=[]
for mclass in dEa_dict:
    labels.append(mclass)
    colors.append(dEa_dict[mclass]['clr'])
n,bins,patches = plt.hist(dEa_all,nbins,normed=1,label=labels,color = colors,stacked=True)
mu,std = norm.fit(dEa_all)
plt.xlim(0,2)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = r"Fit results: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std)
plt.ylabel(r'Counts')
plt.xlabel(r'$E^a_{CH_4} - E^a_{CH_3OH}$ (eV)')
plt.title(title)
plt.tight_layout()
plt.legend(fontsize=10)
plt.savefig('fig-S7c-beef-RuO2-ECH4-ECH3OH.pdf')

plt.cla()
n,bins,patches = plt.hist(Ea_ch4,nbins,normed=1,label=labels,color = colors,stacked=True)
mu,std = norm.fit(Ea_ch4)
plt.xlim(0,2)
#  plt.ylim(0,8)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = r"Fit results: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std)
plt.ylabel(r'Counts')
plt.xlabel(r'$E^a_{CH_4}$ (eV)')
plt.title(title)
plt.tight_layout()
plt.legend(fontsize=10)
plt.savefig('fig-S7a-beef-RuO2-ECH4.pdf')

plt.cla()
n,bins,patches = plt.hist(Ea_ch3oh,nbins,normed=1,label=labels,color = colors,stacked=True)
mu,std = norm.fit(Ea_ch3oh)
plt.xlim(-0.5,1.5)
#  plt.ylim(0,8)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = r"Fit results: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std)
plt.ylabel(r'Counts')
plt.xlabel(r'$E^a_{CH_3OH}$ (eV)')
plt.title(title)
plt.tight_layout()
plt.legend(fontsize=10)
plt.savefig('fig-S7b-beef-RuO2-ECH3OH.pdf')

