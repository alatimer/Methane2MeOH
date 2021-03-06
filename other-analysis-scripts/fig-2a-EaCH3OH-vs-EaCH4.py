#!/usr/bin/env python 

import matplotlib.pyplot as plt
import numpy as np
#from dftclass import dftclass,dftclasses
from matplotlib.patches import Ellipse
import pylab
import math
from scipy.stats import norm
import pickle
from PointParameters import get_color,get_shape
import copy

def PCA_ellipse(xi,yi,ax,**ellipse_kwargs):
    xy = np.array(zip(xi-xi.mean(),yi-yi.mean()))
    U,S,V = np.linalg.svd(xy,full_matrices=True)
    S /= np.sqrt(len(xi))
    if S[0] >= S[1]:
        Pvec = V[0,:]
    else:
        Pvec = V[1,:]
    theta = np.arctan(Pvec[1]/Pvec[0])*(180/np.pi)
    E = Ellipse(xy=[xi.mean(),yi.mean()], width=2*S[0], height=2*S[1],
             angle=theta,**ellipse_kwargs)
    ax.add_artist(E)

fig = plt.figure(figsize=(7,5))
ax = fig.add_subplot(111)

catlistobj = pickle.load(open('dftobj.pkl','rb'))
catlistobj = catlistobj.filter(lambda x: x.ets_ch4!=None)

beef_fit = False
ellipse_plot = True
surf_stab = False
make_legend = True

ch4_list = []
ch3oh_list = []
classes_idx = set() 
shape_handles=[]
clr_handles=[]
for cat in catlistobj.data:
    labeler = cat.cattype
    marker = 'o'#get_shape(cat.cattype)
    #cattype = cat.cattype
    if 'HSE' in cat.tag:
        #marker = 's'
        labeler+='-HSE'
    if labeler in classes_idx:
        label = '_nolegend_'
    else:
        label = labeler
    classes_idx.add(labeler)

    if 'surface-stabilized' in cat.tag:
        if surf_stab == False:
            continue
        clr = 'c'
    else:
        clr = get_color(labeler)
        ch3oh_list.append(cat.ets_ch3oh)
        ch4_list.append(cat.ets_ch4)
    alpha = 1 ##???
    h, = ax.plot(cat.ets_ch3oh,cat.ets_ch4,marker=marker,color=clr,alpha=alpha,label=label)
    clr_handles.append(copy.copy(h))
    shape_handles.append(copy.copy(h))
    #ax.text(cat.ets_ch3oh,cat.ets_ch4,cat.cat,fontsize=3,ha='center',va='center')
    

    ###  BEEF ##
    if cat.beef_ch4 != None:
        label='_nolegend_'
        ech4 = cat.beef_ets_ch4
        ech3oh = cat.beef_ets_ch3oh
        clr = get_color(labeler)
        if beef_fit == True:
            for a,b in zip(ech4,ech3oh):
                ch3oh_list.append(b)
                ch4_list.append(a)
        #either plot ellipse or collection of entire beef ensemble
        if ellipse_plot==True:
            alpha= 0.5
            PCA_ellipse(ech3oh,ech4,ax,alpha=alpha,color=clr)#,ec='k')
        else:
            alpha = 0.05
            ax.plot(ech3oh,ech4,'o',color=clr,marker=marker,alpha=alpha,label=label)


ch4_list = np.array(ch4_list)
ch3oh_list = np.array(ch3oh_list)
p,C_p = np.polyfit(ch3oh_list,ch4_list,1,cov=True)
mu,mu_std = norm.fit(ch4_list-ch3oh_list)
sigma_m, sigma_b = np.sqrt(np.diag(C_p))
m,b = p

err_vec = np.absolute(np.array(ch3oh_list)*m+b - np.array(ch4_list))
MAE = np.mean(err_vec)
print MAE


x_array = np.arange(-1.5,2.5,0.1)

ax.plot(x_array,x_array*m+b,color='k',zorder=1)
ax.plot(x_array,x_array*m+(b+mu_std),'--',color='k',zorder=1)
ax.plot(x_array,x_array*m+(b-mu_std),'--',color='k',zorder=1)

ax.set_xlabel(r'$E^a_{CH_3OH}$ (eV)',fontsize=20)
ax.set_ylabel(r'$E^a_{CH_4}$ (eV)',fontsize=20)

#for h in shape_handles:
#    h.set_color('k')

#for h in clr_handles:
#    h.set_marker('o')

if make_legend == True:
    #plt.legend(loc=3,fontsize=10,ncol=2,handles=shape_handles)
    plt.legend(loc=2,fontsize=13,ncol=2,handles=clr_handles)

if ellipse_plot==True:
    ax.set_xlim(-0.75,1.75)
    ax.set_ylim(0,2.5)
    ax.text(0.5,0.4,r'$E^a_{CH_4}=%4.2fE^a_{CH_3OH}+%4.2f$'%(m,b)+'\n'+r'$MAE=%4.2f$'%(MAE))
    plt.text(-1.1,-0.4,'(a)',fontsize=30)
else:
    ax.text(0,-0.5,'m=%4.2f\nb=%4.2f'%(m,b))

plt.tight_layout()
plt.savefig('fig-2a-EaCH3OH-vs-EaCH4.pdf')
