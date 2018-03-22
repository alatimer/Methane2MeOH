#!/usr/bin/env python

from dftclass import dftclass,dftclasses
import pickle
#from ase import Atoms
#from ase.io import read,write
#import numpy as np

def reader(file_name, dftclasses_obj):
    """
    appends new dftclass objects to dftclasses_obj from a file 
    with correct format
    """
    for i, line in enumerate(open(file_name, 'r').readlines()):
        if i == 0:
            labels = line.split()
        else:
            if line.startswith('#'):
                continue
            vals = line.split()
            cat = vals[labels.index('cat')]
            cattype = vals[labels.index('cattype')]
            ets_ch4 = float(vals[labels.index('ets_ch4')])
            ets_ch3oh = float(vals[labels.index('ets_ch3oh')])
            tag = vals[labels.index('tag')]
            cat_object = dftclass(cat, cattype, ets_ch4=ets_ch4, ets_ch3oh=ets_ch3oh, tag=tag)
            dftclasses_obj.data.append(cat_object)
    return dftclasses_obj


########## RUTILE OXIDES #############

RuO2 = dftclass('RuO2',
    'rutile-110',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/RuO2/methane/neb/beef/qn.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/RuO2/meoh/neb/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/RuO2/O/qn.traj',
#    vibloc_ch4='/home/alatimer/work_dir/meoh-vs-methane/RuO2/methane/neb/vib',
#    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/RuO2/meoh/neb/vib',

    )

IrO2 = dftclass('IrO2',
    'rutile-110',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/IrO2/methane/neb/no-spin/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/IrO2/meoh/neb/nospin/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/IrO2/O/wrong-spin/qn.traj',
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/IrO2/meoh/neb/vib',
    vibloc_ch4='/home/alatimer/work_dir/meoh-vs-methane/IrO2/methane/neb/vib',
    )

PtO2 = dftclass('PtO2',
    'rutile-110',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/PtO2/fixed-slab/methane/neb/beef/out.traj',
    traj_ch3oh='/scratch/users/alatimer/meoh-vs-methane/PtO2/fixed-slab/meoh/neb/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/PtO2/fixed-slab/O/qn.traj',
    vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/PtO2/fixed-slab/methane/neb/vib/' ,
    vibloc_ch3oh = '/home/alatimer/work_dir/meoh-vs-methane/PtO2/fixed-slab/meoh/neb/vib/',
    )

RhO2 = dftclass('RhO2',
    'rutile-110',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/RhO2/methane/qn.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/RhO2/meoh/neb/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/RhO2/O/qn.traj',
    vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/RhO2/methane/vib/' ,
    vibloc_ch3oh = '/home/alatimer/work_dir/meoh-vs-methane/RhO2/meoh/neb/vib/',
    )

######### METALS ########

Ag = dftclass('Ag',
    'metal-111',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Ag111/methane/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Ag111/meoh/neb/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Ag111/O/qn.traj',
    vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Ag111/methane/vib/' ,
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Ag111/meoh/neb/vib/',
                  )

