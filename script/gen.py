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