#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.stats import norm
from PointParameters import get_color
import pylab

#Load DFT object
dco = pickle.load(open('dftobj.pkl','rb'))
#Filter out calculations that do not have vibrational analysis
vib_dco = dco.filter(lambda x: x.vibs_ch4 !=None)

#Conditions at which to evaluate dGcorr
P = 101325
Ts=np.arange(200,1000,10)

avg_dGcs = []
avg_dZPEs = []
avg_dSs = []
avg_dCvs = []
mu_stds = []
for T in Ts: 
    dGcorr_list = []
    dZPE_list = []
    dS_list = []
    dCv_list = []
    for cat in vib_dco.data:
        dGcorr = cat.get_dGcorr(T,P)
        dZPE = cat.get_dZPE()
        dCv = cat.get_dC(T)
        dCv_list.append(dCv)
        dS = cat.get_dS(T)
        dGcorr_list.append(dGcorr)
        dZPE_list.append(dZPE)
        dS_list.append(dS)
    mu,std = norm.fit(dGcorr_list)
    mu_stds.append([mu,std])
    avg_dGc = np.mean(np.array(dGcorr_list))
    avg_dGcs.append(avg_dGc)
    avg_dZPE = np.mean(np.array(dZPE_list))
    avg_dZPEs.append(avg_dZPE)
    avg_dS = np.mean(np.array(dS_list))
    avg_dSs.append(avg_dS)
    avg_dCv = np.mean(np.array(dCv_list))
    avg_dCvs.append(avg_dCv)

avg_dZPEs = np.array(avg_dZPEs)
mu_stds = np.array(mu_stds)
avg_dGcs = np.array(avg_dGcs)
avg_dCvs = np.array(avg_dCvs)
avg_ndST =  avg_dSs*Ts*-1.0

fig = plt.figure()
ax = fig.add_subplot(111)

p,C_p = np.polyfit(Ts,avg_dGcs,1,cov=True)
m,b=p
print "slope, intercept: ",m,b
print "Variance matrix: ", C_p
print "ZPEs: ",avg_dZPEs
print "avg_dSs: ",avg_dSs
print "avg_dCvs: ",avg_dCvs
print "avg -dST+dCv",avg_ndST+avg_dCvs

dEa=0.55

# Plot dGcor vs T
ax.plot(Ts, avg_dGcs+dEa, 'g', linewidth=4,label=r'$\Delta G^a (real)$')
ax.plot(Ts, m*Ts+b+dEa, 'k', linewidth=2,label=r'$\Delta G^a \approx \Delta E^a %.3e \cdot T  %4.4f$'%(m,b),alpha=0.5)
ax.plot(Ts, avg_dGcs+dEa+mu_stds[:,1]+0.08, 'g',linestyle= '--',linewidth=2) #std dev
ax.plot(Ts, avg_dGcs+dEa-mu_stds[:,1]-0.08, 'g',linestyle= '--',linewidth=2) #std dev
ax.fill_between(Ts,avg_dGcs+dEa-mu_stds[:,1]-0.08,avg_dGcs+dEa+mu_stds[:,1]+0.08,color='green',alpha=0.2)
ax.plot(Ts, avg_dZPEs, 'b', linewidth=2,label=r'$\Delta E_{ZPE}^a$',alpha=0.5)
ax.axhline( dEa, color='orange', linewidth=2,label=r'$\Delta E^a$',alpha=0.5)
ax.plot(Ts, avg_ndST, 'c', linewidth=2,label=r'$T \Delta S^a$',alpha=0.5)
ax.plot(Ts, avg_dCvs, 'r', linewidth=2,label=r'$\int_{0}^{T} \Delta C_v^a dT$',alpha=0.5)
#ax.plot(Ts, avg_dCvs+avg_dZPEs+avg_ndST, 'm', linewidth=2,label='all')
#ax.text(500,-0.5,r'$\Delta G^a \approx %.3e \cdot T  %4.4f$'%(m,b))
#title = r"Fit results: $\mu$ = %.2f,  $\sigma$ = %.2f" % (mu, std)
#plt.title(title)
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

ax.plot(Ts,sel_fun(1e-5,Ts,avg_dGcs,0.55),label='dGcorr ~ real')
ax.plot(Ts,sel_fun(1e-5,Ts,(m*Ts+b),0.55),label='dGcorr ~ linear fit')
ax.plot(Ts,sel_fun(1e-5,Ts,(avg_dZPEs-avg_dSs*Ts),0.55),label='dGcorr ~ cst entropy+ZPE')
ax.legend()
plt.savefig('k2k1_T.pdf')
