#!/usr/bin/python
from __future__ import division
import sys, string
import os
import re
import numpy
from math import *
from numpy import matrix
from numpy import array
from numpy import *
from numpy import linalg as LA


# constants

h = 6.62606896e-34 # J*s
h_2pi = h/(2*pi) # J*s
k_b = 1.3806504e-23 # J/K
Na = 6.02214179e+23 # Avogadro's number
Rg = k_b * Na
I_amu_A2_to_kg_m2 = 1.660538782e-27*1e-20
kcal_to_j = 4.184*1000/Na
c= 2.99792458e+10  # cm-sec-1
amu_to_kg = 1.66053886e-27
cm_to_hertz = 2.997e+10

# the list of the elements

elements = {
        'H ': ' 1 ',
        'He ': ' 2 ',
        'Li ': ' 3 ',
        'Be ': ' 4 ',
        'B ': ' 5 ',
        'C ': ' 6 ',
        'N ': ' 7 ',
        'O ': ' 8 ',
        'F ': ' 9 ',
        'Ne ': ' 10 ',
        'Na ': ' 11 ',
        'Mg ': ' 12 ',
        'Al ': ' 13 ',
        'Si ': ' 14 ',
        'P ': ' 15 ',
        'S ': ' 16 ',
        'Cl ': ' 17 ',
        'Ar ': ' 18 ',
        'K ': ' 19 ',
        'Ca ': ' 20 ',
        'Sc ': ' 21 ',
        'Ti ': ' 22 ',
        'V ': ' 23 ',
        'Cr ': ' 24 ',
        'Mn ': ' 25 ',
        'Fe ': ' 26 ',
        'Co ': ' 27 ',
        'Ni ': ' 28 ',
        'Cu ': ' 29 ',
        'Zn ': ' 30 ',
        'Ga ': ' 31 ',
        'Ge ': ' 32 ',
        'As ': ' 33 ',
        'Se ': ' 34 ',
        'Br ': ' 35 ',
        'Kr ': ' 36 ',
        'Rb ': ' 37 ',
        'Sr ': ' 38 ',
        'Y ': ' 39 ',
        'Zr ': ' 40 ',
        'Nb ': ' 41 ',
        'Mo ': ' 42 ',
        'Tc ': ' 43 ',
        'Ru ': ' 44 ',
        'Rh ': ' 45 ',
        'Pd ': ' 46 ',
        'Ag ': ' 47 ',
        'Cd ': ' 48 ',
        'In ': ' 49 ',
        'Sn ': ' 50 ',
        'Sb ': ' 51 ',
        'Te ': ' 52 ',
        'I ': ' 53 ',
        'Xe ': ' 54 ',
        'Cs ': ' 55 ',
        'Ba ': ' 56 ',
        'La ': ' 57 ',
        'Ce ': ' 58 ',
        'Pr ': ' 59 ',
        'Nd ': ' 60 ',
        'Pm ': ' 61 ',
        'Sm ': ' 62 ',
        'Eu ': ' 63 ',
        'Gd ': ' 64 ',
        'Tb ': ' 65 ',
        'Dy ': ' 66 ',
        'Ho ': ' 67 ',
        'Er ': ' 68 ',
        'Tm ': ' 69 ',
        'Yb ': ' 70 ',
        'Lu ': ' 71 ',
        'Hf ': ' 72 ',
        'Ta ': ' 73 ',
        'W ': ' 74 ',
        'Re ': ' 75 ',
        'Os ': ' 76 ',
        'Ir ': ' 77 ',
        'Pt ': ' 78 ',
        'Au ': ' 79 ',
        'Hg ': ' 80 ',
        'Tl ': ' 81 ',
        'Pb ': ' 82 ',
        'Bi ': ' 83 ',
        'Po ': ' 84 ',
        'At ': ' 85 ',
        'Rn ': ' 86 ',
        'Fr ': ' 87 ',
        'Ra ': ' 88 ',
        'Ac ': ' 89 ',
        'Th ': ' 90 ',
        'Pa ': ' 91 ',
        'U ': ' 92 ',
        'Np ': ' 93 ',
        'Pu ': ' 94 ',
        'Am ': ' 95 ',
        'Cm ': ' 96 ',
        'Bk ': ' 97 ',
        'Cf ': ' 98 ',
        'Es ': ' 99 ',
        'Fm ': ' 100 ',
        'Md ': ' 101 ',
        'No ': ' 102 ',
        'Lr ': ' 103 ',
        'Rf ': ' 104 ',
        'Db ': ' 105 ',
        'Sg ': ' 106 ',
        'Bh ': ' 107 ',
        'Hs ': ' 108 ',
        'Mt ': ' 109 ',
        'Ds ': ' 110 ',
        'Rg ': ' 111 ',
        'Cn ': ' 112 ',
        'Uut ': ' 113 ',
        'Fl ': ' 114 ',
        'Uup ': ' 115 ',
        'Lv ': ' 116 ',
        'Uuh ': ' 117 ',
        'Uuh ': ' 118 ',
}

masses = {
        'H ': ' 1.0078250 ',
        'He ': ' 4.0026033 ',
        'Li ': ' 7.0160045 ',
        'Be ': ' 9.0121825 ',
        'B ': ' 11.0093053 ',
        'C ': ' 12.0000000 ',
        'N ': ' 14.0030740 ',
        'O ': ' 15.9949146 ',
        'F ': ' 18.9984033 ',
        'Ne ': ' 19.9924391 ',
        'Na ': ' 22.9897697 ',
        'Mg ': ' 23.9850450 ',
        'Al ': ' 26.9815413 ',
        'Si ': ' 27.9769284 ',
        'P ': ' 30.9737634 ',
        'S ': ' 31.9720718 ',
        'Cl ': ' 34.9688527 ',
        'Ar ': ' 39.9623831 ',
        'K ': ' 38.9637079 ',
        'Ca ': ' 39.9625907 ',
        'Sc ': ' 44.9559136 ',
        'Ti ': ' 47.9479467 ',
        'V ': ' 50.9439625 ',
        'Cr ': ' 51.9405097 ',
        'Mn ': ' 54.9380463 ',
        'Fe ': ' 55.9349393 ',
        'Co ': ' 58.9331978 ',
        'Ni ': ' 57.9353471 ',
        'Cu ': ' 57.9353471 ',
        'Zn ': ' 63.9291454 ',
        'Ga ': ' 68.9255809 ',
        'Ge ': ' 73.9211788 ',
        'As ': ' 74.9215955 ',
        'Se ': ' 79.9165205 ',
        'Br ': ' 78.9183361 ',
        'Kr ': ' 83.9115064 ',
        'Rb ': ' 84.9117000 ',
        'Sr ': ' 87.9056000 ',
        'Y ': ' 88.9054000 ',
        'Zr ': ' 89.9043000 ',
        'Nb ': ' 92.9060000 ',
        'Mo ': ' 97.9055000 ',
        'Tc ': ' 98.9063000 ',
        'Ru ': ' 101.9037000 ',
        'Rh ': ' 102.9048000 ',
        'Pd ': ' 105.9032000 ',
        'Ag ': ' 106.9050900 ',
        'Cd ': ' 113.9036000 ',
        'In ': ' 114.9041000 ',
        'Sn ': ' 117.9018000 ',
        'Sb ': ' 120.9038000 ',
        'Te ': ' 129.9067000 ',
        'I ': ' 126.9004000 ',
        'Xe ': ' 131.9042000 ',
        'Cs ': ' 132.9054290 ',
        'Ba ': ' 137.9050000 ',
        'La ': ' 138.9061000 ',
        'Hf ': ' 179.9468000 ',
        'Ta ': ' 180.9480000 ',
        'W ': ' 183.9510000 ',
        'Re ': ' 186.9560000 ',
        'Os ': ' 189.9586000 ',
        'Ir ': ' 192.9633000 ',
        'Pt ': ' 194.9648000 ',
        'Au ': ' 196.9666000 ',
        'Hg ': ' 201.9706000 ',
        'Tl ': ' 204.9745000 ',
        'Pb ': ' 207.9766000 ',
        'Bi ': ' 208.9804000 ',
        'Po ': ' 208.9825000 ',
        'At ': ' 210.9875000 ',
        'Rn ': ' 222.0175000 ',
        'Fr ': ' 223.0198000 ',
        'Ra ': ' 226.0254000 ',
        'Ac ': ' 227.0278000 ',
}

