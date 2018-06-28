#!/usr/bin/env python

from expclass import expclass,expclasses
import pickle

# Takes experimental data in exp.dat and returns expobj.pkl, which has experimental data stored in class structure 
# specified in expclass.py

def reader(file_name,cat_list):
    for i,line in enumerate(open(file_name,'r').readlines()):
        if i == 0:
            labels = line.split()
        else:
            if line.startswith('#'):
                continue
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
            category = vals[labels.index("category")]
            tag = vals[labels.index("tag")]
            print category
            if tag == None:
                tag = ''
            cat_object=expclass(cat,cattype,T=T,log_conv=log_conv,sel=sel,author=author,rxntype=rxntype,
                    oxidant=oxidant,catalysis=catalysis,single_site=single_site,tag=tag,DOI=DOI,category=category)
            cat_list.append(cat_object)
    return cat_list

cat_list = []
expclasses_obj = expclasses(reader('exp.dat',cat_list))

for obj in expclasses_obj.data:
    if '/zeolite' in obj.category:
        obj.category = obj.category.split('/')[0]
    if obj.cat == '-':
        obj.cat = 'Gas-Phase(Radical)'
    if obj.category in ['Zeolite','ZSM-5','MOR','SSZ-13']:
        obj.category = 'Zeolite'


### make pickle file
pickle.dump( expclasses_obj, open( "expobj.pkl", "wb" ) )
eco = pickle.load(open('expobj.pkl','rb'))

for cat in eco.data:
    print cat.cat,cat.cattype,cat.category
