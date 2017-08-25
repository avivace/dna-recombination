#!/usr/bin/python3
import numpy

# Dummy Input (no overlapped sections/pointers)
#      I1 M1    I2  M2    I2
MIC = "ACCCCAAAAACTGCCCGTATAG"
MAC = "CCAAAACCCGTA"

MIC = "ACCCCAAAAACTGCCCGTATAGACCCCAAAAACTGCCCGTATAGACCCCAAAAACTGCCCGTATAGACCCCAAAAACTGCCCGTATAGACCCCAAAAACTGCCCGTATAGACCCCAAAAACTGCCCGTATAG"
MAC = "CCAAAACCCGTACCAAAACCCGTACCAAAACCCGTACCAAAACCCGTACCAAAACCCGTA"

def reverse_complement(dna):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([complement[base] for base in dna[::-1]])

print("Initializing")
Eq = numpy.zeros((len(MIC),len(MIC),len(MAC),len(MAC)))
cwc = numpy.zeros((len(MIC),len(MIC),len(MAC),len(MAC)))
MACmap = numpy.zeros((len(MAC), 5))
MICmap = numpy.zeros((len(MIC), 5))

print("Populating Eq")
for i in range(0, len(MIC)):
	for j in range(i, len(MIC)):
		for h in range(0, len(MAC)):
			for l in range(h, len(MAC)):
				if (MIC[i:j] and MAC[h:l] and (MIC[i:j] == MAC[h:l])):
					Eq[i][j][h][l] = 1
					if (j-i > 3):
						print("matched MIC",i,j,"to MAC", h, l, " - length:",j-i)

print("Populating cwc")
for i in range(0, len(MIC)):
	for j in range(i, len(MIC)):
		for h in range(0, len(MAC)):
			for l in range(h, len(MAC)):
				if (MIC[i:j] and MAC[h:l] and (MIC[i:j] == reverse_complement(MAC[h:l]))):
					cwc[i][j][h][l] = 1
					if (j-i > 1):
						print("matched MIC",i,j,"to Reverse MAC", h, l, " - length:",j-i)

numNotation = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

print("Populating MIC String")
for i in range(0, len(MIC)):
	MICmap[i][numNotation[MIC[i]]] = 1

print("Populating MAC String")
for i in range(0, len(MAC)):
	MACmap[i][numNotation[MAC[i]]] = 1