# function to calculate the moment of inertia along the particular bond
def mr2 (x1, x2, a):
	# the function to calculate the distance from the point a = (a[0], a[1], a[2]) to the line passing through two given points x1(x1[0], x1[1], x2[2])
	# 1st we need to write the equation of the line in 3d : (x-x1)/(x2-x1)=(y-y1)/(y2-y1)=(z-z1)/(z2-z1)
	# or we can write down the same thing x = t*(x2-x1)+ x1, y = t*(y2-y1)+ y1, z = t*(z2-z1)+ z1
	# then we can write the equation for the distance d = ((a-x1-t*(x2-x1))**2 + (b-y1-t*(y2-y1))**2 + (c-z1-t*(z2-z1))**2 )**1/2
	# then we claim the minimum of the above-mentioned function d is the same as for d**2. Then we take the first derivative of the function d**2
	# and set it to be 0. Then we derive t. Then we take t and put in the expression for d.
	# the second derivative for d**2 is always positive, meaning that extremum does correspond to minimum
	t = (     (a[3]-x1[3])*(x2[3]-x1[3]) + (a[4]-x1[4])*(x2[4]-x1[4]) + (a[5]-x1[5])*(x2[5]-x1[5])        )/( (x2[3]-x1[3])**2 + (x2[4]-x1[4])**2 + (x2[5]-x1[5])**2   )
	d = (   (a[3] - x1[3] -t*(x2[3] - x1[3] ))**2 + (a[4] - x1[4] -t*(x2[4] - x1[4] ))**2 + (a[5] - x1[5] -t*(x2[5] - x1[5] ))**2          )**0.5
	# to calculate the moment of inertia I = m*r**2, d = r, m = a[3]
	I = a[2]*d**2 
	return (I)


# function to calculate the moment of inertia along the bond

def MIB (molecule,frrotor):

	rotor_1 = []
	rotor_2 = []
	# frrotor[0] is the freq sequential number
	bond = [frrotor[1], frrotor[2]]
	rotor = frrotor[3:]
# to put atoms in the rotor1 and rotor2

	for i in range(len(molecule)):
		if (i+1) in rotor:
			rotor_2.append(molecule[i])
		else: rotor_1.append(molecule[i])

	rotor_1_inertia = []
	rotor_2_inertia = []

# to calculate the mr2 term for rotor1 and for rotor2

	for i in range(len(rotor_1)):
		t = mr2(molecule[int(bond[0])-1], molecule[int(bond[1])-1], rotor_1[i])
		rotor_1_inertia.append(t)


	for i in range(len(rotor_2)):
		t = mr2 (molecule[int(bond[0])-1], molecule[int(bond[1])-1], rotor_2[i])
		rotor_2_inertia.append(t)

# to calculate the reduced moment of inertia I = I1*I2/(I1 + I2)

	I = sum(rotor_1_inertia)*sum(rotor_2_inertia)/(sum(rotor_1_inertia) + sum(rotor_2_inertia))
	return I


# function to calculate the free rotation, do not apply it to enourmously large moment of inertia. Please, don't calculate this for very big moment of inertia
def free_rotor(I, points):
	array_q = []
	array_e = []
	for i in range (-int(points), +int(points), 1):
		e_i = (h_2pi**2*i**2)/(2*I*I_amu_A2_to_kg_m2) # energy levels in Joules
		q = e**(-e_i/(k_b*T))
		array_q.append(q)
		array_e.append(e_i)
	q = sum(array_q)
#	print ('rotation partition function ', q )
	return (q, array_e)


# formula to calculate the moments of inertia of a molecule as a whole around the mass center
def Iij (a, b, i, j):
	array = []
	if int(i) == int(j):
		d=1
	else: d = 0
	for z in range(len(a)):
		n = a[z][2]*  ( ( (a[z][3]-b[3])**2 + (a[z][4]-b[4])**2 + (a[z][5]-b[5])**2 )*d - ( a[z][i]-b[i]) * (a[z][j]-b[j])  )
		array.append(n)
	return sum(array)


# n - is the periodicity
# x - the value for the angle

def Function_cos(n, x):
	F = (cos(n*x*pi/(180)))
#	F = (1-cos(n*x*pi/180))
	return (F)

# to read the input file

def input_search_simple(a):
	f.seek(0)
	s = f.readline()
	f.seek(0)
	while str.find(s, a) == -1 and s != "":s = f.readline()
	s = f.read(1)
	position = f.tell()-1
	f.seek(position)
	array = []
	while str.find(s, '$end') == -1 and s != "":
		s = f.readline()
		d = str.split(s)
		for i in range(len(d)):
			array.append(d[i])
	del array[-1]
	return (array)

def input_search_list(a):
	f.seek(0)
	s = f.readline()
	f.seek(0)
	while str.find(s, a) == -1 and s != "":s = f.readline()
	s = f.read(1)
	position = f.tell()-1
	f.seek(position)
	array = []
	while str.find(s, '$end') == -1 and s != "":
		s = f.readline()
		d = str.split(s)
		array.append(d)
	del array[-1]
	return (array)


def Function_sin(n, x):
	F = (sin(n*x*pi/(180)))
#	F = (1-sin(n*x*pi/180))
	return (F)


def Difference(Y, Y1):
	tmp = []
	for i in range(len(Y)):
		sum1 = abs(Y[i]-Y1[i])
		tmp.append(sum1)
#	print (sum(tmp))
	M = sum(tmp)/len(Y)
	return(M)

def make_a_list_array (Y):
	tmp = []
	for i in Y:
		i = float(i)
		tmp.append(i)
	Y_new = tmp
	return(Y_new)

def write_line(f,m,i,n):
	for j in range(n):
		f.write(' ')
	for j in range(i):
		f.write(m)
	f.write('\n')

def write_symbol(f,m,i,n):
	for j in range(n):
		f.write(' ')
	for j in range(i):
		f.write(m)


f = open(sys.argv[1])

#########################################################################################################
# read the input file for the given molecule
#########################################################################################################

# find the molecule
molecule = input_search_list('$molecule')

