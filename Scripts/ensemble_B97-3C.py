#!/usr/bin/python
import sys, string, os, glob
import subprocess
from math import *
from multiprocessing import Pool
import multiprocessing
import random



td = ['GR_100_4_1', 'GR_50_4_1', 'GR_25_4_1', 'HO', 'HO_100', 'HO_175']
#td = ['GR_25_4_1']
Temp = []

# length of array of temperatures
d = len(sys.argv)
if d > 1:
	for i in range(d-1):
		Temp.append(sys.argv[i+1])
else:
	print ("List temperature values after ensemble_B97-3C.py in K as arguments, e.g. 298.15 300 310 .. ")
	sys.exit(0)

# get current folder's path
path=os.path.abspath( os.path.dirname( __file__ ) )

def parallel_run(j):
	# change the temperature in dat file
	out = subprocess.check_output("mv "+j[0][0:-4]+'.dat '+j[0][0:-4]+'.dat_cp ', shell=True)
	fr = open (j[0][0:-4]+'.dat_cp', 'r')
	fw = open (j[0][0:-4]+'.dat', 'w')
	while True:
		s = fr.readline()
		if not s:
			break
		else:
			if '$temperature' in s:
				fw.write(s)
				fw.write(j[1]+'\n')
				s = fr.readline()
			else:
				fw.write(s)
	fr.close()
	fw.close()
	out = subprocess.check_output("rm "+j[0][0:-4]+'.dat_cp ', shell=True)
	out = subprocess.check_output("python3 "+path+"/thermochemistry_mmRRHO.py "+j[0][0:-4]+'.dat '+j[2], shell=True)

# for each temperature in array
# entropies
ALL_TEMP = []
ALL_TEMP_SIM = []
# enthalpies
ALL_TEMP_H = []
ALL_TEMP_HIM = []

for m in Temp:
	tmp0 = []	
	tmp0.append(m)
	tmp1 = []
	tmp1.append(m) 
	for n in td:
		if __name__ == '__main__':
			filelist = glob.glob('*.xyz')
			# list that contains filename.xyz, T
			fTtd = []
			for i in filelist:
				fTtd.append((i,m,n))
			cpu_count = multiprocessing.cpu_count()
			with Pool(cpu_count) as pool:
				pool.map(parallel_run,fTtd)
		#print ("Done.")
		filelist = glob.glob('*.xyz')
		mol = []
		Se=0
		k=1.3806504e-23
		Na = 6.02214179e+23 # Avogadro's number
		R = k * Na

		for i in filelist:
			E=''
			f = open(i, 'r')
			s = f.readline()
			s = f.readline()
			d = str.split(s)
			E = float(d[-1])
			f.close()
			f = open(i[0:-4]+'.td', 'r')
			H='NaN'
			S='NaN'
			G='NaN'
			for line in f:
				if 'S total' in line:
					d = str.split(line)
					S = float(d[2])
				elif 'Thermal correction to Enthalpy' in line:
					d = str.split(line)
					H = float(d[5])
					H = H + E
				elif 'Thermal correction to Gibbs Free Energy' in line:
					d = str.split(line)
					G = float(d[7])
					G = G + E
			mol.append([i,E,S,H,G])
			f.close()

		ind=4 # dG sorting
		mol.sort(key=lambda x: x[ind])
		mol_copy=mol.copy()

		# get sum

		p=0
		plnp=0
		E0=mol[0][ind]
		Eavg=0
		Erelavg=0
		Savg=0
		Havg=0
		Gavg=0
		Hcorravg=0
		Gcorravg=0

		for j in range(len(mol)):
			Erel=(mol[j][ind]-E0)*627.51
			Se = Se + e**(-1*Erel/((R/4184)*float(m))) # m is T in Temp[]
			mol[j].append(Erel)
		for j in range(len(mol)):
			#print (e**(-1*mol[j][-1]/((R/4184)*float(Temp))))
			pi=e**(-1*mol[j][-1]/((R/4184)*float(m))) /Se
			Eavg = Eavg + pi*mol[j][1]
			Erelavg = Erelavg + pi*(mol[j][1]-mol[0][1])
			Havg = Havg + pi*mol[j][3]
			Gavg = Gavg + pi*mol[j][4]
			Hcorravg = Hcorravg + pi*(mol[j][3]-mol[j][1])
			Gcorravg = Gcorravg + pi*(mol[j][4]-mol[j][1])
			mol[j].append(pi)
			p=p+pi
			plnp = plnp + pi*log(pi)
			Savg=Savg + pi*mol[j][2]
	
		#print (Se)
		#print(p)
		Sconf = -1*(R/4.184)*plnp

