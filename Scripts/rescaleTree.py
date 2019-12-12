import pandas as pd
import sys
from ete3 import Tree, TreeStyle, NodeStyle

file=sys.argv[1]
scale = float(sys.argv[2])
out=file.split('.')[0]+'_rescaled.dnd'



def readTreeFromFile(file):
    try:
        f=open(file, 'r')
    except IOError:
        print ("Unknown file: "+file)
        sys.exit()

    line = ""
    for l in f:
        line += l.strip()

    f.close()
    t = Tree( line )
    return t

t = readTreeFromFile(file)

blBefore = list()
blAfter = list()

for node in t.traverse("postorder"):
        blBefore.append(node.dist)
        node.dist = node.dist*scale
        blAfter.append(node.dist)

blBeforeDF = pd.DataFrame (blBefore, columns=["blBefore"])
blAfterDF = pd.DataFrame (blAfter, columns=["blAfter"])
#print(blBeforeDF.describe())
print(blAfterDF.describe())

t.write(format=1, outfile=out)