# get the mmRRHO parameters, tau and alpha
thld=0
if (len(sys.argv)>2):
	GR = [['NaN'],['NaN'],['NaN']]
	if sys.argv[2].lower()[0:2] == 'ho':
		GR[0][0] = 0.00001
		GR[1][0] = 1000.0
		GR[2][0] = 0
		d = sys.argv[2].split('_')
		#print(d)
		if len(d)>1:
			try:
				thld=float(d[1])
			except:
				print ("Your HO (FREQ) parameters are not clear")
				print ("I am using the default: HO (100) ")
				thld=100.0
	elif sys.argv[2].lower()[0:2] == 'gr':
		try:
			d = sys.argv[2].split('_')
			GR[0][0] = float(d[1])
			GR[1][0] = float(d[2])
			GR[2][0] = int(d[3])
		except:
			print ("Your msRRHO parameters are not clear")
			print ("I am using the default: 100 4 1")
			GR[0][0] = 100
			GR[1][0] = 4
			GR[2][0] = 1
	else:
		print ("Specify:")
		print ("HO = harmonic oscillator")
		print ("HO_FREQ = harmonic oscillator (FREQ) - Thrular's approach")
		print ("GR_100_4_0 = msRRHO, tau = 100, alpha = 4, enthapy is from HO")
		print ("GR_100_4_1 = msRRHO, tau = 100, alpha = 4, enthapy is corrected")
		sys.exit(0)
else:
		print ("Specify:")
		print ("HO = harmonic oscillator")
		print ("GR_100_4_0 = msRRHO, tau = 100, alpha = 4, enthapy is from HO")
		print ("GR_100_4_1 = msRRHO, tau = 100, alpha = 4, enthapy is corrected")
		sys.exit(0)

# find the frequencies
freq_raw = input_search_list('$freq')

# get the frequencies for HO
# I suggest that internal rotors are better treated in HO approximation

try: 
	ho = input_search_list('$hofreq')
	HO = []
	for i in ho:
		HO.append(int(i[0]))
except:
	HO = []	

# get the info for free rotor
# $frrotor
# N1 N2 N3 ...
# N1 is freq
# N2, N3 are the bond
# ... is one part of the rotor - to be defined later automatically via connectivity

try:
	frrotor = input_search_list('$frrotor')
	FR = []
	for j in frrotor:
		for i in range (len(j)):
			j[i] = int(j[i])
			if i == 0:
				FR.append(j[i])
except:
	frrotor = []
	FR = []
#print (frrotor, FR)

Internal_rotation = False

# find the bond for rotation
f.seek(0)
for line in f:
	if '$bond' in line:
		Internal_rotation = True
#		print ('There is an internal rotation')
		bond = input_search_simple('$bond')

# to read the points value (steps for Schrodinger equation)
if Internal_rotation:
	points = int(input_search_simple('$steps')[0])

# find the frequency to be replaced with the rotation
if Internal_rotation:
	freq_rotor = int(input_search_simple('$freq_rotor')[0])

# find for the atoms forming the first rotor
if Internal_rotation:
	rotor = input_search_simple('$rotor')

# read the temperature
T = float(input_search_simple('$temperature')[0])

# read the multiplicity
mult = int(input_search_simple('$mult')[0])

# read the sigma - the symmetry number for rotation

sigma = float(input_search_simple('$sigma')[0])

# read the pressure in atm

P = float(input_search_simple('$pressure')[0])

# read the scale coefficient for frequency thermochemistry analysis

scale = float(input_search_simple('$scale')[0])


# accuracy to describe the potential

if Internal_rotation:
	accuracy =  input_search_simple('accuracy')[0]


# read the potential 
if Internal_rotation:
	potential = input_search_list('$potential')


#print potential	for j in range(n):

f.close()



#############################################################################################################
# end reading the input file
#############################################################################################################

# to put the number and the mass 

for i in range (len(molecule)):
	molecule[i].insert(1, elements[molecule[i][0]+' '])
for i in range (len(molecule)):
	molecule[i].insert(2, masses[molecule[i][0]+' '])

for i in range (len(molecule)):
	molecule[i][1] = int(molecule[i][1])
	molecule[i][2] = float(molecule[i][2])
	molecule[i][3] = float(molecule[i][3])
	molecule[i][4] = float(molecule[i][4])
	molecule[i][5] = float(molecule[i][5])

# to get the brutto formula of the compound

brutto = []
brutto_main = []
numbers = []
for i in range(len(molecule)):
	if molecule[i][0] in brutto: t=0 
	else: brutto_main.append(molecule[i][0]) 
	brutto.append(molecule[i][0])
#print (brutto)
#print (brutto_main)

for j in brutto_main:
	m = 0
	for i in brutto:
		if j == i: 
			m = m + 1
	numbers.append(m)

compound = ''
for i in range(len(brutto_main)):
	compound = compound + brutto_main[i]+str(numbers[i])
#print (compound)
#############################################################################################################
# To calculate principal moments of inertia
############################################################################################################# 

# to calculate the center of mass coordinates
# x = summ(mi*xi)/summ(mi)

mx = [[], [], []]
for i in range(len(molecule)):
	t = molecule[i][2]*molecule[i][3]
	mx[0].append(t)
	t = molecule[i][2]*molecule[i][4]
	mx[1].append(t)
	t = molecule[i][2]*molecule[i][5]
	mx[2].append(t)

m = []
for i in range(len(molecule)):
	m.append(molecule[i][2])

# the first three zeros just for formalities
com = [0,0,0]

for i in range(3):
	t = sum(mx[i])/sum(m)
	com.append(t)

# matrix of the moments of inertia
N = [[], [], []]

for i in range(3, 6, 1):
	for j in range(3, 6, 1):
		N[i-3].append(Iij(molecule, com, i, j))
#		print (Iij(molecule, com, i, j), i, j)

matr_N_new = N
matr_N = matrix(N)

#print (matr_N)
V,D = linalg.eig (matr_N)

#print (V)

# the principal moments of inertia
moments_of_inertia = make_a_list_array (array(V))

# to check whether the molecule is linear or not
Linear = False

moments_inertia = []

for i in moments_of_inertia:
	if round(i,8) == 0:
		Linear = True
		print ('Linear')

if Linear: 
	for i in moments_of_inertia:
		if round(i,8) != 0.00000000:
#			print (round(i,8))
			moments_inertia.append(i)
	if len(moments_inertia) !=0:
		q_rot = ((8*pi**2)*moments_inertia[0]*(I_amu_A2_to_kg_m2)*k_b*T/(sigma*h**2))
		################## thermodynamic of the rotation ######################
		H_rot = Rg*T/4.184 # cal/mol
		U_rot = Rg*T/4.184
		S_rot = Rg*(log(q_rot) + 1)/4.184 # cal/mol*K
		G_rot = H_rot - T*S_rot # cal/mol
		Cv_rot = Rg/4.184 # cal/mol*K
	else:
		q_rot = 1
		################## thermodynamic of the rotation ######################
		H_rot = 0 # cal/mol
		U_rot = 0
		S_rot = 0 # cal/mol*K
		G_rot = 0 # cal/mol
		Cv_rot = 0 # cal/mol*K
else: 
	I_rot = moments_of_inertia[0]*moments_of_inertia[1]*moments_of_inertia[2]
	q_rot = ((pi*I_rot*I_amu_A2_to_kg_m2**3)**0.5)*(1/sigma)*(8*pi**2*k_b*T/h**2)**1.5
	################## thermodynamic of the rotation ######################
	H_rot = 1.5*Rg*T/4.184 # cal/mol
	U_rot = 1.5*Rg*T/4.184
	S_rot = Rg*(log(q_rot) + 1.5)/4.184 # cal/mol*K
	G_rot = H_rot - T*S_rot # cal/mol
	Cv_rot = 1.5*Rg/4.184 # cal/mol*K

#print ('Rotation partition function ', q_rot)
#print ('Rotational entropy ', S_rot)
#print ('Rotational enthalpy', H_rot)
#print ('Rotational Gibbs Free energies', G_rot)
#print ('Rotational Cv contribution', Cv_rot)


