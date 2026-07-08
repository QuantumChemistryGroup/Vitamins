#!/usr/bin/python
import sys, string
from math import *

f = open(sys.argv[1])

s = f.readline()
i = 0
CHR = ''

# Try CHELPG
for line in f:  # for each line in a file
	if 'CHELPG Charges' in line: i = i + 1   
print ('CHELPG', i)
f.seek(0)
s = f.readline()

if i > 0:
	CHR = 'CHELPG'
else:
	# Try Hirshfeld
	for line in f:  # for each line in a file
		if 'HIRSHFELD ANALYSIS' in line: i = i + 1   
	print ('HIRSHFELD', i)
	if i > 0:
		CHR = 'HIRSHFELD'
	else:
		# Try Mulliken
		f.seek(0)
		for line in f:  # for each line in a file
			if 'MULLIKEN ATOMIC CHARGES' in line: i = i + 1   
		print ('MULLIKEN', i)
		if i > 0:
			CHR = 'MULLIKEN'
		else:
			print ('No CHELPG/HIRSHFELD/MULLIKEN in your ORCA output: ', sys.argv[1], '. Stop.\n')
			sys.exit(0)

Z = []
f.seek(0)

if CHR == 'CHELPG':
	for j in range(i):
		while str.find(s, 'CHELPG Charges') == -1 and s != "": s = f.readline()
		s = f.readline()
	s = f.readline()
	while str.find(s, "--------") == -1:
		d = str.split(s);
		if len(d) == 4:
			z = float(d[3])
			Z.append(z)
			s = f.readline()
		else: print ("All the charges read"); s = f.readline()
elif CHR == 'HIRSHFELD':
	for j in range(i):
		while str.find(s, 'HIRSHFELD ANALYSIS') == -1 and s != "": s = f.readline()
		s = f.readline()
	while str.find(s, 'ATOM     CHARGE      SPIN') == -1 and s != "": s = f.readline()
	for line in f:
	        d = str.split(line)
	        if len(d) > 2:
	                Z.append(float(d[2]))
	        else:
	                break
elif CHR == 'MULLIKEN':
	for j in range(i):
		while str.find(s, 'MULLIKEN ATOMIC CHARGES') == -1 and s != "": s = f.readline()
		s = f.readline()
	for line in f:
	        d = str.split(line)
	        if len(d) > 2 and len(d) < 5:
	                Z.append(float(d[-1]))
	        else:
	                break
else:
	print ('something is wrong.')
# get last coordinates
f.seek(0)
s = f.readline()
i = 0
for line in f:  # for each line in a file
        if 'CARTESIAN COORDINATES (ANGSTROEM)' in line: i = i + 1   
print (i)

f.seek(0)
s = f.readline()

for j in range(i):
        while str.find(s, 'CARTESIAN COORDINATES (ANGSTROEM)') == -1 and s != "": s = f.readline()
        s = f.readline()

s = f.readline()
#s = f.readline()
#print s
coord = []
while str.find(s, "--------") == -1:
        d = str.split(s); 
        if len(d) == 4:
                g = [d[0], d[1], d[2], d[3]]
                coord.append(g); s = f.readline()
        else: 
                print ("All the coordinates read")
                s = f.readline()

if len(Z) != len(coord):
	print ("Lengths of coord and charges are not equal.", len(Z), len(coord))
	sys.exit(0)
else:
	for i in range(len(coord)):
		coord[i].append(Z[i])

f = open(sys.argv[1][0:-4]+'.CHR', 'w')
for i in range(len(coord)):
	f.write("%3s %15s %15s %15s %15s \n" % (coord[i][0], coord[i][1], coord[i][2], coord[i][3], coord[i][4]))
f.close()
