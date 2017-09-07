# FIXME compare same length only
print("Populating Eq")
for i in range(0, len(MIC)):
	for j in range(i+1, len(MIC)):
		for h in range(0, len(MAC)):
			for l in range(h+1, len(MAC)):
				if (MIC[i:j] and MAC[h:l] and (MIC[i:j] == MAC[h:l])):
					Eq[i,j,h,l] = 1
					#if (j-i > 3):
					print("matched MIC",i,j,"to MAC", h, l, " - length:",j-i)

# FIXME compare same length only
print("Populating cwc")
for i in range(0, len(MIC)):
	for j in range(i, len(MIC)):
		for h in range(0, len(MAC)):
			for l in range(h, len(MAC)):
				if (MIC[i:j] and MAC[h:l] and (MIC[i:j] == reverse_complement(MAC[h:l]))):
					cwc[i,j,h,l] = 1
					if (j-i > 1):
						print("matched MIC",i,j,"to Reverse MAC", h, l, " - length:",j-i)