############################################################################################
#   Ideal gas approximation
############################################################################################

# to calculate the mass of the molecule

m = []
for i in range(len(molecule)):
	m.append(molecule[i][2])

M = sum(m)
#print ('mass of the molecule ', M)

q_tr = ((2*pi*M*k_b*T*amu_to_kg)/h**2)**1.5*(k_b*T/(P*101325))

#print ('partition function for the translation', q_tr)

######################## thermodynamic functions ##########################################

S_tr = Rg*(log(q_tr)+ 1 + 1.5)/4.184
H_tr = 1.5*Rg*T/4.184 + Rg*T/4.184
U_tr = 1.5*Rg*T/4.184
G_tr = H_tr - T*S_tr
Cv_tr = 1.5*Rg/4.184

#print ('Translational partition function ', q_tr)
#print ('Translational entropy ', S_tr)
#print ('Translational enthalpy', H_tr)
#print ('Translational Gibbs Free energies', G_tr)
#print ('Translational Cv contribution', Cv_tr)




##########################################################################################
# Frequencies analysis
##########################################################################################

freq_thermo = []
#print (freq_raw)

# to scale the frequencies
for i in range(len(freq_raw)):
	fri = float(freq_raw[i][0])*scale
	if thld!=0:
		if fri < thld:
			fri=thld
	freq_thermo.append(fri)
		

#print (freq_thermo)
# to calculate the partition function for frequencies

q_freq = []

# Entropy of Grimme, eq. 5 (https://pubs.rsc.org/en/content/articlepdf/2021/sc/d1sc00621e)

def SR (v,T,Bav):
	mu = h / (8*(pi**2)*v*cm_to_hertz)
	mup = mu*Bav/(mu+Bav)
	eq0 = 8*(pi**3)*mup*k_b*T/(h**2)
	eq1 = eq0**0.5
	eq2 = log(eq1)
	S = Rg * (0.5 + eq2)
	return S 

# Grimme's parameters

tau = float(GR[0][0])
alpha = float(GR[1][0])
HG = False
if int(GR[2][0]) == 0:
	HG = False
else:
	HG = True
j=0
for i in moments_of_inertia:
	j = j + i
j=j/len(moments_of_inertia)
Bav = j*I_amu_A2_to_kg_m2


for i in range(len(freq_thermo)):
	if freq_thermo[i] > 0:
		Q = h*freq_thermo[i]*c/k_b
		ZP = (h*freq_thermo[i]*c*Na)/(2*4.184*1000) 
		q = 1/(1 - exp(-h*freq_thermo[i]*c/(k_b*T)))
		S = Rg*(((Q/T)/(exp(Q/T) - 1)) - log(1-exp(-Q/T)  ))/4.184
		E = Rg*(Q*(0.5 + (1/(exp(Q/T) - 1))))/(1000*4.184)
		Cv = (Rg*((Q/T)**2)*(e**(Q/T))/(e**(Q/T)-1)**2)/4.184
		# entropy of Grimme, eq. 7
		eq0 = 1 + (tau/freq_thermo[i])**alpha
		Sg = 4.184*S/eq0 + (1-1/eq0)*SR(freq_thermo[i],T,Bav)
		Sg=Sg/4.184
		# Cv in Grimme's approach
		Cvg = 4.184*Cv/eq0 + (1-1/eq0)*0.5*Rg
		Cvg = Cvg/4.184
		# if H is also treated by Grimme's approach
		Eg = 1000*4.184*E/eq0 + (1-1/eq0)*0.5*Rg*T
		Eg = Eg/(1000*4.184)
		if i+1 in HO:
			q_all = [i+1, round(float(freq_raw[i][0]), 3), freq_thermo[i], 'yes (HO)', q, ZP, E, S, E-(T*S)/1000, Cv]
		elif i+1 in FR:
			# we treat this frequency as free rotor
			# get the index of i+1
			ind = FR.index(i+1)
			I = MIB (molecule, frrotor[ind])
			q_fr,e_fr = free_rotor(I, 84000)
			u_fr_summ = []
			for i1 in range(len(e_fr)):
				u = e_fr[i1]*e**(-e_fr[i1]/(k_b*T))
				u_fr_summ.append(u)
			U_fr = (1/q_fr)*sum(u_fr_summ)*Na
			S_fr = k_b*log(q_fr)*Na + U_fr/T
			# to calory system
			U_fr = U_fr/(1000*4.184) # kcal/mol
			S_fr = S_fr/4.184 # cal/mol*K
			H_fr = U_fr
			G_fr = U_fr - (T*S_fr)/1000
			Cv_fr = 0.5*Rg/4.184
			q_all = [i+1, round(float(freq_raw[i][0]), 3), freq_thermo[i], 'yes (FR)', q_fr, 0, H_fr, S_fr, G_fr, Cv_fr]
		else:		
			if HG == False:			
				q_all = [i+1, round(float(freq_raw[i][0]), 3), freq_thermo[i], 'yes', q, ZP, E, Sg, E-(T*Sg)/1000, Cvg]
			else:
				q_all = [i+1, round(float(freq_raw[i][0]), 3), freq_thermo[i], 'yes', q, ZP, Eg, Sg, Eg-(T*Sg)/1000, Cvg]
	else: 
		q_all = [i+1, float(freq_raw[i][0]), freq_thermo[i], 'no', 0.00000, 0.000, 0.000, 0.000, 0.000, 0.000]
	q_freq.append(q_all)

#print ('frequencies')
#print (q_freq)

####################################################### Electronic ##########################################

# just take the multiplicity into account

q_el = mult
S_el = Rg*log(q_el)/4.184 # cal/mol*K
H_el = 0
U_el = 0
G_el = 0
Cv_el = 0

############################################################################################################
# To carry out the potential 
############################################################################################################

#to put the n for Fourier expansion
# to describe the given potential analytically
# To get it describe we define the accuracy we need. I have taken accuracy as a summ of the deviations (Ei(theor) - Ei(Fourier)) devided by the number of points 

#print (int(len(potential)/2))

#for ii in range(1, int(len(potential)/2)+1, 1):
if Internal_rotation:
	for ii in range(1, 1000+1, 1):
		# the lists for the values of the angles and corresponding energies in kcal/mol
		X = []
		E = []
	#	print (ii)
		for q in potential:
			X.append(float(q[0]))
			E.append(float(q[1]))
		N1 = []
		for i in range(ii):
			N1.append(i+1)
			N = []
		N.append(1)
		for i in N1:
			i = float(i)
			N.append(i)
			N.append(i)
		Q = []
		for i in N:
			i = []
			Q.append(i)
		for i in range(1, len(N), 2):
			for k in X:
				A = Function_cos(N[i], k)
				Q[i].append(A)
		for i in range(2, len(N), 2):
			for k in X:
				A = Function_sin(N[i], k)
				Q[i].append(A)
	
		for i in range(1):
			for k in X:
				A = 1
				Q[i].append(A)

	
		Q = matrix(Q)
		A = Q.T
		AT = A.T
		E = matrix(E)
		E = E.T

		# Knut's equation
	#	a = (AT*A).I*(AT*E)
		a = (A.I)*E
	#	print ('Determinant', numpy.linalg.det(AT*A))
		E1 = A*a
		# the array with the obtained energies
		E1 = array(E1)
		# the array with the initial energies
		E= array(E)
		parameter = []
		for i in range(len(E1)):
			t = abs(E[i] - E1[i])
			parameter.append(t)
	#	print ('I am here')
	#	print (sum(parameter)/len(parameter)	 )
		if sum(parameter)/len(parameter) < float(accuracy):
			accuracy_achieved = True
			accuracy_f = float(sum(parameter)/len(parameter))
	#		print ('The accuracy is achived, '+ str(sum(parameter)/len(parameter))+ ' is less then '+str(accuracy))
			break
		print (len(potential))
		if ii == int((len(potential)-1)/2):
			accuracy_achieved = False
			accuracy_f = float(sum(parameter)/len(parameter))
			break


	f.close()
	E1=make_a_list_array(E1)

