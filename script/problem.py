#import gurobipy
from difflib import SequenceMatcher


# Find common substrings
# - regex: 
# 'Tel_Reg_Exp_5' : "(A{0,4}(C{4}A{4})+C{0,4})|(C{0,4}(A{4}C{4})+A{0,4})|(A{1,4}C{4}A{1,4})|(C{1,4}A{4}C{1,4})",
# 'Tel_Reg_Exp_3' : "(T{0,4}(G{4}T{4})+G{0,4})|(G{0,4}(T{4}G{4})+T{0,4})|(T{1,4}G{4}T{1,4})|(G{1,4}T{4}G{1,4})"
# - find()
# - libdiff
# https://en.wikipedia.org/wiki/N-gram
# http://www3.cs.stonybrook.edu/~algorith/files/longest-common-substring.shtml
# http://www.aaai.org/Papers/IJCAI/2007/IJCAI07-101.pdf



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
