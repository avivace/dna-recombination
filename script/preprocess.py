def segment(lenght, parts, offset=0):
	segmentations = []
	if (parts > lenght):
		raise ValueError("Can't divide in more parts than the total lenght")
	if parts == 1:
		return [[[0+offset, lenght+offset]]]
	if parts == 2:
		for i in range(1, lenght):
			segmentations.append([[0+offset, i+offset], [i+offset,lenght+offset]])
		return segmentations
	if parts == lenght:
		segmentations.append([[0+offset,1+offset]])
		for i in range(1, lenght):
			segmentations[0].append([i+offset,i+1+offset])
		return segmentations
	else:
		n = -1
		for i in range(1, lenght-parts+2):
			rest = segment(lenght-i, parts-1, offset+i)
			for j, element in enumerate(rest):
				segmentations.append([[0+offset, i+offset]])
				n+=1
				for k, seg in enumerate(element):
					segmentations[n].append(seg)
	return segmentations

def stringSegments(string, segmentation):
	segmentedWord = ""
	for i in range(0, len(segmentation)):
		segmentedWord += string[segmentation[i][0]:segmentation[i][1]]
		if i != len(segmentation)-1:
			segmentedWord += " "
	return segmentedWord


s = segment(7, 2, 0)

print(stringSegments("Antonio", s[0]))

for i, element in enumerate(s):
	print("SEGMENTATION "+str(i) +" :"+ str(s[i]))
	print(stringSegments("Antonio", s[i]))