#	# to put analytically describe potential in the file
#
#	# to put the original potential
#	f = open(sys.argv[1][0:-3]+'dat', 'w')
#	for i in range(len(X)):
#		f.write('%10.2f %8.5f\n' % (X[i], E[i]))
#	f.close()
#	# to put the analytically calculated potential
#	f = open(sys.argv[1][0:-4]+'-f'+'.dat', 'w')
#	for i in range(len(X)):
#		f.write('%10.2f %8.5f\n' % (X[i], E1[i]))
#	f.close()


	a = array(a)
	a_final = make_a_list_array (a)

	
	
	results = []

	# to define the step
	step = (X[-1]-X[0])/points


	array_3 = []

	# to create the list to store the angle (with the steps), its potential, hamiltonian
	all_x_f = []
	
	for i in range(points+1):
		array_3.append(i)
		all_x_f.append(i)

	for i in range(points+1):
		array_3[i] = []
		all_x_f[i] = []

	array_4 = []


	for j in range (points+1):
		x = X[0]+step*j
		array_4.append(x)
		# to scale to be from -pi to +pi
#		all_x_f[j].append(  ((X[0]+step*j - X[0] -180)/180)*pi  )
		all_x_f[j].append(  ((X[0]+step*j)/180)*pi  )

		for i in range(1, len(N), 2):
			t = a_final[i]*Function_cos(N[i], x)
			array_3[j].append(t)
		for i in range(2, len(N), 2):
			y = a_final[i]*Function_sin(N[i], x)
			array_3[j].append(y)
		array_3[j].append(a_final[0]*1)

	# redifne te step to be in pi
	step = (all_x_f[-1][0]-all_x_f[0][0])/points

	for i in range(len(array_3)):
		all_x_f[i].append(sum(array_3[i]))

	for i in range(len(array_3)):
		print (str(array_4[i])+' , '+str(sum(array_3[i])))
	
	parameter = []

	for i in range(len(E1)):
		t = abs(E[i] - E1[i])
		parameter.append(t)

#############################################################################################
# To carry out the moment of inertia
#############################################################################################

	rotor_1 = []
	rotor_2 = []

# to put atoms in the rotor1 and rotor2

	for i in range(len(molecule)):
		if str(i+1) in rotor:
			rotor_2.append(molecule[i])
		else: rotor_1.append(molecule[i])

	rotor_1_inertia = []
	rotor_2_inertia = []

# to calculate the mr2 term for rotor1 and for rotor2

	for i in range(len(rotor_1)):
		t = mr2(molecule[int(bond[0])-1], molecule[int(bond[1])-1], rotor_1[i])
		rotor_1_inertia.append(t)


	for i in range(len(rotor_2)):
		t = mr2 (molecule[int(bond[0])-1], molecule[int(bond[1])-1], rotor_2[i])
		rotor_2_inertia.append(t)

# to calculate the reduced moment of inertia I = I1*I2/(I1 + I2)

	I = sum(rotor_1_inertia)*sum(rotor_2_inertia)/(sum(rotor_1_inertia) + sum(rotor_2_inertia))
#	print (rotor_1_inertia)
#	print (rotor_2_inertia)
#	print (rotor_2)
#	print (I)


#print (rotor_2)
#I = sum(rotor_2_inertia)

#print ('moment of inertia', I)


############################################################################################
# To solve the Schrodinger equation for hindered rotor
############################################################################################


# to put some values to the array all_x_f

	for i in range(points+1):
		all_x_f[i].insert(0, i)
		all_x_f[i].insert(3, -h_2pi**2/(2*I*I_amu_A2_to_kg_m2*step**2))
	#	all_x_f[i].insert(3, -h_2pi**2/(2*1.57*I_amu_A2_to_kg_m2*step**2))
	
	#	all_x_f[i].insert(3, 0)
	#	all_x_f[i].insert(3, -h_2pi**2/(2*I*I_amu_A2_to_kg_m2*step**2)) # this is for free rotor
	
	
	#	print (all_x_f[i][2])
		all_x_f[i].insert(4, (all_x_f[i][2]*kcal_to_j + h_2pi**2/(I*I_amu_A2_to_kg_m2*step**2)   ))
	#	all_x_f[i].insert(4, (all_x_f[i][2]*kcal_to_j + h_2pi**2/(1.57*I_amu_A2_to_kg_m2*step**2)   ))
	
	#	all_x_f[i].insert(4, (all_x_f[i][2]*kcal_to_j  ))
	#	all_x_f[i].insert(4, (h_2pi**2/(I*I_amu_A2_to_kg_m2*step**2)   )) # this is for free rotor
	
	#print (all_x_f)

	# to create the matrix F, see the article of G. Ercolani
	F = []

	for i in range(1, points+1):
		F.append(i)
	for i in range(len(F)):
		F[i] = []
	# to put all zeroes to the matrix
	for i in range(len(F)):
		for j in range(len(F)):
			F[i].append(0)
	# to put the coefficients bi to the diagonal
	for i in range(len(F)):
		F[i][i] = all_x_f[i+1][4]
	# to put a 
	for i in range(len(F)-1):
		F[i][i+1] = all_x_f[i+1][3]
	# to put a
	for i in range(1, len(F)):
		F[i][i-1] = all_x_f[i+1][3]
	# put a in the corners
	F[len(F)-1][0] = all_x_f[len(F)-1][3]
	F[0][len(F)-1] = all_x_f[0][3]


	# to get the matrix F and diagonalize it
	F = matrix(F)
	#print (F)
	# V - the diagonal matrix, D - the matrix of wavefunctions
	V,D = linalg.eig(F)

	#print (F)
	#print (V)
	#print (D)

	# for some reasons the diagonal elements Ej are placed in the mixed order, that's why we need to sort it
	E_j = sort(V)


	# to calculate the partition function
	# Q = summ(e**(Ei/kT))
	E_j = make_a_list_array(array(E_j))

#	print (E_j)
	Q_all = []
	for i in range(len( E_j)):
		q = e**(-E_j[i]/(k_b*T))
#		print (q)
		Q_all.append(q)
	Q_rotation = sum(Q_all)
	
	print (Q_rotation)

	Q_all = []

	for i in range(1, len( E_j)+1):
		q = e**(-E_j[len(E_j)-i]/(k_b*T))
	#	print (q)
		Q_all.append(q)
	Q_rotation = sum(Q_all)
	#Q_rotation=0.5*Q_rotation
	print (Q_rotation)
	
	#print ('The energies')
	#for i in E_j:
	#	print ((i*Na)/1000)

#	print ('Enthalpy')

	u_summ = []
	for i in range(len(E_j)):
		u = E_j[i]*e**(-E_j[i]/(k_b*T))
		u_summ.append(u)
	U = (1/Q_rotation)*sum(u_summ)*Na
	
	S = k_b*log(Q_rotation)*Na + U/T
