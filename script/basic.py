## Imports and support classes

import random 
import gurobipy
import __future__

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

## Artificially generate a basic instance of the problem (no overlap)

mic = ""
mac = ""

numNotation = {1: 'A', 2: 'C', 3: 'G', 4: 'T'}

# Generate MIC
i = 0
while (i<500):
	c = random.randint(1,4)
	mic = mic + numNotation[c]
	i+=1



MDSn = random.randint(2,10)
print(MDSn, "MDS")

m = 0
while (m < MDSn):
	startOffset = random.randint(0, int(500/MDSn))
	length = random.randint(10,50)
	print("MDS",m,"starts at",int(startOffset+(500/MDSn)*m), "and ends at", int(startOffset+(500/MDSn)*m)+length)
	mac = mac + mic[int(startOffset+(500/MDSn)*m):int(startOffset+(500/MDSn)*m)+length]
	m+=1

print("MIC  ", mic)
print("MAC  ", mac)

## Preprocess Phase

# Populate Eq
# Eq(i,j,k,l) = 1 iff MIC[i:j]=MAC[h,l]

Eq = sparray((len(mic),len(mic),len(mac),len(mac)))

matches = 0

print("Populating Eq")
for i in range(0, len(mic)-1):
	for j in range (i, len(mic)-1):
		for a in range(0, len(mac)-(j-i)):
			#print(i,j,a,a+(j-i))
			if (mic[i:j] == mac[a:a+(j-i)]):
				matches = matches+1
				if (j-i) > 20:
					print("Match with length ",j-i)

print("Populating cwc")
for i in range(0, len(mic)-1):
	for j in range (i, len(mic)-1):
		for a in range(0, len(mac)-(j-i)):
			#print(i,j,a,a+(j-i))
			if (mic[i:j] == reverse_complement(mac[a:a+(j-i)])):
				matches = matches+1
				if (j-i) > 0:
					print("Match with length ",j-i)