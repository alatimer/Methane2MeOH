#!/usr/bin/env python

from expclass import expclass,expclasses
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm



solv_corr=0.22#+0.09
dEa_guess=0.56
kb = 0.0000862
h = 4.14e-15
verbose=True
plttype = 'sep_cat'
nbins=4
normed=True
fit = True

catlistobj = pickle.load(open('expclasses_obj.pkl','rb'))
catlistobj = catlistobj.classfilter(lambda x: x.sel!=0)
catlistobj = catlistobj.classfilter(lambda x: x.cattype!='MMO')
if plttype != 'sep_ss':
    catlistobj = catlistobj.classfilter(lambda x: x.single_site=='yes')
#catlistobj = catlistobj.classfilter(lambda x: x.sel!=100)
#catlistobj = catlistobj.classfilter(lambda x: x.cattype!='Zirconia')
#catlistobj = catlistobj.classfilter(lambda x: x.rxntype=='gas')

#catlistobj = catlistobj.classfilter(lambda x: x.cat=='Fe')
#catlistobj = catlistobj.classfilter(lambda x: x.cat=='Cu')

#for dGcorr
dftclassesobj = pickle.load(open('dftclasses_obj.pkl','rb'))
dftclassesobj = dftclassesobj.filter(lambda x: x.vibs_ch4!=None)
dftclassesobj = dftclassesobj.filter(lambda x: x.cat=='Ni')
dftclassesobj = dftclassesobj.filter(lambda x: x.cattype=='BN')
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
        print "exp dEa = %4.2f for S=%4.2f and X=%4.2f %4.2f"%(pt.dEa,pt.sel,pt.log_conv,10**pt.log_conv)
    exp_dEa_list.append(pt.dEa)

if plttype=='no_sep':
    n,bins,patches = plt.hist(exp_dEa_list,nbins,normed=normed)

elif plttype == 'sep_cat':
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
        if cat in expclass.clr_dict.keys():
            colors.append(expclass.clr_dict[cat])
        else:
            colors.append('grey')
    n,bins,patches = plt.hist(dEa_multi,nbins,label=labels,color=colors,stacked=True,normed=normed)#kwargs
    plt.legend(fontsize=10)

elif plttype=='sep_ss':
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

if fit==True:
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
plt.savefig('fig-exp-dEa-hist.pdf')
