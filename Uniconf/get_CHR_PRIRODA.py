#!/usr/bin/python
import sys, string
from math import *


elements = {
       'H':'1',
       'He':'2',
       'Li':'3',
       'Be':'4',
       'B':'5',
       'C':'6',
       'N':'7',
       'O':'8',
       'F':'9',
       'Ne':'10',
       'Na':'11',
       'Mg':'12',
       'Al':'13',
       'Si':'14',
       'P':'15',
       'S':'16',
       'Cl':'17',
       'Ar':'18',
       'K':'19',
       'Ca':'20',
       'Sc':'21',
       'Ti':'22',
       'V':'23',
       'Cr':'24',
       'Mn':'25',
       'Fe':'26',
       'Co':'27',
       'Ni':'28',
       'Cu':'29',
       'Zn':'30',
       'Ga':'31',
       'Ge':'32',
       'As':'33',
       'Se':'34',
       'Br':'35',
       'Kr':'36',
       'Rb':'37',
       'Sr':'38',
       'Y':'39',
       'Zr':'40',
       'Nb':'41',
       'Mo':'42',
       'Tc':'43',
       'Ru':'44',
       'Rh':'45',
       'Pd':'46',
       'Ag':'47',
       'Cd':'48',
       'In':'49',
       'Sn':'50',
       'Sb':'51',
       'Te':'52',
       'I':'53',
       'Xe':'54',
       'Cs':'55',
       'Ba':'56',
       'La':'57',
       'Ce':'58',
       'Pr':'59',
       'Nd':'60',
       'Pm':'61',
       'Sm':'62',
       'Eu':'63',
       'Gd':'64',
       'Tb':'65',
       'Dy':'66',
       'Ho':'67',
       'Er':'68',
       'Tm':'69',
       'Yb':'70',
       'Lu':'71',
       'Hf':'72',
       'Ta':'73',
       'W':'74',
       'Re':'75',
       'Os':'76',
       'Ir':'77',
       'Pt':'78',
       'Au':'79',
       'Hg':'80',
       'Tl':'81',
       'Pb':'82',
       'Bi':'83',
       'Po':'84',
       'At':'85',
       'Rn':'86',
       'Fr':'87',
       'Ra':'88',
       'Ac':'89',
       'Th':'90',
       'Pa':'91',
       'U':'92',
       'Np':'93',
       'Pu':'94',
       'Am':'95',
       'Cm':'96',
       'Bk':'97',
       'Cf':'98',
       'Es':'99',
       'Fm':'100',
       'Md':'101',
       'No':'102',
       'Lr':'103',
       'Rf':'104',
       'Db':'105',
       'Sg':'106',
       'Bh':'107',
       'Hs':'108',
       'Mt':'109',
       'Ds':'110',
       'Rg':'111',
       'Cn':'112',
       'Uut':'113',
       'Fl':'114',
       'Uup':'115',
       'Lv':'116',
       'Uuh':'117',
       'Uuh':'118',
}


# Main program starts here

atoms = []
coord = []

f = open(sys.argv[1])

s = f.readline()
i = 0
for line in f:  # for each line in a file
	if 'Atomic Coordinates' in line: i = i + 1   
print (i)

f.seek(0)
s = f.readline()



for j in range(i):
	while str.find(s, 'Atomic Coordinates') == -1 and s != "": s = f.readline()
	s = f.readline()


while str.find(s, "#") == -1:
	d = str.split(s); 
	if len(d) == 4:
		g = (d[0], d[1], d[2], d[3])
		coord.append(g); s = f.readline()
	else: print ("All the coordinates read"); s = f.readline()

#print coord

# get Hirshfeld charges

f.seek(0)
i=0
for line in f:  # for each line in a file
	if 'Atomic partitions of the density' in line: i = i + 1   
print (i)

f.seek(0)
s = f.readline()



for j in range(i):
	while str.find(s, 'Atomic partitions of the density') == -1 and s != "": s = f.readline()
	s = f.readline()

s = f.readline()

ch_hirsh = []
while str.find(s, "total") == -1:
	d = str.split(s); 
	if len(d) == 4:
		ch_hirsh.append(d)
	else: print ("All the coordinates read")
	s = f.readline()


f1 = open(sys.argv[1][0:-4]+'.CHR', 'w')
if len(coord) == len(ch_hirsh):
	for i in range(len(coord)):
		f1.write('%2s %15s %15s %15s %10s\n' % (ch_hirsh[i][1], coord[i][1], coord[i][2], coord[i][3], ch_hirsh[i][2]))
else:
	print ('Dimesnisions of chrg and coord are not equal. exit', len(coord), len(ch_hirsh), 2)
	sys.exit(0)
f1.close()