#	S = k_b*log(Q_rotation)*Na + (U-U0)/T




	U_hr = U/(1000*4.184) # kcal/mol
	S_hr = S/4.184 # cal/mol*K
	H_hr = U/(1000*4.184)
	G_hr = U/(1000*4.184) - (T*S/4.184)/1000
#	print (S_hr)
#	print (H_hr)
############################### to calculate the free rotor approximation ##########################

	q_fr,e_fr = free_rotor(I, 84000)

#	print (q_fr)
########### TD functions ##############

	u_fr_summ = []
	for i in range(len(e_fr)):
		u = e_fr[i]*e**(-e_fr[i]/(k_b*T))
		u_fr_summ.append(u)
	U_fr = (1/q_fr)*sum(u_fr_summ)*Na
	S_fr = k_b*log(q_fr)*Na + U_fr/T

	U_fr = U_fr/(1000*4.184) # kcal/mol
	S_fr = S_fr/4.184 # cal/mol*K
	H_fr = U_fr/(1000*4.184)
	G_fr = U_fr/(1000*4.184) - (T*S_fr)/1000



#	print (S_fr)
#	print (U_fr)

##################################################################################################
# To print everything in a file
##################################################################################################
f = open(sys.argv[1][0:-3]+'td', 'w')
f.write ("       \n"
        "       Thermochemistry v.1.0.0 (28.05.2024)\n"
        "       Copyright: Yury Minenkov\n"
        "       N.N. Semenov Federal Research Center\n"
        "       of Chemical Physics RAS\n"
        "       119991 Moscow, The Russian Federation\n"
        "       Kosygina street, 4\n"
        "       \n"
);
axis = ['x', 'y', 'z']
f.write('%45s %23s\n' % ('The thermochemical analysis of the Molecule: ', compound))
f.write('\n')
write_line(f,'-',75,2)
f.write('%10s %6s %16s %18s %18s\n' % ( ' N ', ' M ', 'x', 'y', 'z'))
write_line(f,'-',75,2)
for i in range(len(molecule)):
	f.write('%3s %5i %10.5f %18.10f %18.10f %18.10f\n' % (molecule[i][0], molecule[i][1], molecule[i][2], molecule[i][3], molecule[i][4], molecule[i][5]   ))
write_line(f,'-',75,2)
f.write('\n')
f.write('%58s\n' % ('The external parameters for thermodynamic calculations:'))
write_line(f,'-',75,2)
f.write('%50s %10.5f\n' % ('Pressure (atm): ', P))
f.write('%50s %10.5f\n' % ('Temperature (Kelvin): ', T))
f.write('%50s %10i\n' % ('Symmetry number (sigma): ', sigma))
f.write('%50s %10.5f\n' % ('The frequencies scale coefficient: ', scale)) 
f.write('%50s %10i\n' % ('The frequencies number: ', len(freq_raw)))
write_line(f,'-',75,2)
f.write('\n')
if Internal_rotation:
	write_symbol(f,'=',10,3)
	f.write('%50s' % ('The internal rotation options have been found   '))
	write_symbol(f,'=',10,0)
	f.write('\n')
	write_line(f,'-',75,2)
	f.write('%50s %8i %3i\n' % ('The rotation bond: ', int(bond[0]), int(bond[1])))
	f.write('%50s %8i\n' % ('The step size (the basis set): ', points))
	f.write('%50s \n' % ('The atoms in the rotor: '))
	f.write('\n')
	for i in range(0,len(rotor),3):
		if i+2<len(rotor):
			f.write('%45s %3s %3s\n' % (rotor[i], rotor[i+1], rotor[i+2]))
		else: 
			if i+1<len(rotor):
				f.write('%45s %3s\n' % (rotor[i], rotor[i+1]))
			else: f.write('%45s\n' % (rotor[i]))
	f.write('\n')
	f.write('%50s %10.5f\n' % ('The accuracy of Fourier transformation: ', float(accuracy)))
	f.write('\n')
	f.write('%50s\n' % ('The rotation potential (kcal/mol): '))
	f.write('\n')
	for i in range(len(potential)):
		f.write('%45.1f %10.3f\n' % (float(potential[i][0]), float(potential[i][1])))
else: 
	f.write('%3s\n' % ('The internal rotation options have not been found'))
	f.write('%3s\n' % ('The hindered rotation will not be considered'))	
f.write('\n')
write_symbol(f,'=',10,3)
f.write('%50s' % (' The reading of the input file has been finished '))
write_symbol(f,'=',10,0)
f.write('\n')
f.write('\n')
f.write('\n')
write_line(f,'=',75,2)
f.write('%58s\n' % ('The thermochemistry evaluation at '+str(T)+' K'+' and '+str(P)+' atm'))
write_line(f,'=',75,2)
f.write('\n')
f.write('%3s\n' % ('      ******    Rotation of a molecule as a whole     *****'))
f.write('\n')
write_line(f,'-',75,2)
f.write('%55s\n' % ('The approximation : Rigid rotor'))
write_line(f,'-',75,2)
f.write('%45s\n' % ('The coordinates of the center of mass: '))
f.write('%15s %15s %15s\n' % ('x', 'y', 'z'))
f.write('%20.8f %15.8f %15.8f\n' % (round(com[3], 8), round(com[4], 8), round(com[5], 8)))
f.write('\n')
f.write('%68s\n' % ('The non-diagonalized matrix moments of inertia (amu*A**2): '))
f.write('%18s %15s %15s\n' % (axis[0], axis[1], axis[2]))
for i in range(len(matr_N_new)):
	f.write('%5s %15.5f %15.5f %15.5f\n' % ( axis[i], matr_N_new[i][0], matr_N_new[i][1], matr_N_new[i][2]    ))
f.write('\n')
f.write('%55s\n' % ('Principal moments of inertia (amu*A**2): '))
f.write('%25.8f %20.8f %20.8f\n' % (round(moments_of_inertia[0], 5), round(moments_of_inertia[1], 5), round(moments_of_inertia[2], 5)))
f.write('\n')
if Linear:
	f.write(('%55s\n' % ('The molecule was found to be linear.')))
else:
	f.write(('%55s\n' % ('The molecule was found to be non-linear.')))
