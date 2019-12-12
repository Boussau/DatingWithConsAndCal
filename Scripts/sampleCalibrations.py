import sys
import random

file=sys.argv[1]
out=sys.argv[2]
num = int(sys.argv[3])

try:
    f=open(file, 'r')
except IOError:
    print ("Unknown file: "+file)
    sys.exit()

calibrations = list()
newcalib = False
current = ""
for l in f:
    if "####### Internal node constraints #######" in l:
        pass
    elif "### we create a deterministic node for the age of the MRCA of each clade with an extinct species" in l:
        pass
    elif "### the age of the node is a function of the fossil age" in l:
        newcalib=True
        if current != "":
            calibrations.append(current)
            current = l
    else:
        current = current +l
if current != "":
    calibrations.append(current)

f.close()

#for c in calibrations:
#    print(c)

sels = random.sample(calibrations, num)


try:
    fout=open(out, 'w')
except IOError:
    print ("Unknown file: "+out)
    sys.exit()

i = 0
for l in sels:
    fout.write(l+"\n")

fout.close()
