#!/usr/bin/env python

from expclass import expclass,expclasses
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from PointParameters import get_color

solv_corr=0.22
dEa_guess=0.56
kb = 0.0000862
h = 4.14e-15
verbose=True
nbins=4
normed=True

catlistobj = pickle.load(open('expobj.pkl','rb'))
#don't fit selectivites of 0 or 100 (rate), sigmoid is not well defined
catlistobj = catlistobj.classfilter(lambda x: x.sel!=0)
catlistobj = catlistobj.classfilter(lambda x: x.sel!=100)

#Don't plot MMO enzyme points
catlistobj = catlistobj.classfilter(lambda x: x.cattype!='MMO')

#Only plot data known to be single site catalysts
catlistobj = catlistobj.classfilter(lambda x: x.single_site=='yes')

#Can plot distributions for different active site types if desired
#catlistobj = catlistobj.classfilter(lambda x: x.cat=='Fe')
#catlistobj = catlistobj.classfilter(lambda x: x.cat=='Cu')

#for dGcorr
dftclassesobj = pickle.load(open('dftobj.pkl','rb'))
dftclassesobj = dftclassesobj.filter(lambda x: x.vibs_ch4!=None)
dftclassesobj = dftclassesobj.filter(lambda x: x.cat=='Ni')
dftclassesobj = dftclassesobj.filter(lambda x: x.cattype=='Boron-nitride')
clr_dict = {
	'Fe':'firebrick',
	'Cu':'goldenrod',
	'Cu-Fe':'firebrick',
	'Fe-MMO':'forestgreen',
	'V':'blue',
	'Mo':'m',
	'Ga':'green',
	'W':'orange',
	'Co':'cyan',
	'Ni':'pink',
	'Rh':'lightskyblue',
	'Au-Pd':'palegoldenrod',
	}

fig = plt.figure()
ax = fig.add_subplot(111)

exp_dEa_list = []
for pt in catlistobj.data:
    pt.get_dEa(dEa_guess,pt.T,dftclassesobj,solv_corr=solv_corr)
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
n,bins,patches = plt.hist(dEa_multi,nbins,label=labels,color=colors,stacked=True,normed=normed)#kwargs
plt.legend(fontsize=10)


mu,std = norm.fit(exp_dEa_list)
xmin, xmax = plt.xlim()
x = np.linspace(-.2, 2, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = r"Fit results: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std)
plt.title(title)

plt.ylabel(r'Counts')
#plt.xlabel(r'$\Delta E^a$ (eV)')
plt.xlabel(r'$E^a_{CH_4} - E^a_{CH_3OH}$ (eV)')
plt.xlim(0,1)
plt.ylim(0,6)
plt.tight_layout()
plt.savefig('fig-3b-EXP-dEa-hist.pdf')
