import sys
from ete3 import Tree, TreeStyle, NodeStyle
from collections import OrderedDict, deque
from sortedcontainers import SortedSet

exec (open("/home/boussau/Data/TransferRelated/datingWithTransfers/ReplicatedAnalysis_112019/Scripts/usefulFunctions.py").read ())

##########################################
############## The main function #########
##########################################


table_file = sys.argv[1] # file that contains constraints and related information
tree_file = sys.argv[2] # file that contains the tree
out = sys.argv[3] # output file
favour_short_node_distances = sys.argv[4]
favour_long_node_distances = sys.argv[5]
favour_balanced = sys.argv[6]
favour_unbalanced = sys.argv[7]
favour_similar_age = sys.argv[8]
favour dissimilar_age = sys.argv[9]



t = readTreeFromFile(tree_file)

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
