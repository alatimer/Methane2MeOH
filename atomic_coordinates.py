import pickle
from ase import io

catlistobj = pickle.load(open('dftobj.pkl','rb'))
catlistobj = catlistobj.filter(lambda x: x.atoms_ch4!=None)


for cat in catlistobj.data:
    print cat.cattype,cat.cat
    for surf,atoms in zip(['slab','CH4-TS','CH3OH-TS'],[cat.atoms_slab,cat.atoms_ch4,cat.atoms_ch3oh]):
        print surf
        io.write('traj-files/%s-%s-%s.cif'%(cat.cat,cat.cattype,surf),atoms)
        for atom in atoms:
            print atom.symbol,round(atom.position[0],4),round(atom.position[1],4),round(atom.position[2],4)

