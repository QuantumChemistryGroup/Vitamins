On the first step of conformational search with the Uniconf software, one should obtain CHELPG atomic charges from any available source (mopac, Priroda, ORCA). In this case, they were derived within the B97-3c approximation as it is implemented in the ORCA 6.0 software package by submiting the input files (*B97-3C-TZ.inp) providing corresponding output files (*B97-3C-TZ.out). 

Then the charges were extracted with the get_CHR_ORCA.py script by executing the following comand in terminal:
python3 /path/to/script/get_CHR_ORCA.py /path/to/file/m1_00_Vitamin_A-B97-3C-TZ.inp
(as an example). This procedure results in generation of the new file "m1_00_Vitamin_A-B97-3C-TZ.CHR", which contains molecular geometry and charges.

The file with rotational bonds specification needs to be created manualy. Here is the example of its content:
7    12    90   90    30
the bond between 7th and 12th atoms is being rotated from 0 to 90 degrees with 90 degrees step and +/- 30 degrees rotation allowed for every generated structer to avoid clashes (see more here: https://github.com/QuantumChemistryGroup/uniconf-bin). All selected rotatable bonds must be specified in .ROT file.

To prepare the input for the Uniconf program, one should executa the following command: 
python3 /path/to/script/input_uniconf-VIT.py /path/to/file/m1_00_Vitamin_A-B97-3C-TZ.CHR 
(as an example). Both .ROT and .CHR should be in the same folder. The resulting m1_00_Vitamin_A-B97-3C-TZ-uni.inp file contains the following informaiton:
rotatable bonds, geometry structure, atomic charges, and conformational search settings (systematic search of structures through all specified torsional rotations without clusterization, number of structure optimization steps, maximum amount of conformers to be printed).

The Uniconf program 64-bit Linux binary is available for download free of charge at https://github.com/QuantumChemistryGroup/uniconf-bin
Download the Uniconf program and run it on these input files to perform systematic conformational sampling
