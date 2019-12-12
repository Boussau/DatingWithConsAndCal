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

lines = list()
for l in f:
    lines.append( l.strip() )

f.close()

sels = random.sample(lines, num)


try:
    fout=open(out, 'w')
except IOError:
    print ("Unknown file: "+out)
    sys.exit()

i = 0
for l in sels:
    fout.write(l+"\n")

fout.close()
