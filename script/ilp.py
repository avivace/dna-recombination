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

def rc(dna):
	complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
	return ''.join([complement[base] for base in dna[::-1]])

# Generated instance:
# 
# MDS     Start   End
# 0       3       9
# 1       21      27
# 2       30      38
# 3       40      50
# 4       13      19
# 
# P       Start1  End1    Start2  End2
# 1       7       9       21      23
# 2       25      27      30      32
# 3       35      38      40      43
# 4       46      50      13      17
# 
# MIC     ---AAATAT----TGGAGG--ATCGGT---GTAGAATT--ATTTCGTGGA----------
#                ^^    ^^^^    ^^  ^^   ^^   ^^^  ^^^   ^^^^          
# MAC     AAATATCGGTAGAATTTCGTGGAGG

mic = "---AAATAT----TGGAGG--ATCGGT---GTAGAATT--ATTTCGTGGA----------"
mac = "AAATATCGGTAGAATTTCGTGGAGG"
mac_i = rc(mac)

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
			if (mic[i:j] == mac[a:a+(j-i)]):
				Eq[i,j,a,a+(j-i)] = 1
				matches = matches+1
			if (mic[i:j] == mac_i[a:a+(j-i)]):
				cwc[i,j,a,a+(j-i)] = 1
				i_matches = i_matches+1

print("Matches: Eq:", matches,"cwc:", i_matches)

try:
	## Model
	m = Model("dnar")

	## Variables
	MDS_Mac_Start = m.addVars(11, len(mac), vtype=GRB.BINARY, name="MDS_Mac_Start")
	MDS_Mac_End = m.addVars(11, len(mac), vtype=GRB.BINARY, name="MDS_Mac_End")
	MDS_Mic_Start = m.addVars(11, len(mic), vtype=GRB.BINARY, name="MDS_Mic_Start")
	MDS_Mic_End = m.addVars(11, len(mic), vtype=GRB.BINARY, name="MDS_Mic_End")
	Cov_Mac = m.addVars(11, len(mac), vtype=GRB.BINARY, name="Cov_Mac")
	Cov_Mic = m.addVars(11, len(mic), vtype=GRB.BINARY, name="Cov_Mic")
	
	## Constraints
	# MDS substring equivalences
	#for i in range(11):
	#	print(i)
	#	m.addConstrs((MDS_Mic_Start[i,a] +
	#				  MDS_Mic_End[i,b] +
	#				  MDS_Mac_Start[i,c] +
	#				  MDS_Mac_End[i,d] <= 4 * Eq[a,b,c,d] for a in range(len(mic))
	#												  for b in range(len(mic))
	#												  for c in range(len(mac))
	#												  for d in range(len(mac))) , name="c0")
	

	# Each MDS must start at least one time
	m.addConstrs((sum(MDS_Mic_Start[i,a] for a in range(len(mic))) <= 1
										 for i in range(11)), name="c2")

	m.addConstrs((sum(MDS_Mac_Start[i,a] for a in range(len(mac))) <= 1
										 for i in range(11)), name="c2b")

	# MDSs with a start must have an end too.
	m.addConstrs((sum(MDS_Mac_End[i,a] for a in range(len(mac))) == sum(MDS_Mac_Start[i,b] for b in range(len(mac))) 
									   for i in range(11)), name="c3")

	m.addConstrs((sum(MDS_Mic_End[i,a] for a in range(len(mic))) == sum(MDS_Mic_Start[i,b] for b in range(len(mic))) 
									   for i in range(11)), name="c4")
	
	# (MIC) Coverage definition
	#m.addConstrs(((Cov_Mic[i,j] == sum(MDS_Mic_Start[i,b] for b in range(0,j)) - 
	#							  sum(MDS_Mic_End[i,e] for e in range(0,j)))
	#							  for j in range(len(mic))
	#							  for i in range(11)), name="c8")

	# Each MDS must end exactly before the following one starts
	m.addConstrs((MDS_Mac_End[i,j] == MDS_Mac_Start[i+1,j] for i in range(10)
														   for j in range(len(mac))), name="c9")

	# 100% MAC coverage
	#m.addConstrs((sum(Cov_Mac[i,j] for i in range(11)
	#							   for j in range(len(mac))) == len(mac)), name="c11")

	# end > start FIXME
	#for i in range(11):
	#	end = -1
	#	start = -1
	#	for a in range(len(mac)):
	#		if MDS_Mac_Start[i,a] == 1:
	#			start = a
	#		if MDS_Mac_End[i,a] == 1:
	#			end = a
	#	if (end != -1 & start != -1):
	#		m.addConstr(end > start, name="c5")

	# MIC Coverage
	#m.addConstrs(((sum(MDS_Mic_Start[i,l]) + 
	#			  sum(MDS_Mic_End[i,k]) for l in range(0,j+1)
	#			  						for k in range(l, len(mic))) - 
	#			  2 * Cov_Mic[i,j] == 0 for i in range(11)
	#			  					    for j in range(len(mic))),name="c6")
	
	# MAC Coverage
	#m.addConstrs((sum(MDS_Mac_Start[i,l] for l in range(0,j+1)) + 
	#			  sum(MDS_Mac_End[i,k] for k in range(l, len(mac))) - 
	#			  2 * Cov_Mac[i,j] == 0 for i in range(11)
	#			  					   for j in range(len(mac))),name="c7")

	m.setObjective((sum(MDS_Mic_Start[i,a] for a in range(0,len(mic)) for i in range(0,11))), GRB.MAXIMIZE)

	m.optimize()

	#Print solutions
	#for v in m.getVars():
	#	print('%s %g' % (v.varName, v.x))
	for i in range(11):
		for a in range(60):
			print(MDS_Mic_Start[i,a].X)
	
	print('Obj: %g' % m.objVal)

except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')