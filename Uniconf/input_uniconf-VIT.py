#!/usr/bin/python
import sys, string, os, glob
from math import *

# a few special functions
def IsFloat(s):
        try: 
                float(s)
                return True
        except ValueError:
                return False

def IsInt(s):
        try: 
                int(s)
                return True
        except ValueError:
                return False

# script to prepare the input file for the uniconf conformer generator

# reading the file with the charges

mol=[]
try:
	f = open(sys.argv[1], "r")
except Exception as e:
	print ("The error occured is: ", e)
	sys.exit(0)

for line in f:
	d = str.split(line)
	if len(d) == 5 and IsFloat(d[1]) == True and IsFloat(d[2]) == True and IsFloat(d[3]) == True and IsFloat(d[4]) == True:
		mol.append((d[0], d[1], d[2], d[3], d[4]))
f.close()

# parameters 
bonds = []

if os.path.isfile(sys.argv[1][0:-4]+'.ROT') == True:
	print ('bonds are here')
	f = open(sys.argv[1][0:-4]+'.ROT', 'r')
	for line in f:
		d = str.split(line)
		if len(d) == 5 and IsInt(d[0]) == True and IsInt(d[1]) == True and IsInt(d[2]) == True and IsInt(d[3]) == True and IsInt(d[4]) == True:
			for i in range(len(d)):
				d[i] = int(d[i])
			bonds.append(d)	
	f.close()	

# writing the uniconf input

f = open(sys.argv[1][0:-4]+'-uni.inp', 'w')
f.write('$BOND\n')
for i in range(len(bonds)):
	f.write('%5i %5i %5i %5i %5i\n' % (bonds[i][0], bonds[i][1], bonds[i][2], bonds[i][3], bonds[i][4]) )
f.write('$END\n')
f.write('$ALGO\n')
f.write('''ALGO=CONF CONNECT=WRITE library=nlopt optloc=nlopt_ln_sbplx 
MAXDISTDIff=0.1 EDIFF=0.1 DIST=1.4 NONHD=FALSE RMSD=0.05 MAXCLUST=300000 population=0
HCHRG=0.25 OCHRG=-0.5 KEL=1.0 KVW=1.0 KGD=0 TESTSIZE=1e-3
STRATEGY=1 CLUSTERPROPERTY=IXX SORT=e
MK=0 ITER1=33000 KMEANS=-1  MAXCONF=150000000 COM=0
ITER2=300000 KMEANS1=-1 MAXCONFPRINT=55000000
''')
f.write('$END\n')
f.write('$MOLECULE\n')
for i in range(len(mol)):
	f.write('%3s %12s %12s %12s\n' % (mol[i][0], mol[i][1], mol[i][2], mol[i][3]))
f.write('$END\n')
f.write('$CHARGE\n')
for i in range(len(mol)):
	f.write('%12s \n' % mol[i][4])
f.write('$END\n')
f.close()