Au = dftclass('Au',
    'metal-111',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Au111/methane/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Au111/meoh/final/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Au111/O/qn.traj')

Cu = dftclass('Cu',
    'metal-111',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Cu111/methane/qn.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Cu111/meoh/neb/beef/qn.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Cu111/O/qn.traj',
    vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Cu111/methane/vib/' ,
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Cu111/meoh/neb/vib/',
        )

Pd = dftclass('Pd',
    'metal-111',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Pd111/methane/neb/beef/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Pd111/meoh/neb/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Pd111/O/qn.traj',
    vibloc_ch4='/home/alatimer/work_dir/meoh-vs-methane/Pd111/methane/neb/vib',
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Pd111/meoh/neb/vib',
    
    )

Pt = dftclass('Pt',
    'metal-111',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Pt111/methane/neb/beef/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Pt111/meoh/neb/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Pt111/O/qn.traj',
    vibloc_ch4='/home/alatimer/work_dir/meoh-vs-methane/Pt111/methane/neb/vib',
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Pt111/meoh/neb/vib',

    )

Rh = dftclass('Rh',
    'metal-111',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Rh111/methane/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Rh111/meoh/neb/beef/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Rh111/O/qn.traj',
    vibloc_ch4='/home/alatimer/work_dir/meoh-vs-methane/Rh111/methane/vib',
    vibloc_ch3oh='/scratch/users/alatimer/meoh-vs-methane/Rh111/meoh/neb/vib',
    )

############ 2D MATERIALS ############

Rh_GN = dftclass('Rh',
    'GN', 
    #traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/methane/out.traj',
    #traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/meoh-lo/out.traj',
    #traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/O/out.traj',
    #traj_ch4g='/scratch/users/alatimer/gases/methane/beef-vdw/476-arv/qn.traj',
    #traj_ch3ohg='/scratch/users/alatimer/gases/methanol/arvin-beef-476/qn.traj',
    vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/methane-lo/vib/' ,
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/meoh-lo/vib/',

    )

Rh_GN_hi = dftclass('Rh-hi',
    'GN',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/methane/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/meoh-hi/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/O/out.traj',
    traj_ch4g='/scratch/users/alatimer/gases/methane/beef-vdw/476-arv/qn.traj',
    traj_ch3ohg='/scratch/users/alatimer/gases/methanol/arvin-beef-476/qn.traj',
    vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/methane/vib/' ,
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Rh-GN/meoh-hi/vib/',

    )

Au_BN = dftclass('Au',
    'BN',
    traj_ch4='/home/alatimer/work_dir/meoh-vs-methane/Au-BN/methane/out.traj',
    traj_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Au-BN/meoh/out.traj',
    traj_slab='/home/alatimer/work_dir/meoh-vs-methane/Au-BN/O/out.traj',
    traj_ch4g='/scratch/users/alatimer/gases/methane/beef-vdw/476-arv/qn.traj',
    traj_ch3ohg='/scratch/users/alatimer/gases/methanol/arvin-beef-476/qn.traj',
    vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Au-BN/methane-lo/vib/' ,
    vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Au-BN/meoh/vib/',
    )

Mn_GN  = dftclass('Mn','GN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Mn-GN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Mn-GN/meoh/',
                    tag='no-beef'   )

Tc_GN  = dftclass('Tc','GN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Tc-GN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Tc-GN/meoh/',
                    tag='no-beef'   )

Fe_GN  = dftclass('Fe','GN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Fe-GN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Fe-GN/meoh/',
                    tag='no-beef'   )


Ru_GN  = dftclass('Ru','GN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Ru-GN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Ru-GN/meoh/',
                    tag='no-beef'   )

Ni_BN  = dftclass('Ni','BN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Ni-BN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Ni-BN/meoh/',
                    tag='no-beef'   )

Cr_BN  = dftclass('Cr','BN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Cr-BN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Cr-BN/meoh/',
                    tag='no-beef'   )

Pd_BN  = dftclass('Pd','BN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Pd-BN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Pd-BN/meoh/',
                    tag='no-beef'   )

Pt_BN  = dftclass('Pt','BN',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/Pt-BN/methane/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/Pt-BN/meoh/',
                    tag='no-beef'   )

Co_CHA_MO  = dftclass('Co','CHA-MO',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/01_CHA_MO/methane/Co/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/01_CHA_MO/meoh/Co/',
                    tag='ambar' )

Ni_CHA_MO  = dftclass('Ni','CHA-MO',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/01_CHA_MO/methane/Ni/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/01_CHA_MO/meoh/Ni/',
                    tag='ambar' )


Cu_CHA_MO  = dftclass('Cu','CHA-MO',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/01_CHA_MO/methane/Cu/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/01_CHA_MO/meoh/Cu/',
                    tag='ambar' )

Cu_CHA_MOH  = dftclass('Cu','CHA-MOH',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/02_CHA_MOH/methane/Cu/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/02_CHA_MOH/meoh/Cu/',
                    tag='ambar' )

Cu_MOR_MOM  = dftclass('Cu','MOR-MOM',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/03_MOR_MOM/methane/Cu/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/03_MOR_MOM/meoh/Cu/',
                    tag='ambar' )


Co_MOR_MOM  = dftclass('CO','MOR-MOM',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/03_MOR_MOM/methane/Co/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/03_MOR_MOM/meoh/Co/',
                    tag='ambar' )

Ni_MOR_MOM  = dftclass('Ni','MOR-MOM',
        vibloc_ch4 ='/home/alatimer/work_dir/meoh-vs-methane/03_MOR_MOM/methane/Ni/' ,
        vibloc_ch3oh='/home/alatimer/work_dir/meoh-vs-methane/03_MOR_MOM/meoh/Ni/',
        tag='ambar' )


dftclasses_obj = dftclasses([
    RuO2,
    IrO2,
    RhO2,
    PtO2,
    Ag,
    Cu,
    Pd,
    Pt,
    Rh,

    #Rh_GN_lo,
    Tc_GN,
    Rh_GN,
    Ru_GN,
    Mn_GN,
    Fe_GN,
    Au_BN,
    Pt_BN,
    Cr_BN,
    Pd_BN,
    Ni_BN,

    Co_CHA_MO,
    Ni_CHA_MO,
    Cu_CHA_MO,
    Cu_CHA_MOH,
    Cu_MOR_MOM,
    Co_MOR_MOM,
    Ni_MOR_MOM,
        ])

reader('from-others.dat', dftclasses_obj)

### make pickle file
pickle.dump( dftclasses_obj, open( "dftobj.pkl", "wb" ) )
dco = pickle.load(open('dftobj.pkl','rb'))

for cat in dco.data:
    print cat.cat,cat.cattype,cat.vibs_ch4,cat.ets_ch4,cat.beef_ets_ch4
    if cat.vibs_ch4!=None:
        dGcorr = cat.get_dGcorr(423,101325)
        print dGcorr
