#!/usr/bin/python3
import numpy

# Dummy Input (no overlapped sections/pointers)
#      I1 M1    I2  M2    I2
MIC = "ACCCCAAAAACTGCCCGTATAG"
MAC = "CCAAAACCCGTA"

print("Init")
Eq = numpy.zeros((len(MIC),len(MIC),len(MAC),len(MAC)))

print("Populating Eq")
for i in range(0, len(MIC)):
	for j in range(i, len(MIC)):
		for h in range(0, len(MAC)):
			for l in range(h, len(MAC)):
				if (MIC[i:j] and MAC[h:l] and (MIC[i:j] == MAC[h:l])):
					Eq[i][j][h][l] = 1
					print("matched",i,j,h,l)
