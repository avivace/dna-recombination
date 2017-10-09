#!/usr/bin/python

### Imports, support classes and functions
from __future__ import division
from __future__ import print_function
import random 
from gurobipy import *


class sparray(object):
	def __init__(self, shape, default=0, dtype=int):
		self.__default = default
		self.shape = tuple(shape)
		self.ndim = len(shape)
		self.dtype = int
		self.__data = {}

	def __setitem__(self, index, value):
		self.__data[index] = value

	def __getitem__(self, index):
		return self.__data.get(index,self.__default)

def reverse_complement(dna):
	complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
	return ''.join([complement[base] for base in dna[::-1]])

### Artificially generate a basic instance of the problem
## TODO: Add overlapping regions (pointers)

mic = ""
mac = ""

numNotation = {1: 'A', 2: 'C', 3: 'G', 4: 'T'}

# Generator Parameters
micl = 50
MDSn = random.randint(2,6)
# inverseRate
# overlapQuantity

# Generate MIC
i = 0
while (i<micl):
	c = random.randint(1,4)
	mic = mic + numNotation[c]
	i+=1

MDSin = 0
m = 0
while (m < MDSn):
	startOffset = random.randint(2, int(micl/MDSn))
	length = random.randint(1,5)
	inverse = random.randint(0,4)
	if (inverse == 4):
		mac = mac + reverse_complement(mic[int(startOffset+(micl/MDSn)*m):int(startOffset+(micl/MDSn)*m)+length])
		MDSin = MDSin + 1
	else:
		mac = mac + mic[int(startOffset+(micl/MDSn)*m):int(startOffset+(micl/MDSn)*m)+length]
	print("MDS",m,"",int(startOffset+(micl/MDSn)*m), ":", int(startOffset+(micl/MDSn)*m)+length)
	m+=1

macl = len(mac) 

print("Generated instance:")
print("MIC:",micl,"MAC:", macl,"-", MDSn, "MDSs,", MDSin, "inverted")

mac_i = reverse_complement(mac)

### Preprocess Phase

# Populate Eq
# Eq(i,j,k,l) = 1 iff MIC[i:j]=MAC[h,l]

Eq = sparray((len(mic),len(mic),len(mac),len(mac)))
cwc = sparray((len(mic),len(mic),len(mac),len(mac)))

matches = 0
i_matches = 0
print("\nPopulating Eq and cwc")
for i in range(0, len(mic)-1):
	for j in range (i, len(mic)-1):
		for a in range(0, len(mac)-(j-i)):
			#print(i,j,a,a+(j-i))
			if (mic[i:j] == mac[a:a+(j-i)]):
				Eq[i,j,a,a+(j-i)] = 1
				matches = matches+1
			if (mic[i:j] == mac_i[a:a+(j-i)]):
				cwc[i,j,a,a+(j-i)] = 1
				i_matches = i_matches+1

print("Matches: Eq:", matches,"cwc:", i_matches)


### ILP formulation

try:
	## Model
	m = Model("dnar")

	## Variables
	MDS_Mac_Start = m.addVars(11, macl, vtype=GRB.BINARY, name="MDS_Mac_Start")
	MDS_Mac_End = m.addVars(11, macl, vtype=GRB.BINARY, name="MDS_Mac_End")
	MDS_Mic_Start = m.addVars(11, micl, vtype=GRB.BINARY, name="MDS_Mic_Start")
	MDS_Mic_End = m.addVars(11, micl, vtype=GRB.BINARY, name="MDS_Mic_End")
	Cov_Mac = m.addVars(11, macl, vtype=GRB.BINARY, name="Cov_Mac")
	Cov_Mic = m.addVars(11, micl, vtype=GRB.BINARY, name="Cov_Mic")
	Inv = m.addVars(11, vtype=GRB.BINARY, name="Inv")
	# Eq
	# cwc

	## Constraints		
	
	# MDS substring equivalences
	m.addConstrs((MDS_Mic_Start[i,a] +
				  MDS_Mic_End[i,b] +
				  MDS_Mac_Start[i,c] +
				  MDS_Mac_End[i,d] <= 4 * Eq[a,b,c,d] for i in range(11)
												  for a in range(micl)
												  for b in range(micl)
												  for c in range(macl)
												  for d in range(macl)) , name="c0")
	# Reverse complement
	m.addConstrs((MDS_Mic_Start[i,a] +
				  MDS_Mic_End[i,b] +
				  MDS_Mac_Start[i,c] +
				  MDS_Mac_End[i,d] +
				  Inv[i] <= 5 * cwc[a,b,c,d] for i in range(11)
												  for a in range(micl)
												  for b in range(micl)
												  for c in range(macl)
												  for d in range(macl)), name="c1")
	
	# Each MDS must start at least one time
	m.addConstrs((sum(MDS_Mic_Start[i,a] for a in range(micl)) <= 1
										 for i in range(11)), name="c2")

	m.addConstrs((sum(MDS_Mac_Start[i,a] for a in range(macl)) <= 1
										 for i in range(11)), name="c2b")

	# MDSs with a start must have an end too.
	m.addConstrs((sum(MDS_Mac_End[i,a] for a in range(macl)) == sum(MDS_Mac_Start[i,b] for b in range(macl)) 
									   for i in range(11)), name="c3")

	m.addConstrs((sum(MDS_Mic_End[i,a] for a in range(micl)) == sum(MDS_Mic_Start[i,b] for b in range(micl)) 
									   for i in range(11)), name="c4")
	
	# (MIC) Coverage definition
	m.addConstrs(((Cov_Mic[i,j] == sum(MDS_Mic_Start[i,b] for b in range(0,j)) - 
								  sum(MDS_Mic_End[i,e] for e in range(0,j)))
								  for j in range(micl)
								  for i in range(11)), name="c8")

	# Each MDS must end exactly before the following one starts
	m.addConstrs((MDS_Mac_End[i,j] == MDS_Mac_Start[i+1,j] for i in range(10)
														   for j in range(macl)), name="c9")

	# 100% MAC coverage
	m.addConstrs((sum(Cov_Mac[i,j] for i in range(11)
								   for j in range(macl)) == macl), name="c11")

	# end > start FIXME
	#for i in range(11):
	#	end = -1
	#	start = -1
	#	for a in range(macl):
	#		if MDS_Mac_Start[i,a] == 1:
	#			start = a
	#		if MDS_Mac_End[i,a] == 1:
	#			end = a
	#	if (end != -1 & start != -1):
	#		m.addConstr(end > start, name="c5")

	# MIC Coverage
	#m.addConstrs(((sum(MDS_Mic_Start[i,l]) + 
	#			  sum(MDS_Mic_End[i,k]) for l in range(0,j+1)
	#			  						for k in range(l, micl)) - 
	#			  2 * Cov_Mic[i,j] == 0 for i in range(11)
	#			  					    for j in range(micl)),name="c6")
	
	# MAC Coverage
	#m.addConstrs((sum(MDS_Mac_Start[i,l] for l in range(0,j+1)) + 
	#			  sum(MDS_Mac_End[i,k] for k in range(l, macl)) - 
	#			  2 * Cov_Mac[i,j] == 0 for i in range(11)
	#			  					   for j in range(macl)),name="c7")

	m.setObjective((sum(MDS_Mic_Start[i,a] for a in range(0,micl) for i in range(0,11))), GRB.MINIMIZE)

	m.optimize()

	#Print solutions
	#for v in m.getVars():
	#	print('%s %g' % (v.varName, v.x))
	
	print('Obj: %g' % m.objVal)

except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')