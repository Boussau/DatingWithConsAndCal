import sys
from ete3 import Tree, TreeStyle, NodeStyle
from collections import OrderedDict, deque
from sortedcontainers import SortedSet

exec (open("/home/boussau/Data/TransferRelated/datingWithTransfers/ReplicatedAnalysis_112019/Scripts/usefulFunctions.py").read ())

##########################################
############## The main function #########
##########################################

file=sys.argv[1]
out=file.split('.')[0]+'_constraints.txt'

t = readTreeFromFile(file)

index = 0
for node in t.traverse("postorder"):
    if not node.is_leaf():
        node.name=str(index)
        node.support=str(index)
        index += 1

id2Height = getNodeHeights( t )

nodeId2LeafListRef, leafList2NodeIdRef, idToDescendants = getNameToLeavesAndIdToDescendantIdsLink( t )

# Now we want to produce all constraints based on node heights, except those that are due to the tree topology.
# And we want to avoid redundant constraints.

# Let's order the nodes according to their heights:
d_ascending = OrderedDict(sorted(id2Height.items(), key=lambda kv: kv[1]))

# print("d_ascending: ")
# print(d_ascending)

# We will use idToDescendants to fill lists of nodes not to use as constraints

idToForbidden = dict()
for k,v in idToDescendants.items():
    values = SortedSet(v)
    # print(values)
    idToForbidden[k] = values

downstreamNodes = deque()
constraints = list()
for k, v in d_ascending.items():
    # print(v)
    if v <= 0.0000001: # very small value, ==0
        print("small")
        pass
    else:
        potentialYoungers = downstreamNodes.copy()
        forbiddens = idToForbidden[k]
        # k is older than all downstream nodes
        while len(potentialYoungers) >0:
            younger = potentialYoungers.pop()
            if younger not in forbiddens:
                forbiddens = forbiddens.union(idToForbidden[younger])
                constraints.append((k,younger))
                print("Adding constraint between" + k + " and " + younger)
        downstreamNodes.append(k)
        # print("downstreamNodes.size(): "+str(len(downstreamNodes)))

# print (constraints)



try:
    fout=open(out, 'w')
except IOError:
    print ("Unknown file: "+out)
    sys.exit()


# Output constraints in a format almost directly palatable by RevBayes
fout.write("lef_older"+"\t"+"right_older"+"\t"+"left_younger"+"\t"+"right_younger"+"\t"+"older_age"+"\t"+"younger_age"+"\t"+"delta_age"+"\t"+"delta_nodes"+"\t" + "delta_dist" + "\t" + "across_the_root"+"\n")

for o,y in constraints:
    # print(o)
    # print(y)
    node_o = t.search_nodes(name=o)[0]
    node_y = t.search_nodes(name=y)[0]
    lo,ro = getLeftRightTips(node_o)
    ly,ry = getLeftRightTips(node_y)
    o_age = id2Height[ o ]
    y_age = id2Height[ y ]
    delta_age = o_age - y_age
    delta_nodes = node_o.get_distance(y, topology_only=True)
    delta_dist = node_o.get_distance(y)
    ancestor = t.get_common_ancestor(o, y)
    across_the_root = ancestor.is_root()
    fout.write(lo+"\t"+ro+"\t"+ly+"\t"+ry+"\t"+str(o_age)+"\t"+str(y_age)+"\t"+str(delta_age)+"\t"+str(delta_nodes)+"\t" + str(delta_dist) + "\t" + str(across_the_root)+"\n")

fout.close()

# print(id2Height)
# print("\n")
# print(nodeId2LeafListRef)
# print("\n")
# print(leafList2NodeIdRef)
# print("\n")
# print(idToDescendants)
# print(t.write(format=2))
