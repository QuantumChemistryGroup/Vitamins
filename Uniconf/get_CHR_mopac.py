#!/usr/bin/python

import sys, string
from math import *

def IsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def IsFloat(s):
	try: 
		float(s)
		return True
	except ValueError:
		return False

# Main program starts here

GEOM=False

try:
	f = open(sys.argv[1], 'r')
	a = 0
	for line in f:
		if 'Empirical Formula' in line:
			a=a+1           
	if a == 2:
		GEOM = True
	f.close()
except:
	GEOM = False
	print ('There is no such file', sys.argv[1])            

coord_calc = []
charges = []

if GEOM == True:
	f = open(sys.argv[1], 'r')
	s = f.readline()
	while str.find(s, "FINAL HEAT OF FORMATION") == -1 : s = f.readline()
	while str.find(s, "CARTESIAN COORDINATES") == -1 : s = f.readline()                  
	while str.find(s, "Empirical Formula") == -1:
		s = f.readline()
		d = str.split(s)
		if len(d) == 5:
			atom = [d[1], d[2], d[3], d[4]]
			coord_calc.append(atom)
	while str.find(s, "NET ATOMIC CHARGES AND DIPOLE CONTRIBUTIONS") == -1 : s = f.readline()
	s = f.readline()
	while str.find(s, "DIPOLE") == -1:
		s = f.readline()
		d = str.split(s)
		if len(d) > 4 and IsInt(d[0]) == True and IsFloat(d[2]) and IsFloat(d[3]) and IsFloat(d[4]):
			charges.append(d[2])
	f.close()
	f = open (sys.argv[1][0:-4]+'.PM7', 'w')
	if len(coord_calc) == len(charges):
		for i in range(len(coord_calc)):
			a = coord_calc[i]		
			f.write('%2s %16s %16s %16s %16s\n' % (a[0], a[1], a[2], a[3], charges[i]))
		f.close()
	else:
		print ('something is wrong with your MOPAC job', sys.argv[1])
