#Embedded file name: /scratch/users/alatimer/meoh-vs-methane/analysis/catclass.py
from ase import Atoms
from ase.io import read, write
import pickle
import numpy as np
from ase.vibrations import Vibrations
from ase.thermochemistry import HarmonicThermo, IdealGasThermo

class dftclass:
    """
    """
    def __init__(self, 
            cat, 
            cattype, 
		    ets_ch4 = None, 
		    ets_ch3oh = None, 
		    traj_ch4 = None, 
		    traj_ch3oh = None, 
		    traj_slab = None,
		    traj_ch4g = '/home/alatimer/work_dir/gases/methane/beef-vdw/550/qn.traj', 
		    traj_ch3ohg = '/home/alatimer/work_dir/gases/methanol/beef-vdw/550/qn.traj', 
		    vibloc_ch4g = '/home/alatimer/work_dir/gases/methane/beef-vdw/550/', 
		    vibloc_ch3ohg = '/home/alatimer/work_dir/gases/methanol/beef-vdw/550/', 
            vibloc_ch4 = None,
            vibloc_ch3oh = None,
		    tag = '',
            ):

        self.cat = cat
        self.cattype = cattype
        self.ets_ch4 = ets_ch4
        self.ets_ch3oh = ets_ch3oh
        self.traj_ch4 = traj_ch4
        self.traj_ch3oh = traj_ch3oh
        self.traj_slab = traj_slab
        self.traj_ch4g = traj_ch4g
        self.traj_ch3ohg = traj_ch3ohg
        self.vibloc_ch4g = vibloc_ch4g
        self.vibloc_ch3ohg = vibloc_ch3ohg
        self.vibloc_ch4 = vibloc_ch4
        self.vibloc_ch3oh = vibloc_ch3oh
        self.tag = tag

        self.atoms_ch4g = read(traj_ch4g)
        self.atoms_ch3ohg = read(traj_ch3ohg)
        self.atoms_slab = None
        self.atoms_ch4 = None
        self.atoms_ch3oh = None

        self.beef_ch4 = None
        self.beef_ch3oh = None
        self.beef_slab = None
        self.beef_ch4g = None
        self.beef_ch3ohg = None
        self.beef_ets_ch4 = None
        self.beef_ets_ch3oh = None

        self.vibs_ch4 = None
        self.vibs_ch4g = None
        self.vibs_ch3oh = None
        self.vibs_ch3ohg = None

        self.ch_ch4 = None
        self.ch_ch3oh = None
        

        clrs_dict = {
            #'Fe':'firebrick',
            #'Cu':'goldenrod',
            #'Cu-Fe':'firebrick',
            #'Fe-MMO':'forestgreen',
            #'V':'blue',
            #'Mo':'m',
            #'Ga':'green',
            #'W':'orange',
            #'Co':'cyan',
            #'Ni':'pink',
            #'Rh':'lightskyblue',
            'rutile-110':'firebrick',
            'metal-111':'goldenrod',
            'GN':'pink',
            'BN':'forestgreen',
            'CHA-MO':'lightgreen',
            'CHA-MOH':'m',
            'SAPO-34-MO':'lightskyblue',
            'CHA-MOM':'indianred',
            'MOR-MOM':'grey',
            'porphyrin':'cyan',
            }

        shape_dict = {
                'rutile-110':'o',
                'metal-111':'s',
                'GN':'8',
                'BN':'p',
                'CHA-MO':'<',
                'CHA-MOH':'>',
                'MOR-MOM':'^',
                }

        if 'HSE' in self.tag:
            self.shape = 's'
         #   self.shape = shape_dict[self.cattype]
        else:
            self.shape = 'o'

        if self.cattype in clrs_dict.keys():
            self.color = clrs_dict[self.cattype]
        else:
            self.color = 'grey'

        #def populate_atoms(self):
        if self.traj_ch4 !=None:
            self.atoms_ch4 = read(self.traj_ch4)
            self.atoms_ch3oh = read(self.traj_ch3oh)
            self.atoms_slab = read(self.traj_slab)
            self.atoms_ch4g = read(self.traj_ch4g)
            self.atoms_ch3ohg = read(self.traj_ch3ohg)
            self.ets_ch4 = self.atoms_ch4.get_potential_energy() - self.atoms_slab.get_potential_energy() \
            - self.atoms_ch4g.get_potential_energy()
            self.ets_ch3oh = self.atoms_ch3oh.get_potential_energy() - self.atoms_slab.get_potential_energy() \
            - self.atoms_ch3ohg.get_potential_energy()
            #for i,atoms in enumerate([self.atoms_ch4,self.atoms_ch3oh]):
            H_list = []
            dist_list = []
            for atom in self.atoms_ch4:
                if atom.symbol == 'C':
                    C_loc = atom.index
                elif atom.symbol == 'H':
                    H_list.append(atom.index)
            for H in H_list:
                dist = ((self.atoms_ch4[H].x-self.atoms_ch4[C_loc].x )**2 +(self.atoms_ch4[H].y-self.atoms_ch4[C_loc].y )**2+(self.atoms_ch4[H].z-self.atoms_ch4[C_loc].z )**2)**0.5
                
                dist_list.append(dist)
            max_dist = max(dist_list)
            print dist_list,max_dist
            self.ch_ch4 = max_dist

            #return

        #def populate_beef(self):

            def beef_reader(traj):
                directory = '/'.join(traj.split('/')[0:-1])
                beef_array = pickle.load(open(directory + '/ensemble.pkl', 'r'))
                if abs(np.mean(beef_array)) < 100:
                    beef_array += read(traj).get_potential_energy()
                return beef_array
            self.beef_ch4 = beef_reader(self.traj_ch4)
            self.beef_ch3oh = beef_reader(self.traj_ch3oh)
            self.beef_slab = beef_reader(self.traj_slab)
            self.beef_ch4g = beef_reader(self.traj_ch4g)
            self.beef_ch3ohg = beef_reader(self.traj_ch3ohg)
            self.beef_ets_ch4 = self.beef_ch4 - self.beef_slab - self.beef_ch4g
            self.beef_ets_ch4 = self.beef_ets_ch4 * 0.684 + np.mean(self.beef_ets_ch4 * (1-0.684))
            self.beef_ets_ch3oh = self.beef_ch3oh - self.beef_slab - self.beef_ch3ohg
            self.beef_ets_ch3oh = self.beef_ets_ch3oh * 0.684 + np.mean(self.beef_ets_ch3oh * (1-0.684))
            #return
        
        if self.vibloc_ch4 != None:
            def vibs_reader(vibloc):
                f = open(vibloc+'/myjob.out','r')
                vibenergies = []
                for line in f:
                    if 'ambar' in self.tag and 'gases' not in vibloc:
                        undes_strings = ('mode','f')
                        for undes_string in undes_strings:
                            if undes_string in undes_strings :
                                line = line.replace(undes_string,'')
                        try:
                            temp = line.replace('.','')
                            temp = temp.replace(' ','')
                            float(temp)
                        except ValueError:
                            continue
                        num, inv_cm = line.split()
                        meV = float(inv_cm)/8.06
                    else:
                        try:
                            temp = line.replace('.','')
                            temp = temp.replace(' ','')
                            temp = temp.replace('i','')
                            float(temp)
                        except ValueError:
                            continue
                        num, meV, inv_cm, = line.split()
                        if 'i' in meV:
                            meV = 7
                    vibenergies.append(float(meV))
                #convert from meV to eV for each mode
                vibenergies[:] = [round(ve/1000.,4) for ve in vibenergies]    
                return vibenergies
            self.vibs_ch4 = vibs_reader(self.vibloc_ch4)
            self.vibs_ch3oh = vibs_reader(self.vibloc_ch3oh)
            self.vibs_ch4g = vibs_reader(self.vibloc_ch4g)
            self.vibs_ch3ohg = vibs_reader(self.vibloc_ch3ohg)

    def get_dGcorr(self,T,P,verbose=False):
        def get_ads_Gcorr(vibs,T,verbose=False):
            gibbs = HarmonicThermo(vib_energies = vibs, potentialenergy = 0)
            adsGcorr = gibbs.get_helmholtz_energy(T,verbose=False)
            return adsGcorr
        def get_gas_Gcorr(atoms,vibs,T,P,symmetrynumber,spin,geometry,verbose=False):
            gibbs = IdealGasThermo(vib_energies=vibs,
                                potentialenergy=0,
                                atoms=atoms,
                                geometry=geometry,
                                symmetrynumber=symmetrynumber,
                                spin=spin,
                                )
            gasGcorr = gibbs.get_gibbs_energy(T,P,verbose=False)
            return gasGcorr
        Gcorr_ch4 = get_ads_Gcorr(self.vibs_ch4,T)                
        Gcorr_ch3oh = get_ads_Gcorr(self.vibs_ch3oh,T)                
        Gcorr_ch4g = get_gas_Gcorr(self.atoms_ch4g,self.vibs_ch4g,T,P,12,0,'nonlinear')                
        Gcorr_ch3ohg = get_gas_Gcorr(self.atoms_ch3ohg,self.vibs_ch3ohg,T,P,1,0,'nonlinear')
       # print Gcorr_ch4, Gcorr_ch3oh,Gcorr_ch4g,Gcorr_ch3ohg
       # print 'ch4',(Gcorr_ch4 - Gcorr_ch4g),'ch3oh',(Gcorr_ch3oh - Gcorr_ch3ohg)
        Gcorr =  (Gcorr_ch4 - Gcorr_ch4g) - (Gcorr_ch3oh - Gcorr_ch3ohg)         
        return Gcorr

class dftclasses:
    """
    """

    def __init__(self, dftclasses):
        self.data = dftclasses

    def filter(self, fun, *args, **kwargs):
        """
        Takes list of chargexfer objects and filters out those that do not give fun(chargexfer) == True.
        Returns new ChargeXfers object
        """
        out = []
        for c in self.data:
            if fun.__name__ == '<lambda>':
                bool = fun(c)
            else:
                bool = fun(c, *args, **kwargs)
            if bool:
                out.append(c)

        return dftclasses(out)

    def get_property(self, ppt):
        """
        Return list of property for each chargexfer
        """
        out = []
        for c in self.data:
            eval('out.append(c.%s)' % ppt)

    def fun_dGcorr(self,T,P):
        dGcorrs = np.zeros(len(self.data))
        for i,cat in enumerate(self.data):
            if cat.vibs_ch4 == None:
                print "Error: passed catalyst with no attached vibrations"
                exit()
            dGcorr = cat.get_dGcorr(T,P)
            dGcorrs[i] = dGcorr
        dGcorr = np.mean(dGcorrs)
        return dGcorr

        return np.array(out)