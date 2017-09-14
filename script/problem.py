#import gurobipy
from difflib import SequenceMatcher

print("Reading MAC")
MAC = ''
with open('oxytri_mac.fna') as f:
    for line in f:
        if line[0] != '>':
            MAC = MAC + line.rstrip()
print("MAC length:",len(MAC))

print("Reading MIC")
MIC = ''
with open('oxytri_mac.fna') as f:
    for line in f:
        if line[0] != '>':
            MIC = MIC + line.rstrip()
print("MIC length:",len(MIC))

MAC = "ciaociao"
MIC = "ciaoasdfasdciao"
s = SequenceMatcher(None, MAC[0:1000], MIC[0:1000])
print(s.get_matching_blocks())

for tag, i1, i2, j1, j2 in s.get_opcodes():
	print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(
		tag, i1, i2, j1, j2, MIC[i1:i2], MAC[j1:j2]))
