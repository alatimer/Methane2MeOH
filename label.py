#!/usr/bin/env python

from dftclass import dftclass,dftclasses
import pickle
#from ase import Atoms
#from ase.io import read,write
#import numpy as np


    #if obj.class == 'GN':
    #    obj.class='Graphene'
  #  elif obj.class == 'BN':
  #      obj.class = 'Boronitride'
  #  elif obj.class == 'porphyrin':
  #      obj.class = 'Porphyrin'
  #  elif obj.class == 'rutile-110':
  #      obj.class = 'Rutile(110)'
  #  elif obj.class == 'metal-111':
  #      obj.class = 'Metal(111)'



### make pickle file
#pickle.dump( dftclasses_obj, open( "dftobj.pkl", "wb" ) )
dco = pickle.load(open('dftobj.pkl','rb'))

for cat in dco.data:
    if cat.cattype == 'GN':
        cat.cattype='Graphene'
    if cat.cattype == 'BN':
        cat.cattype='Boronitride'
    if cat.cattype == 'metal-111':
        cat.cattype='Metal(111)'
    if cat.cattype == 'rutile-110':
        cat.cattype='Rutile(110)'
    if cat.cattype == 'porphyrin':
        cat.cattype='Porphyrin'

  
  
  #  elif obj.class == 'BN':
  #      obj.class = 'Boronitride'
  #  elif obj.class == 'porphyrin':
  #      obj.class = 'Porphyrin'
  #  elif obj.class == 'rutile-110':
  #      obj.class = 'Rutile(110)'
  #  elif obj.class == 'metal-111':
  #      obj.class = 'Metal(111)'


pickle.dump( dco, open( "dftobj.pkl", "wb" ) )
