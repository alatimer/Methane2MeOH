from ase.io import read, write
import glob

xsfs = glob.glob('*.xsf')

for xsf in xsfs:
    base = xsf.strip('.xsf')
    f = open(xsf,'r').readlines()
    w = open(base+'-new.xsf','w')
    print >>w, "CRYSTAL"
    for i in range(len(f)):
        if i<8:
            continue
        print >>w,  f[i],
    w.close()

for xsf in glob.glob('*-new.xsf'):
    print xsf
    atoms = read(xsf)
    #atoms = read(base+'-new.xsf')
    atoms.write(xsf.strip('-new.xsf')+'.cif')