f.write('\n')
f.write('%3s\n' % ('               *****     Rotation thermodynamic functions     *****'))
f.write('\n')
f.write('%12s %25.5f %15s %10.5f\n' % (' Q rotation', q_rot, ' The ln(Q)', log(q_rot)))
f.write('\n')
f.write('%12s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' H rotation', H_rot/1000, '(kcal/mol)', (H_rot/1000)*4.184, '(kJ/mol)', (H_rot/1000)*1.5936e-3, '(hartree)'   ))
f.write('%12s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' U rotation', U_rot/1000, '(kcal/mol)', (U_rot/1000)*4.184, '(kJ/mol)', (U_rot/1000)*1.5936e-3, '(hartree)'   ))
f.write('%12s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' Cv rotation', Cv_rot, '(cal/mol*K)', Cv_rot*4.184, '(J/mol*K)', (Cv_rot/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%12s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' S rotation', S_rot, '(cal/mol*K)', S_rot*4.184, '(J/mol*K)', (S_rot/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%12s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' G rotation', G_rot/1000, '(kcal/mol)', (G_rot/1000)*4.184, '(kJ/mol)', (G_rot/1000)*1.5936e-3, '(hartree)'   ))
f.write('\n')
f.write('\n')
f.write('%55s\n' % ('             *****     Translation of a molecule as a whole     *****'))
f.write('\n')
write_line(f,'-',75,2)
f.write('%55s\n' % ('The approximation : Ideal gas '))
write_line(f,'-',75,2)
f.write('%45s %10.5f %5s\n' % ('The molecular mass: ', M, 'amu'))
f.write('\n')
f.write('%3s\n' % ('              *****      Translation thermodynamic functions     ******'))
f.write('\n')
f.write('%15s %25.5f %15s %10.5f\n' % (' Q translation', q_tr, ' The ln(Q)', log(q_tr)))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' H translation', H_tr/1000, '(kcal/mol)', (H_tr/1000)*4.184, '(kJ/mol)', (H_tr/1000)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' U translation', U_tr/1000, '(kcal/mol)', (U_tr/1000)*4.184, '(kJ/mol)', (U_tr/1000)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' Cv translation', Cv_tr, '(cal/mol*K)', Cv_tr*4.184, '(J/mol*K)', (Cv_tr/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' S translation', S_tr, '(cal/mol*K)', S_tr*4.184, '(J/mol*K)', (S_tr/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' G translation', G_tr/1000, '(kcal/mol)', (G_tr/1000)*4.184, '(kJ/mol)', (G_tr/1000)*1.5936e-3, '(hartree)'   ))
f.write('\n')
f.write('\n')
f.write('%3s\n' % ('                *****      Molecular vibrations     *****'))
f.write('\n')
write_line(f,'-',75,2)
if float(GR[0][0]) < 0.01 and float(GR[1][0]) > 999:
	f.write ('%64s\n' % ('The approximation : Harmonic oscillator'))
else:
	f.write('%64s\n' % ('The approximation : msRRHO of Grimme'))
	f.write('%23s TAU=%5.4s ALPHA=%5.4s ENTHALPY_CORRECTION=%5s\n' % (' ', GR[0][0], GR[1][0], GR[2][0]))
write_line(f,'-',75,2)
j = 0
for i in range(len(freq_raw)):
	if float(freq_raw[i][0]) < 0:
		j = j+1
f.write('%55s %3i\n' % ('The number of frequencies: ', len(freq_thermo)))
f.write('%55s %3i %3s\n' % ('The number of imaginary frequencies: ', j, '(no TD analysis)'))
f.write('%55s %3i\n' % ('The number of frequencies used in TD analysis: ', len(freq_thermo)-j))
f.write('\n')
f.write('\n')
f.write('%5s %10s %15s %10s %10s %10s %10s %12s %12s %12s\n' % ('N ', 'Freq (cm-1)', 'Freq (cm-1)', 'TD?', 'Q', 'ZPE', 'H', 'S', 'G', 'Cv' ))
f.write('%5s %10s %14s %10s %10s %15s %11s %13s %12s %12s\n' % (' ', ' ', 'Scaled', ' ', ' ', 'kcal/mol', 'kcal/mol', 'cal/mol*K', 'kcal/mol', 'cal/mol*K' ))
for i in range(len(q_freq)):
	f.write('%3i %12.3f %15.3f %11s %13.5f %8.3f %12.3f %12.3f %12.3f %12.3f\n' % (q_freq[i][0], q_freq[i][1], q_freq[i][2], q_freq[i][3], q_freq[i][4], q_freq[i][5], q_freq[i][6], q_freq[i][7], q_freq[i][8], q_freq[i][9]))
f.write('\n')
f.write('%3s\n' % ('                   *****     Vibration thermodynamic functions     ******'))
f.write('\n')
q_vib = 1
H_vib = 0
ZPE = 0
S_vib = 0
G_vib = 0
Cv_vib = 0
Sg_vib = 0
Cvg_vib = 0
for i in range(len(q_freq)):
	if 'yes' in q_freq[i][3]:
		q_vib = q_vib*q_freq[i][4]
		H_vib = H_vib+q_freq[i][6]
		ZPE = ZPE + q_freq[i][5]
		S_vib = S_vib + q_freq[i][7]
		G_vib = G_vib + q_freq[i][8]
		Cv_vib = Cv_vib + q_freq[i][9]
f.write('%15s %25.5f %15s %10.5f\n' % (' Q vibration', q_vib, ' The ln(Q)', log(q_vib)))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' H vibration', H_vib, '(kcal/mol)', (H_vib)*4.184, '(kJ/mol)', (H_vib)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' U vibration', H_vib, '(kcal/mol)', (H_vib)*4.184, '(kJ/mol)', (H_vib)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' ZPE ', ZPE, '(kcal/mol)', ZPE*4.184, '(kJ/mol)', (ZPE)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' S vibration', S_vib, '(cal/mol*K)', S_vib*4.184, '(J/mol*K)', (S_vib/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' Cv vibration', Cv_vib, '(cal/mol*K)', Cv_vib*4.184, '(J/mol*K)', (Cv_vib/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' G vibration', G_vib, '(kcal/mol)', (G_vib)*4.184, '(kJ/mol)', (G_vib)*1.5936e-3, '(hartree)'   ))
f.write('\n')
f.write('\n')
f.write('%3s\n' % ('                       *****      Electronic part     *****     '))
f.write('\n')
write_line(f,'-',75,2)
f.write('%55s\n' % ('The approximation : Consider just multiplicity'))
write_line(f,'-',75,2)
f.write('%55s %10i \n' % ('The molecule multiplicity ', mult))
f.write('%3s\n' % ('                      *****     Electronic thermodynamic functions     *****    '))
f.write('\n')
f.write('%15s %25.5f %15s %10.5f\n' % (' Q electronic', q_el, ' The ln(Q)', log(q_el)))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' H electronic', H_el/1000, '(kcal/mol)', (H_el/1000)*4.184, '(kJ/mol)', (H_el/1000)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' U electronic', U_el/1000, '(kcal/mol)', (U_el/1000)*4.184, '(kJ/mol)', (U_el/1000)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' Cv electronic', Cv_el, '(cal/mol*K)', Cv_el*4.184, '(J/mol*K)', (Cv_el/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' S electronic', S_el, '(cal/mol*K)', S_el*4.184, '(J/mol*K)', (S_el/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' G electronic', G_el/1000, '(kcal/mol)', (G_el/1000)*4.184, '(kJ/mol)', (G_el/1000)*1.5936e-3, '(hartree)'   ))
f.write('\n')
f.write('\n')



f.write('%3s\n' % ('                     *****     Final values for TD functions (no internal rotation)     *****'))
f.write('\n')
f.write('%15s %25.5f %15s %10.5f\n' % (' Q total', q_tr*q_rot*q_vib*q_el, ' The ln(Q)', log(q_tr*q_tr*q_vib*q_el)))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' H total', (H_tr+H_rot)/1000+H_vib, '(kcal/mol)', ((H_tr+H_rot)/1000+H_vib)*4.184, '(kJ/mol)', ((H_tr+H_rot)/1000+H_vib)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' U total', (U_tr+U_rot)/1000+H_vib, '(kcal/mol)', ((U_tr+U_rot)/1000+H_vib)*4.184, '(kJ/mol)', ((U_tr+U_rot)/1000+H_vib)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' Cv total', Cv_tr+Cv_rot+Cv_el+Cv_vib, '(cal/mol*K)', (Cv_tr+Cv_rot+Cv_el+Cv_vib)*4.184, '(J/mol*K)', ((Cv_tr+Cv_rot+Cv_el+Cv_vib)/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' ZPE ', ZPE, '(kcal/mol)', ZPE*4.184, '(kJ/mol)', (ZPE)*1.5936e-3, '(hartree)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' S total', (S_tr+S_vib+S_rot+S_el), '(cal/mol*K)', (S_tr+S_vib+S_rot+S_el)*4.184, '(J/mol*K)', ((S_tr+S_vib+S_rot+S_el)/1000)*1.5936e-3, '(hartree/K)'   ))
f.write('%15s %14.5f %12s %12.5f %12s %18.8f %12s\n' % (' G total', (G_tr+G_rot+G_el)/1000+G_vib+Rg*T/(4.184*1000), '(kcal/mol)', ((G_tr+G_rot+G_el)/1000+G_vib+Rg*T/(4.184*1000))*4.184, '(kJ/mol)', ((G_tr+G_rot+G_el)/1000+G_vib+Rg*T/(4.184*1000))*1.5936e-3, '(hartree)'   ))
f.write('\n')
f.write('\n')

f.write('%3s\n' % ('                    *****     Final corrections for TD functions (no internal rotation)     *****'))
f.write('\n')
f.write('%55s %12.8f %8s\n' % (' Thermal correction to Energy :', ((U_tr+U_rot)/1000+H_vib)*1.5936e-3, '(hartree)'   ))
f.write('%55s %12.8f \n' % (' Thermal correction to Enthalpy :', ((H_tr+H_rot)/1000+H_vib)*1.5936e-3))
f.write('%55s %12.8f %8s\n' % (' Thermal correction to Gibbs Free Energy :',  (  ( (H_tr+H_rot)/1000 + H_vib       ))*1.5936e-3 - (T*(S_tr+S_vib+S_rot+S_el)/1000)*1.5936e-3, '(hartree)'   ))
f.write('%55s %12.8f %8s\n' % (' ZPE correction to the Electronic Energy :', (ZPE)*1.5936e-3, '(hartree)'   ))
f.write('\n')
f.write('\n')
if Internal_rotation:
	write_symbol(f,'=',10,3)
	f.write('%50s' % ('Internal rotation consideration   '))
	write_symbol(f,'=',10,0)
	f.write('\n')
	write_line(f,'-',75,2)
	f.write('%55s\n' % ('The potential description : Fourier transformation '))
	write_line(f,'-',75,2)
	f.write('\n')
	if accuracy_achieved:
		f.write('%35s %10.5f %10s %10.5f %10s %10i %10s\n' % ('The accuracy is achieved ', accuracy_f, ' is less then ', float(accuracy), '(', ii, 'iterations)' ))
	else:
		f.write('%35s %10.5f %10s %10.5f %10s %10i %10s\n' % ('The accuracy is not achieved ', accuracy_f, ' is not less then ', float(accuracy), '(', ii, 'iterations)' ))
		f.write('          That is the limit of Fourier expansion\n')	
	f.write('\n')
	f.write('%33s\n' % ('The theoretical and Fourier potential: '))
	f.write('\n')
	f.write('%33s %10s %12s\n' % ('Angle', 'Theor', 'Fourier'))
	f.write('%33s %12s %12s\n' % ('(deg)', '(kcal/mol)', '(kcal/mol)'))
	f.write('\n')
	for i in range(len(X)):
		#print (X[i], ',', E[i], ',', E1[i])
		f.write('%33.2f %2s %8.5f %2s %8.5f\n' % (X[i], ',', E[i][0], ',', E1[i]))
	f.write('\n')
	f.write('%10s %10.8f %5s\n' % ('The reduced moment of inertia for the bond '+str(bond[0])+' '+str(bond[1])+' ', I, '(amu*A**2)'))
	f.write('\n')
	f.write('%55s\n' % ('The hamiltonian matrix '))
	f.write('\n')
	f.write('%3s\n' % (F))
	f.write('\n')
	f.write('%55s\n' % ('The diagonalized hamiltonian matrix'))
	f.write('\n')
	f.write('%3s\n' % (V))
	f.write('\n')
	f.write('%55s\n' % (' The wavefunctions matrix F'))
	f.write('\n')
	f.write('%3s\n' % (D))
	f.write('\n')
	f.write('%3s\n' % ('                *****     Internal Rotation thermodynamic functions     *****'))
	f.write('\n')
	f.write('%54s %15s %15s\n' % ('H-O', 'F-R', 'H-R'))
	f.write('%35s %20.5f %16.5f %14.5f\n' % (' Q ',q_freq[freq_rotor-1][4], q_fr , Q_rotation))
	f.write('%35s %20.5f %16.5f %14.5f\n' % (' U (kcal/mol) ',q_freq[freq_rotor-1][6], U_fr , U_hr))
	f.write('%35s %20.5f %16.5f %14.5f\n' % (' H (kcal/mol)',q_freq[freq_rotor-1][6], U_fr , U_hr))
	f.write('%35s %20.5f %16.5f %14.5f\n' % (' S (cal/mol*K)',q_freq[freq_rotor-1][7], S_fr , S_hr))
	f.write('%35s %20.5f %16.5f %14.5f\n' % (' G (kcal/mol)',q_freq[freq_rotor-1][8], G_fr , G_hr))
	f.write('\n')
	f.write('%3s\n' % ('                *****     Final values for TD functions (internal rotation)     *****'))
	f.write('\n')
	f.write('%55s %15s\n' % ('H-O', 'H-R'))
	f.write('%35s %22.5f %16.5f\n' % (' ln Q ',log(q_vib*q_tr*q_rot*q_el), log(q_tr*(q_vib*Q_rotation/q_freq[freq_rotor-1][4])*q_el*q_rot)))
	f.write('%35s %22.5f %16.5f\n' % (' U (kcal/mol) ', H_vib+(U_rot+U_tr)/1000+U_el, -q_freq[freq_rotor-1][6] + U_hr +H_vib+(U_rot+U_tr)/1000+H_el))
	f.write('%35s %22.5f %16.5f\n' % (' H (kcal/mol)', H_vib+((H_rot+H_tr)/1000)+H_el, -q_freq[freq_rotor-1][6] + U_hr + H_vib+(H_rot+H_tr)/1000+H_el))
	f.write('%35s %22.5f %16.5f\n' % (' S (cal/mol*K)', S_vib+S_rot+S_tr+S_el, -q_freq[freq_rotor-1][7] + S_hr + S_vib+S_rot+S_tr+S_el))
	f.write('%35s %22.5f %16.5f\n' % (' G (kcal/mol)', G_vib+(G_rot+G_tr)/1000+G_el+Rg*T/(4.184*1000), -q_freq[freq_rotor-1][8] + G_hr + G_vib+(G_rot+G_tr)/1000+G_el+Rg*T/(4.184*1000)))
	f.write('\n')

	f.write('%3s\n' % ('               *****     Final corrections for TD functions (internal rotation) *****'))
	f.write('\n')
	f.write('%55s %12.8f %5s\n' % (' Thermal correction to Energy :', ((U_tr+U_rot)/1000+H_vib-q_freq[freq_rotor-1][6]+U_hr)*1.5936e-3, '(hartree)'   ))
	f.write('%55s %12.8f \n' % (' Thermal correction to Enthalpy :', ((H_tr+H_rot)/1000+H_vib-q_freq[freq_rotor-1][6]+U_hr)*1.5936e-3   ))
	f.write('%55s %12.8f %5s\n' % (' Thermal correction to Gibbs Free Energy :',  (( (H_tr+H_rot)/1000 + H_vib-q_freq[freq_rotor-1][6]+U_hr ))*1.5936e-3 - 0.001*(T*(S_tr+S_vib+S_rot+S_el-q_freq[freq_rotor-1][7]+S_hr))*1.5936e-3, '(hartree)'   ))
	f.write('\n')
	f.write('\n')
	
	
