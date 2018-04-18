#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
#from analysis_functions import *
#from catclass import *
from scipy.stats import norm
import pickle

#mat_list = collect()
#print len(mat_list)

dftobj = pickle.load(open('dftobj.pkl','rb'))
dftobj = dftobj.filter(lambda x: x.tag!='surface-stabilized')
dftobj = dftobj.filter(lambda x: 'HSE' not in x.tag)
#dftobj = dftobj.filter(lambda x: x.cat=='RuO2')


dEa_dict={}
dEa_all = []
sep_class = False
beef_err = False
scaled = False
just_ruo2 = False

nbins = 5

if beef_err == True:
    nbins = 20
    Ea_ch3oh = []
    Ea_ch4 = []

for mat in dftobj.data:
    if mat.ets_ch4 !=None:
        if scaled == False:
            dEa = mat.ets_ch4 - mat.ets_ch3oh
        elif scaled == True:
            dEa = (mat.ets_ch3oh*0.94+0.58) - mat.ets_ch3oh
        mclass = mat.cattype
        if 'HSE' not in mat.tag:
            if mclass in dEa_dict.keys():
                dEa_dict[mclass]['dEas'].append(dEa)
            else:
                dEa_dict[mclass] = {}
                dEa_dict[mclass]['dEas'] = [dEa]
                
                dEa_dict[mclass]['clr'] = mat.color
        elif 'HSE' in mat.tag:
            key = mclass+'-HSE'
            if key in dEa_dict.keys():
                dEa_dict[key]['dEas'].append(dEa)
            else:
                dEa_dict[key] = {}
                dEa_dict[key]['dEas'] = [dEa]
                dEa_dict[key]['clr'] = mat.color


        if beef_err == True :
            if mat.beef_ch4 != None:
                for b_ch4,b_ch3oh in zip(mat.beef_ets_ch4,mat.beef_ets_ch3oh):
                    dEa_dict[mclass]['dEas'].append(b_ch4-b_ch3oh)
                    dEa_all.append(b_ch4-b_ch3oh)
                    Ea_ch4.append(b_ch4)
                    Ea_ch3oh.append(b_ch3oh)
        dEa_all.append(dEa)
        print mat.cat,mat.cattype, mat.ets_ch4,mat.ets_ch3oh,dEa


if sep_class == False:
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
    plt.title(title)
    plt.tight_layout()
    plt.legend(fontsize=10)

    plt.savefig('fig-hist.pdf')

    if just_ruo2 == True:
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
        plt.savefig('fig-Each4-beef.pdf')
        
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
        plt.savefig('fig-Each3oh-beef.pdf')

elif sep_class == True:
    for mclass in dEa_dict:
        nbins = 50
        if len(dEa_dict[mclass])< 50:
            continue
        n,bins,patches = plt.hist(dEa_dict[mclass]['dEas'],nbins,color=clrs_dict[mclass],normed=1)
        mu,std = norm.fit(dEa_dict[mclass]['dEas'])
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        nmat = len(dEa_dict[mclass]['dEas'])/2000
        title = "Class: %s , nmat: %4.2f \n Fit results: mu = %.2f,  std = %.2f" % (mclass,nmat,mu, std)
        plt.title(title)
        plt.tight_layout()
        plt.savefig('fig-sep-hists/fig-hist-%s.pdf'%(mclass))
        plt.clf()



