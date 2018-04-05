#!/usr/bin/env python

from ase import Atoms
from ase.io import read,write
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm
#from dG import *
#import vibclass
import math
from ase.units import kB


class expclass:
    """
    """
    
    '''
    shape_dict = {'Panov':'o',
            'Leshkov':'o',
            'Hutchings':'o',
            'Lobo':'o',
            'Dalton':'*',
            'ravi':'o',
            'sievers':'o',
            'Zhang':'o',
            'dowden':'o',
            'Weng':'o',
            'rooney':'o',
            'Chen':'o',
            'Wang':'o',
            'Durante':'o',
            'Wood':'o',
            }
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
    fill_dict = {
            'ZSM-5':'full',
            'SSZ-13':'full',
            'MOR':'full',
            'Silicalite':'full',
            'x':'full',
            'oxide':'full',
            }'''
    alpha_dict = {
            }

    def __init__(self,
            cat,
            cattype,
            T=None, 
            log_conv=None, 
            sel=None,
            author='',
            rxntype='gas',
            oxidant='O2',
            catalysis='heterogeneous',
            single_site = 'no',
            DOI = 'None', 
            tag=''):
        self.cat = cat
        self.cattype = cattype
        self.T = T
        self.log_conv = log_conv
        self.conv = 10**log_conv
        self.sel = sel
        self.author = author
        self.rxntype = rxntype
        self.oxidant = oxidant
        self.catalysis = catalysis
        self.single_site = single_site
        self.tag = tag
        self.DOI = DOI
        self.dEa = None
        '''
        if self.author in self.shape_dict:
            self.shape = self.shape_dict[self.author]
        else:
            self.shape = 'o'       
        if self.cat in self.clr_dict:
            self.clr = self.clr_dict[self.cat]
        else:
            self.clr = 'grey'       
        if self.cattype in self.fill_dict:
            self.fill = self.fill_dict[self.cattype]
        else:
            self.fill = 'full'
        '''
        return
   
    def get_dEa(self,dEa_guess,T,dftclasses_object,solv_corr=0.22,P=101325):
        def sel_fun(conv_vec,dGa,T):
            k2_k1 = math.exp(dGa/kB/T)
            sel = (1-conv_vec-(1-conv_vec)**(k2_k1))/(conv_vec*(k2_k1-1))
            return sel
        def dEa_min_fun(exp_dEa,T,S,X):
            dGa = exp_dEa + dftclasses_object.fun_dGcorr(T,P)
            diff = (sel_fun(X,dGa,T)*100-S)**2
            return diff
        bounds =[(0.1,1.2)]
        #For some reason, fit is tricky for this one point.  Need to 
        #tighten the bounds to get correct fit.
        if self.cattype == 'Zirconia':
            bounds = [(0.2,1.2)]
        dEa = minimize(dEa_min_fun,dEa_guess,args = (self.T,self.sel,10**self.log_conv),bounds=bounds).x[0]
        #Add on a solvation correction to fitted dEa if reaction conditions are aqueous
        if self.rxntype =='aqueous':
            dEa+=solv_corr
        self.dEa = dEa
        return
    
    def sel_fun(self,T,P,dftobj):
        dGa = self.dEa + dftobj.fun_dGcorr(T,P)
        k2_k1 = math.exp(dGa/kB/T)
        sel = (1-self.conv-(1-self.conv)**(k2_k1))/(self.conv*(k2_k1-1))*100
        return sel #in percent

class expclasses():
    """
    """
    def __init__(self,expclasses):
        self.data = expclasses
    
    def classfilter(self,fun,*args,**kwargs):
        """
        Takes list of objects and filters out those that do not give fun(object) == True.
        Returns new object
        """
        out = []
        for c in self.data:
            if fun.__name__ == '<lambda>': #lambda functions
                cbool = fun(c)
            else:
                cbool = fun(c,*args,**kwargs)
            if cbool:
                out.append(c)
        #print out
        return expclasses(out)

    def get_property(self,ppt):
        """
        Return list of property for each object
        """
        out = []
        for c in self.data:
            eval('out.append(c.%s)'%ppt)
        return np.array(out)

    def parity_fun(self,fun_dGcorr):
        plt.cla()
        for pt in self.data:
            #shape,clr,fill,size = pt.pointFun()
            dGa = dEa + dftclasses_object.fun_dGcorr(pt.T)
            model_sel = sel_fun(10**pt.log_conv,dGa,pt.T)*100
            ax.plot(pt.sel,model_sel,color=clr,fillstyle=fill,marker=pt.shape)
        ax.plot(np.arange(0,100,1),np.arange(0,100,1),'-')        
        return


