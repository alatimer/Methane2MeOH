#!/usr/bin/env python

import pickle
import matplotlib.pyplot as plt
import math
from ase.units import kB
import numpy as np
from PointParameters import get_color,get_shape
from Selectivity import plot_sel,sel_fun

##### load exp data #########
expclassesobj = pickle.load(open('expobj.pkl','rb'))
#remove exp data where no methanol observed
expclassesobj = expclassesobj.classfilter(lambda x: x.sel!=0)
expclassesobj = expclassesobj.classfilter(lambda x: x.T<700)
expclassesobj = expclassesobj.classfilter(lambda x: x.rxntype=='gas')
#only include what are believed to be single-atom catalysts
expclassesobj = expclassesobj.classfilter(lambda x: x.single_site=='yes')
#exclude exp MMO, diffusion limited
expclassesobj = expclassesobj.classfilter(lambda x: x.cattype!='MMO')

solv_corr=0.22
dEa_guess=0.55
T_fix=700
P = 101325

#### Plot Model selectivity ####
conv_vec = np.logspace(-5,-.01,num=1e2,base=10)

print "catalyst  type    dEa    log_conv    sel     T   DOI"
#### Plot Experimental points #####
labels=[]
for cat in expclassesobj.data:
    label = '%s-%s, %s'%(cat.cat,cat.cattype,cat.author)
    label = '%s'%(cat.category)
    if label in labels:
        label = None
    else:
        labels.append(label)

    #assign cat object a dEa
    cat.get_dEa(dEa_guess,cat.T,solv_corr=solv_corr)

    if cat.dEa<=0.55:
        print cat.cat,cat.cattype,cat.dEa,cat.log_conv,cat.sel,cat.T,cat.DOI
    


#expclassesobj = expclassesobj.classfilter(lambda x: x.cattype=='ZSM-5')
#DOIs = set()
for cat in expclassesobj.data:
    DOIs.add(cat.DOI)
    print cat.cat,cat.cattype,cat.dEa,cat.log_conv,cat.sel,cat.T,cat.DOI
#print DOIs,len(DOIs)