#		print('Most stable: ', mol[0][0], " p = ", round(mol[0][-1],3))
		#print ('E = ', mol[0][1])
		#print ('S = ', mol[0][2])
		#print ('H = ', mol[0][3])
		#print ('G = ', mol[0][4])
		#print ('Hcorr = ', mol[0][3]-mol[0][1])
		#print ('Gcorr = ', mol[0][4]-mol[0][1])
		#print()
#		print ('Ensemble ('+m+'): ', sys.argv[1], '# conf: ',len(mol))
		#print('Total number of conformers: ',len(mol))
		#print ('Eavg = ', Eavg)
		#print ('Erelavg = ', Erelavg)
		#print ('Savg = ', Savg)
#		print ('bSrrho (akin CREST) = ', Savg-mol[0][2])
#		print ('Sconf (akin CREST) = ', Sconf)
		#print ('Stot = ', Savg + Sconf)
#		print ('Stot (akin CREST) = ', Savg-mol[0][2] + Sconf)

		#print ('Havg = ', Havg)
		#print ('Gavg = ', Gavg)
		#print ('Gconf = ', -1*float(Temp)*Sconf/(1000*627.51))
		#print ('Gtot = ', Gavg+-1*float(Temp)*Sconf/(1000*627.51))

		#print ('Hcorravg = ', Hcorravg)
		#print ('Gcorravg = ', Gcorravg)
		#print ('Gcorravgtot = ', Gcorravg+-1*float(Temp)*Sconf/(1000*627.51))
#		print ('H(T)-H(0) (akin CREST) = ', Erelavg+Hcorravg-(mol[0][3]-mol[0][1]))
		#print ('Hcorravg (+Erelavg) = ', Erelavg+Hcorravg)
		#print ('Gcorravg (+Erelavg) = ', Erelavg+Gcorravg)
		#print ('Gcorravgtot (+Erelavg+Sconf)= ', Erelavg+Gcorravg+-1*float(Temp)*Sconf/(1000*627.51))
		
		# put everythin in the file
		# m - temp, n - model, m[0][0] - most stable conf, round(mol[0][-1],3) - p
		# len(mol) Nconf, mol[0][2] - S of the most stable, Savg-mol[0][2] - difference Boltzmann av. S and S most stable
		# Sconf - informational entropy, 
		tmp = [m, [n, mol[0][0], round(mol[0][-1],3), len(mol), round(mol[0][2],2), round(Savg-mol[0][2],2), round(Sconf,2), round(mol[0][2]+(Savg-mol[0][2])+Sconf,2)]]
		# m - temp, n - model, m[0][0] - most stable conf, round(mol[0][-1],3) - p
		# len(mol) Nconf, (mol[0][3]-mol[0][1])  - Hcorr of the most stable, Erelavg+Hcorravg-(mol[0][3]-mol[0][1]) - difference 					Boltzmann av. Hcorr and Hcorr most stable, total Hcorr
		tmp11 = [m, [n, mol[0][0], round(mol[0][-1],3), len(mol), round((mol[0][3]-mol[0][1]),5), round(Erelavg+Hcorravg-(mol[0][3]-mol[0][1]),5), round(Erelavg+Hcorravg-(mol[0][3]-mol[0][1])+(mol[0][3]-mol[0][1]),5)]]
#		print(tmp)
		ALL_TEMP.append(tmp)
		ALL_TEMP_H.append(tmp11)
		tmp0.append(round(mol[0][2]+(Savg-mol[0][2])+Sconf,2))
	ALL_TEMP_SIM.append(tmp0)
#print (ALL_TEMP)
#print()
#print (ALL_TEMP_SIM)

# detailed printing 
f = open("SI_S.txt", 'w')
for i in ALL_TEMP:
	f.write('%4.2f %12s %20s %5.2f %5i %6.2f %6.2f %6.2f %6.2f\n' % (round(float(i[0]),2), i[1][0], i[1][1], i[1][2], i[1][3], i[1][4], i[1][5], i[1][6], i[1][7]))

#	f.write(i[0]+';')
#	for j in i[1]:
#		f.write(str(j)+';')
#	f.write('\n')
f.close()

f = open("SI_H.txt", 'w')
for i in ALL_TEMP_H:
	f.write('%4.2f %12s %20s %5.2f %5i %6.5f %6.5f %6.5f \n' % (round(float(i[0]),2), i[1][0], i[1][1], i[1][2], i[1][3], i[1][4], i[1][5], i[1][6]))

#	f.write(i[0]+';')
#	for j in i[1]:
#		f.write(str(j)+';')
#	f.write('\n')
f.close()


# print data for Excel
f = open('Excel.txt', 'w')
for i in ALL_TEMP_SIM:
	for j in i:
		f.write(str(j)+';')
	f.write('\n')
f.close()		
