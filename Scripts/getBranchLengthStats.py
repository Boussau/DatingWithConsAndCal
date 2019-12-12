import pandas as pd
import sys
from ete3 import Tree, TreeStyle, NodeStyle

file=sys.argv[1]



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

blAfter = list()

for node in t.traverse("postorder"):
        blAfter.append(node.dist)

blAfterDF = pd.DataFrame (blAfter, columns=["bls"])
#print(blBeforeDF.describe())
print ("\t\t File " + file + " : ")
print(blAfterDF.describe())
print ("##########################")
print ("##########################\n")
