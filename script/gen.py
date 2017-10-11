#!/usr/bin/python

### Imports, support classes and functions
from __future__ import division
from __future__ import print_function
import random 
import json
from random import shuffle
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

mic = ""
mac = ""

numNotation = {1: 'A', 2: 'C', 3: 'G', 4: 'T'}

def inverted_char(inverted, char):
	if (inverted):
		return char
	else:
		return ""
## Generator Parameters
# MIC length
micl = 60
# MDS Quantity
MDSn = random.randint(3,5)
# Rate of Inversion: 1 will give 10% of chance to any MDS 
#  to be inverted in the MAC, 10 will make every MDS inverted
inverseRate = 0
# overlapQuantity

# Generate MIC
i = 0
while (i<micl):
	c = random.randint(1,4)
	mic = mic + numNotation[c]
	i+=1

MDSin = 0
m = 0

print("Generated instance:\n")
print("MDS\tStart\tEnd")
end = 0
MDS = [{}] * MDSn

while (m < MDSn):
	inverted = ""
	# 2,5 ~ 10% micl
	space = random.randint(2, 5)
	# 10 ~ 20% micl
	length = random.randint(5, 10)
	inverse = random.randint(0, 10-inverseRate)
	if (inverse == 0 & inverseRate != 0):
		inverted_flag = 1
	else:
		inverted_flag = 0
	start = end + space
	end = start + length
	MDS[m] = { 'start': start, 'end': end, 'inverted': inverted_flag}
	m+=1

MDS_o = MDS
shuffle(MDS)
m = 0

while m < MDSn :
	print(str(m)+inverted_char(MDS[m]["inverted"], "*")+"\t"+str(MDS[m]["start"])+"\t"+str(MDS[m]["end"])+"\t")
	m+=1

print("\nP\tStart1\tEnd1\tStart2\tEnd2")

m = 1
P = [{}] * MDSn

while m < MDSn :
	length = int(((MDS[m-1]["end"]-MDS[m-1]["start"])/100)*40)
	P[m] = { 'start1' : (MDS[m-1]["end"] - length),
			 'end1': MDS[m-1]["end"],
			 'start2': MDS[m]["start"],
			 'end2': MDS[m]["start"] + length
			}
	print(str(m)+"\t"+str(P[m]["start1"])+"\t"+str(P[m]["end1"])+"\t"+str(P[m]["start2"])+"\t"+str(P[m]["end2"]))
	# l = 30% of MDS m-1 lenght
	m+=1

print()

# Build MIC
## Note: END is NOT included
mic = "-" * 60
p_mic = " " * 60
m = 0
while m < MDSn :
	i = 0
	string = ""
	length = MDS[m]["end"] - MDS[m]["start"]
	while i < length:
		c = random.randint(1,4)
		string += numNotation[c]
		i+=1
	mic = mic[:(MDS[m]["start"])] + string + mic[(MDS[m]["end"]):]
	m += 1

m = 1
while m < MDSn :
	i = 0
	string = ""
	length = P[m]["end1"] - P[m]["start1"]
	while i < length:
		c = random.randint(1,4)
		string += numNotation[c]
		i+=1
	if MDS[m-1]["inverted"]:
		string2 = reverse_complement(string)
	else:
		string2 = string

	if MDS[m]["inverted"]:
		string1 = reverse_complement(string)
	else:
		string1 = string

	mic = mic[:(P[m]["start1"])] + string1 + mic[(P[m]["end1"]):]
	p_mic = p_mic[:(P[m]["start1"])] + "^"*length + p_mic[(P[m]["end1"]):]
	mic = mic[:(P[m]["start2"])] + string2 + mic[(P[m]["end2"]):]
	p_mic = p_mic[:(P[m]["start2"])] + "^"*length + p_mic[(P[m]["end2"]):]
	m += 1

print("MIC\t"+mic)
print("\t"+p_mic)

# Build MAC
m = 0
while m < MDSn:
	string = ""
	# Overlap sections are copied only the second time they appear
	if m == (MDSn - 1):
		string = mic[MDS[m]["start"]:MDS[m]["end"]]
	else:
		string = mic[MDS[m]["start"]:(MDS[m]["end"]-(P[m+1]["end1"] - P[m+1]["start1"]))]
	mac += string
	m += 1

print("MAC\t"+mac)

print(json.dumps(MDS), json.dumps(P))