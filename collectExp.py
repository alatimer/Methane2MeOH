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
            print line
            vals = line.split()
            DOI = vals[labels.index("DOI")]
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
                    oxidant=oxidant,catalysis=catalysis,single_site=single_site,tag=tag,DOI=DOI)
            print cat_object.single_site
            cat_list.append(cat_object)
    return cat_list

cat_list = []
expclasses_obj = expclasses(reader('exp.dat',cat_list))

for obj in expclasses_obj.data:
    if obj.cat == '-':
       # print obj.cat
        obj.cat = 'Gas-Phase(Radical)'

### make pickle file
pickle.dump( expclasses_obj, open( "expobj.pkl", "wb" ) )
eco = pickle.load(open('expobj.pkl','rb'))

for cat in eco.data:
    print cat.cat,cat.cattype
