import sys

def get_num(ls):
	pms = [0] * 4
	for i in range(4):
		pms[i] = (ls[i].count('+'), ls[i].count('-'))
	val = max(pms[0]) * max(pms[1])
	mul = 1
	if ls[3][2] == '-':
		mul = -1
	val += mul * max(pms[2]) * max(pms[3])
	return val

def gauss(x):
    return (x+1) * x // 2


bf = open(sys.argv[1]).readlines() # open the (formatted! file)
ls = [x.strip() for x in bf[:128]] # take all characters (the value 124 is taken by looking at the source)
ls = [get_num(ls[i:i+4]) for i in range(0, len(ls), 4)] # compute all values
for i in range(1, len(ls)): # apply the gaussian subtraction
    ls[i] = ls[i] - gauss(ls[i-1])
print("".join(map(chr, ls)))
