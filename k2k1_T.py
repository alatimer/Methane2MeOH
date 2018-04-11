#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.stats import norm
from PointParameters import get_color
import pylab
import math

#Load DFT object
dco = pickle.load(open('dftobj.pkl','rb'))
#Filter out calculations that do not have vibrational analysis
vib_dco = dco.filter(lambda x: x.vibs_ch4 !=None)

#Conditions at which to evaluate dGcorr
P = 101325 #doesnt affect results, dummy P
Ts=np.arange(200,1000,100)
dEa=0.55

avg_dGcs = []
avg_dZPEs = []
avg_dSs = []
avg_dCvs = []
mu_stds = []

dmT = {}
dmT['dZPE'] = np.zeros((Ts.shape[0],len(vib_dco.data)))
dmT['dS'] = np.zeros((Ts.shape[0],len(vib_dco.data)))
dmT['dCv'] = np.zeros((Ts.shape[0],len(vib_dco.data)))
dmT['dGc'] = np.zeros((Ts.shape[0],len(vib_dco.data)))
dmT['dG'] = np.zeros((Ts.shape[0],len(vib_dco.data)))
dmT['nTdS'] = np.zeros((Ts.shape[0],len(vib_dco.data)))
dmT['dE'] = np.zeros((Ts.shape[0],len(vib_dco.data)))
print dmT
for i,T in enumerate(Ts): 
    for j,cat in enumerate(vib_dco.data):
        dmT['dGc'][i][j] = cat.get_dGcorr(T,P)
        dmT['dZPE'][i][j] = cat.get_dZPE()
        dmT['dS'][i][j] = cat.get_dS(T)
        dmT['nTdS'][i][j] = -T*cat.get_dS(T)
        dmT['dCv'][i][j] = cat.get_dC(T)
        dmT['dG'][i][j] = cat.get_dGcorr(T,P)+cat.ets_ch4-cat.ets_ch3oh
        dmT['dE'][i][j] = cat.ets_ch4-cat.ets_ch3oh

fig2=plt.figure(figsize=(8,8))
ax1 = fig2.add_subplot(221)
ax2 = fig2.add_subplot(222)
ax3 = fig2.add_subplot(223)
ax4 = fig2.add_subplot(224)
axes = [ax1,ax2,ax3,ax4]

fig = plt.figure()
ax = fig.add_subplot(111)

labels= {'dZPE':r'$\Delta E_{ZPE}^a$',
         'dS':r'$ \Delta S^a$',
         'nTdS':r'$-T \Delta S^a$',
         'dGc':r'$\Delta G^a_{corr}$',
         'dG':r'$\Delta G^a (real)$',
         'dCv':r'$\int_{0}^{T} \Delta C_v^a dT$',
         'dE':r'$\Delta E^a$',
         }
colors = ['b','c','r','m','green','pink','lightgreen']
j=0
for i,dX in enumerate(dmT.keys()):
    avg_vT = np.mean(dmT[dX],axis=1)
    std_vT = np.std(dmT[dX],axis=1)

    if dX in ['dS','dG','dZPE','dCv']:
        n,bins,patches = axes[j].hist(dmT[dX][0],5,normed=1)
        print dmT[dX][0]
        #axes[j].set_xlim([-.25,.75])
        #axes[j].set_ylim([0,8])
        xmin, xmax = axes[j].get_xlim()
        print xmin,xmax
        j+=1
    if dX in ['dS','dGc']:
        continue
    ax.fill_between(Ts,avg_vT+std_vT,avg_vT-std_vT,color=colors[i],alpha=0.2)
    ax.plot(Ts, avg_vT, linewidth=2,label=labels[dX],color=colors[i])
   
pylab.figure(fig2.number)
plt.savefig('spread.pdf')

p,C_p = np.polyfit(Ts,np.mean(dmT['dG'],axis=1),1,cov=True)
m,b=p
print "dGc linear fit: ",m,b
per,C_per = np.polyfit(Ts,np.std(dmT['dG'],axis=1),1,cov=True)
mer,ber=per
print "dG 1sigma linear fit: ",mer,ber

# Plot dGcor vs T
#ax.fill_between(Ts,avg_dGcs+dEa-mu_stds[:,1]-0.08,avg_dGcs+dEa+mu_stds[:,1]+0.08,color='green',alpha=0.2)
ax.plot(Ts, m*Ts+b, 'k',linestyle='--', linewidth=2,label=r'$%.3e \cdot T +  %4.4f$'%(m,b))
ax.plot(Ts, (m-mer)*Ts+(b-ber), 'grey',linestyle='--', linewidth=2,label=r'$\Delta G^a + %.3e \cdot T + %4.4f$'%(mer,ber))
ax.plot(Ts, (m+mer)*Ts+(b+ber), 'grey',linestyle='--', linewidth=2,label=None)
#ax.plot(Ts, m*Ts+b+dEa, 'k', linestyle='--', linewidth=2,label=r'$\Delta E^a %.3e \cdot T  %4.4f$'%(m,b),alpha=1)
#ax.plot(Ts, avg_dGcs+dEa+mu_stds[:,1]+0.08, 'g',linestyle= '--',linewidth=2) #std dev
#ax.plot(Ts, avg_dGcs+dEa-mu_stds[:,1]-0.08, 'g',linestyle= '--',linewidth=2) #std dev
#ax.plot(Ts, avg_dZPEs, 'b', linewidth=2,label=r'$\Delta E_{ZPE}^a$',alpha=0.5)
#ax.axhline( dEa, color='orange', linewidth=2,label=r'$\Delta E^a$',alpha=0.5)
#ax.plot(Ts, avg_ndST, 'c', linewidth=2,label=r'$T \Delta S^a$',alpha=0.5)
#ax.plot(Ts, avg_dCvs, 'r', linewidth=2,label=r'$\int_{0}^{T} \Delta C_v^a dT$',alpha=0.5)
#ax.plot(Ts, avg_dCvs+avg_dZPEs+avg_ndST, 'm', linewidth=2,label='all')
#ax.text(500,-0.5,r'$\Delta G^a \approx %.3e \cdot T  %4.4f$'%(m,b))
ax.set_ylim(-1,0.75)
ax.set_xlim(250,900)
plt.ylabel(r'$\Delta G^a$ (eV)')
plt.xlabel('T (K)')
plt.legend(fontsize=13,loc='lower left')
plt.savefig('dGcorr_T.pdf')


plt.cla()
kB=0.00008617

def sel_fun(conv_vec,T,dGcorr_vec,dEa):
    k2_k1 = np.exp((dGcorr_vec+dEa)/kB/T)
    sel = (1-conv_vec-(1-conv_vec)**(k2_k1))/(conv_vec*(k2_k1-1))*100
    return sel

conv_vec = np.logspace(-7,-.01,num=5,base=10)
clrs = ['b','r','g','m','c']

'''
for conv,clr in zip(conv_vec,clrs):
    ax.plot(Ts,sel_fun(conv,Ts,avg_dGcs,0.55),color=clr,linestyle='-',label='Real; log(X)= %4.2f'%(math.log(conv,10)))
    ax.plot(Ts,sel_fun(conv,Ts,(m*Ts+b),0.55),color='k',linestyle='--',label='Linear fit')
    #ax.plot(Ts,sel_fun(conv,Ts,(avg_dZPEs-avg_dSs*Ts),0.55),label='dGcorr ~ cst entropy+ZPE')
ax.legend(loc='best')
ax.set_ylabel('Selectivity')
ax.set_xlabel('log(Conversion)')
plt.savefig('k2k1_T.pdf')
'''
