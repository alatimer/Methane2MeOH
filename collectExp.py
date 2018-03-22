#!/usr/bin/env python

from expclass import expclass,expclasses
import pickle

def reader(file_name,cat_list):
    for i,line in enumerate(open(file_name,'r').readlines()):
        if i == 0:
            labels = line.split()
        else:
            if line.startswith('#'):
                continue
            vals = line.split()
            cat = vals[labels.index("cat")]
            cattype = vals[labels.index("cattype")]
            T = int(vals[labels.index("T")])
            log_conv = float(vals[labels.index("log_conv")])
            sel = float(vals[labels.index("sel")])
            author = vals[labels.index("author")]
            rxntype = vals[labels.index("rxntype")]
            oxidant = vals[labels.index("oxidant")]
            catalysis = vals[labels.index("catalysis")]
            single_site = vals[labels.index("single-site")]
            tag = vals[labels.index("tag")]
            if tag == None:
                tag = ''
            cat_object=expclass(cat,cattype,T=T,log_conv=log_conv,sel=sel,author=author,rxntype=rxntype,
                    oxidant=oxidant,catalysis=catalysis,single_site=single_site,tag=tag)
            cat_list.append(cat_object)
    return cat_list

cat_list = []
expclasses_obj = expclasses(reader('exp.dat',cat_list))

### make pickle file
pickle.dump( expclasses_obj, open( "expobj.pkl", "wb" ) )
eco = pickle.load(open('expobj.pkl','rb'))

for cat in eco.data:
    print cat.cat,cat.cattype
