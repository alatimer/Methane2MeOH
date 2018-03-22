#!/usr/bin/env python
### def selclass
from ase.units import kB
import math
import numpy as np
import matplotlib as plt


class selclass:
    """
    """
    def __init__(self,conv_vec,dftobj,color='k'):
        self.conv_vec = conv_vec
        self.dftobj = dftobj  
        self.color=color 
        self.logconv_vec = np.log10(conv_vec)
        return 

    def sel_fun(self,dEa,T,P,dGa=None):
        if dGa==None:
            dGa = dEa + self.dftobj.fun_dGcorr(T,P)
        k2_k1 = math.exp(dGa/kB/T)
        sel = (1-self.conv_vec-(1-self.conv_vec)**(k2_k1))/(self.conv_vec*(k2_k1-1))*100
        return sel #in percent

    def fun_err(self,ax,err,dEa,T,P=101325,T_low=None,T_hi=None,plttype='all'):
        if T_low == None:
            T_low = T
        if T_hi == None:
            T_hi = T
        alphamin = 0.01
        alphamax = 0.3
        
        ## Sigmoids
        dEa_vec = np.arange(dEa-err,dEa+err,err/6.)
        for i,dEa_pt in enumerate(dEa_vec):
            if i < len(dEa_vec)/2:
                if plttype == 'low':
                    alpha = 0
                else:
                    alpha = alphamin + 2*i*(alphamax-alphamin)/len(dEa_vec)
            elif i  == len(dEa_vec)/2:
                alpha = 1
            else:
                if plttype == 'high':
                    alpha = 0
                else:
                    alpha = alphamax - 2*(i-len(dEa_vec)/2.)*(alphamax - alphamin)/len(dEa_vec)
            sel = self.sel_fun(dEa_pt,T,P)
            ax.plot(self.logconv_vec,sel,ls='-',color=self.color,alpha=alpha)

        ### Fill
        if plttype == 'low':
            sel_low = self.sel_fun(dEa,T,P)
            sel_high = self.sel_fun((dEa+err),T_low,P)
        elif plttype == 'high':
            sel_low = self.sel_fun((dEa-err),T_hi,P)
            sel_high = self.sel_fun(dEa,T_low,P)
        elif plttype=='all':
            sel_low = self.sel_fun((dEa-err),T_hi,P)
            sel_high = self.sel_fun((dEa+err),T_low,P)
        ax.fill_between(self.logconv_vec, sel_high, sel_low, alpha=0.1,facecolor=self.color, interpolate=True)

        return


