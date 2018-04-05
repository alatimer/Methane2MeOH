#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
import pickle
from matplotlib import colors
import matplotlib.cm as cmx

kB = 0.0000862 #eV*s
dS = -0.002 #eV/K
P0CH4 = 1.0
dEa = 0.55
logPCH3OH_real = -5

dftobj = pickle.load(open('dftobj.pkl','rb'))
dftobj = dftobj.filter(lambda x: x.vibs_ch4!=None)
dftobj = dftobj.filter(lambda x: x.cat=='Ni')
dftobj = dftobj.filter(lambda x: x.cattype=='Boronitride')

def lim_PCH3OH(dE,dS,T,theta_lim):
    dG = dE - T*dS
    PCH3OH = theta_lim/(1-theta_lim)*math.exp(dG/kB/T)
    #X = 10**logPCH3OH*math.exp(-dG/kB/T)
    #theta = X/(1+X)
    return PCH3OH

def fun_theta(logPCH3OH,dE,dS,T):
    dG = dE - T*dS
    X = 10**logPCH3OH*math.exp(-dG/kB/T)
    theta = X/(1+X)
    return theta

def deriv(y_vec,x_vec):
    dy_vec = np.zeros(y_vec.shape,np.float)
    dy_vec[0:-1] = np.diff(y_vec)/np.diff(x_vec)
    dy_vec[-1] = (y_vec[-1]-y_vec[-2])/(x_vec[-1]-x_vec[-2])
    return dy_vec

def sel_fun(conv_vec,dGa,T):
     k2_k1 = math.exp(dGa/kB/T)
     sel = (1-conv_vec-(1-conv_vec)**(k2_k1))/(conv_vec*(k2_k1-1))
     return sel

ECH3OH_vec = np.arange(-2.5,0,2.5/50)
T_vec = np.arange(300,900,600./50)
logPCH3OH_vec = np.arange(-20,1,0.1)
sel_grid = np.empty((ECH3OH_vec.shape[0],T_vec.shape[0]))
logP_grid = np.empty((ECH3OH_vec.shape[0],T_vec.shape[0]))
theta_lim = 0.5

for j,T in enumerate(T_vec):  
    dGcorr = dftobj.fun_dGcorr(T,101325)
    dGa = max(dEa + dGcorr,0)
    for i,dE in enumerate(ECH3OH_vec):
        logPCH3OH_thresh = math.log10(lim_PCH3OH(dE,dS,T,theta_lim))
        logPCH3OH_thresh = max(logPCH3OH_thresh,-15) #needed for some weird math problems
        #print dE,T,logPCH3OH_thresh
        conv = min(10**logPCH3OH_thresh/P0CH4,1) #assuming PCH4=1atm
        sel = sel_fun(conv,dGa,T)
        logP_grid[j][i]=logPCH3OH_thresh
        sel_grid[j][i] = max(0,min(sel,1))

### Plotting 2D Map
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
temp_plot = plt.contourf(ECH3OH_vec,T_vec,sel_grid,25)
plt.colorbar(temp_plot)
ax.set_ylabel('Temperature (K)')
ax.set_xlabel(r'Collector $E_{CH_3OH}$ (eV)')
ax.set_title('Selectivity')

#Add collector lines
collector_dict = {
        r'$GeO_2$':-1.24,
        r'$ZnO$':-1.46,
        r'$Al_2O_3$':-1.6,
        }
move=850
for col in collector_dict:
    move-=50
    clr = 'white'
    dE = collector_dict[col]
    ax.annotate(col,[dE,move],color=clr)
    plt.axvline(x=dE,color=clr,ls='--')
#Save figure
plt.tight_layout()
plt.savefig('fig-4b-collector.pdf')


###Plotting other fig
plt.clf()
ax2 = fig.add_subplot(111)
ax = ax2.twinx()
ax.set_ylabel('Selectivity (%)')
ax2.set_ylabel(r'$\Theta_{CH_3OH}$ ($Al_2O_3$)')#),rotation=270)
ax2.set_xlabel(r'$P_{CH_3OH}$')

T_range = np.arange(500,800,100)
cm = plt.get_cmap('gnuplot')
cNorm = colors.Normalize(vmin=0,vmax=len(T_range))
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

dE=-1.6 #for al2o3
for i,T in enumerate(T_range):
    clr = scalarMap.to_rgba(i)
    dGcorr = dftobj.fun_dGcorr(T,101325)
    dGa = max(dEa + dGcorr,0)
    theta_vec = fun_theta(logPCH3OH_vec,dE,dS,T)
    logPCH3OH_thresh = math.log10(lim_PCH3OH(dE,dS,T,theta_lim))
    sel_vec = sel_fun(10**logPCH3OH_vec,dGa,T)
    ax.plot(logPCH3OH_vec,sel_vec*100,label=str(T),color=clr,lw=3)
    ax2.plot(logPCH3OH_vec,theta_vec,'-',alpha=0.3,color='k',lw=3)
    plt.axvline(x=logPCH3OH_thresh,color=clr,lw=3,ls='--')

ax.set_xlim(-7,0)
ax.set_ylim(0,100)
ax2.set_ylim(0,1)
ax.axhline(y=0,linewidth=3, color="k")        # inc. width of x-axis and color it green
ax.axhline(y=100,linewidth=3, color="k")        # inc. width of x-axis and color it green
ax.axvline(x=0,linewidth=3, color="k")        # inc. width of y-axis and color it red
ax.axvline(x=-7,linewidth=3, color="k")        # inc. width of y-axis and color it red
ax.legend(loc=3,fontsize=10)
plt.tight_layout()
plt.savefig('fig-S8-theta-sel.pdf')

