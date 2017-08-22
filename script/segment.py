# Usage: python3 preprocess.py

def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result

print(lcs('ciao', 'c1a2o'))

## Initial dynamic programming version of 'segment'
print("Initializing")
segM = [[[0 for i in range(0, 50)] for i in range(0, 50)] for i in range(0,50)]


def segment(lenght, parts, offset=0):
	"""
	Compute the list of all the possibile segmentations (using all the given
	parts) of a string with the specified lenght
	Every segmentation is a list of segments
	Every segment is an array containing the start and end indexes
	"""
	
	segmentations = []
	# Offset is used to keep the index values relative to the original string
	# that caused the recursive call
	if (segM[lenght][parts][offset] != 0):
		return segM[lenght][parts][offset]
	# TODO
	#elif (segM[lenght][parts][0] != 0)
		#offset, save and return it
	else:
		if (parts > lenght):
			raise ValueError("Can't divide in more parts than the total lenght")
		if parts == 1:
			segM[lenght][parts][offset] = [[[0+offset, lenght+offset]]]
			return [[[0+offset, lenght+offset]]]
		if parts == 2:
			for i in range(1, lenght):
				segmentations.append([[0+offset, i+offset], [i+offset,lenght+
					offset]])
			segM[lenght][parts][offset] = segmentations
			return segmentations
		if parts == lenght:
			segmentations.append([[0+offset,1+offset]])
			for i in range(1, lenght):
				segmentations[0].append([i+offset,i+1+offset])
			segM[lenght][parts][offset] = segmentations
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
		segM[lenght][parts][offset] = segmentations
		return segmentations

def segmentString(string, segmentation, cut=" - "):
	"""
	Given a string and a compatible segmentation, compute the segmented
	string, using the specified character to represent the cuts.
	"""
	result = ""
	for i in range(0, len(segmentation)):
		result += string[segmentation[i][0]:segmentation[i][1]]
		if i != len(segmentation)-1:
			result += cut
	return result

# Print every possibile segmentation of a string
# (trying every number of parts)

string = "HELLOWORLDFADFASDFASD"

c = 0
for j in range(1, len(string)+1):
	s = segment(len(string), j, 0)
	for i, element in enumerate(s):
		print("SEGMENTATION "+ str(c) + "( " + str(j) + " parts:" + str(i) +
			") :"+ str(s[i]))
		print(segmentString(string, s[i]))
		c+=1