#!/usr/bin/python
import numpy
import random
import __future__

def reverse_complement(dna):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([complement[base] for base in dna[::-1]])

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

print("Reading MAC")
MAC = ''
with open('oxytri_mac.fna') as f:
    for line in f:
        if line[0] != '>':
            MAC = MAC + line.rstrip()
print("MAC length:",len(MAC))

print("Reading MIC")
MIC = ''
with open('oxytri_mic_cut.fna') as f:
    for line in f:
        if line[0] != '>':
            MIC = MIC + line.rstrip()
print("MIC length:",len(MIC))


Eq = sparray((len(MIC),len(MIC),len(MAC),len(MAC)))
cwc = sparray((len(MIC),len(MIC),len(MAC),len(MAC)))

MACmap = numpy.zeros((len(MAC), 5))
MICmap = numpy.zeros((len(MIC), 5))

MAC = MAC[0:1000]
MIC = MIC[0:1000]
matches = 0

# Naive Method
print("Populating Eq")
for i in range(4, len(MIC)):
    print(i)
    for a in range (0, len(MIC)-i):
        for b in range(0, len(MAC)-i):
            if (MIC[a:a+i] == MAC[b:b+i]):
                matches = matches+1
                print("matched ",a,a+i,b, b+i,"len",i,MIC[a:a+i],MAC[b:b+i])

print(matches, "matches")


print("Populating cwc")

numNotation = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

print("Populating MIC String")
for i in range(0, len(MIC)):
	MICmap[i][numNotation[MIC[i]]] = 1

print("Populating MAC String")
for i in range(0, len(MAC)):
	MACmap[i][numNotation[MAC[i]]] = 1
