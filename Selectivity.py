#!/usr/bin/env python
from ase.units import kB
import math
import numpy as np
import matplotlib as plt

def dEa2dGa(dEa,T):
    return dEa - 3.942e-4*T - 0.0289

def err_fun(T):
    return 4.7e-5*T+0.0572

def sel_fun(conv,T,dEa=None,dGa=None,error=None):
    if dGa == None:
        dGa = dEa2dGa(dEa,T)
    if error=='+':
        dGa+=err_fun(T)
    elif error=='-':
        dGa-=err_fun(T)
    k2_k1 = math.exp(dGa/kB/T)
    sel = (1-conv-(1-conv)**(k2_k1))/(conv*(k2_k1-1))*100
    return sel #in percent

def plot_sel(ax,conv,dEa,T,T_low=None,T_hi=None,error=True,facecolor='w',**kwargs):

    #ax.plot(conv,sel_fun(conv,dEa,T),**kwargs)
    if T_low == None:
        T_low = T
    if T_hi == None:
        T_hi = T
    alphamin = 0.01
    alphamax = 0.3
    
    ## Sigmoids
    dGa_lo = dEa2dGa(dEa,T)-err_fun(T)
    dGa_hi = dEa2dGa(dEa,T)+err_fun(T)
    dGa_vec = np.arange(dGa_lo,dGa_hi,err_fun(T)/6.)
    for i,dGa in enumerate(dGa_vec):
        if i < len(dGa_vec)/2:
            alpha = alphamin + 2*i*(alphamax-alphamin)/len(dGa_vec)
        elif i  == len(dGa_vec)/2:
            alpha = 1
        else:
            alpha = alphamax - 2*(i-len(dGa_vec)/2.)*(alphamax - alphamin)/len(dGa_vec)
        sel = sel_fun(conv,T,dGa=dGa)
        ax.plot(np.log10(conv),sel,alpha=alpha,**kwargs)

    sel_low = sel_fun(conv,T_hi,dGa=dGa_lo)
    sel_high = sel_fun(conv,T_low,dGa=dGa_hi)
    ax.fill_between(np.log10(conv), sel_high, sel_low, alpha=0.1,facecolor=facecolor, interpolate=True)

    return


