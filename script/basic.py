## Imports, support classes and functions
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

## Artificially generate a basic instance of the problem
## TODO: Add overlapping regions (pointers)

print("Generated instance:")
mic = ""
mac = ""

numNotation = {1: 'A', 2: 'C', 3: 'G', 4: 'T'}

# Generate MIC
i = 0
micl = 500
while (i<micl):
	c = random.randint(1,4)
	mic = mic + numNotation[c]
	i+=1

MDSn = random.randint(2,10)
MDSin = 0
m = 0
while (m < MDSn):
	startOffset = random.randint(0, int(micl/MDSn))
	length = random.randint(10,50)
	inverse = random.randint(0,4)
	if (inverse == 4):
		mac = mac + reverse_complement(mic[int(startOffset+(micl/MDSn)*m):int(startOffset+(micl/MDSn)*m)+length])
		MDSin = MDSin + 1
	else:
		mac = mac + mic[int(startOffset+(micl/MDSn)*m):int(startOffset+(micl/MDSn)*m)+length]
	print("MDS",m,"",int(startOffset+(micl/MDSn)*m), ":", int(startOffset+(micl/MDSn)*m)+length)
	m+=1

print("MIC:",micl,"MAC:", len(mac),"-", MDSn, "MDSs,", MDSin, "inverted")

mac_i = reverse_complement(mac)

## Preprocess Phase

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

## ILP formulation

m = Model("dnar")

MDS_Mac_Start = m.addVars(vtype=GRB.BINARY, name="MDS_Mac_Start")

t = 0

for t in range(0..)