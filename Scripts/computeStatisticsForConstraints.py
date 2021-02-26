import sys
from ete3 import Tree, TreeStyle, NodeStyle
from collections import OrderedDict, deque
from sortedcontainers import SortedSet

exec (open("/home/boussau/Work/TransferRelated/datingWithTransfers/ReplicatedAnalysis_112019/Scripts/usefulFunctions.py").read ())

##########################################
############## The main function #########
##########################################

tree_file = sys.argv[1]
constraint_file = sys.argv[2]
out_file=sys.argv[3]

# reading list of constraints
constraints = list()
with open(constraint_file, "r") as fin:
    for l in fin:
        constraints.append(l.strip())

# parsing tree file
t = readTreeFromFile(tree_file)
index = 0
for node in t.traverse("postorder"):
    if not node.is_leaf():
        node.name=str(index)
        node.support=str(index)
        index += 1

root = t.get_tree_root()

id2Height = getNodeHeights( t )

nodeId2LeafListRef, leafList2NodeIdRef, idToDescendants = getNameToLeavesAndIdToDescendantIdsLink( t )

with open(out_file, "w") as fout:
    fout.write("older_left\tolder_right\tyounger_left\tyounger_right\to_age\ty_age\tdelta_age\tdelta_nodes\tdelta_dist\tacross_the_root\tnum_leaves_older\tnum_leaves_younger\tnum_ancestors_older\tnum_ancestors_younger\n")
    for cons in constraints:
        cons_li = cons.split()
        node_o = t.get_common_ancestor(cons_li[0], cons_li[1])
        node_y = t.get_common_ancestor(cons_li[2], cons_li[3])
        o = node_o.name
        y = node_y.name
        o_age = id2Height[ o ]
        y_age = id2Height[ y ]
        delta_age = o_age - y_age
        delta_nodes = node_o.get_distance(y, topology_only=True)
        delta_dist = node_o.get_distance(y)
        ancestor = t.get_common_ancestor(o, y)
        across_the_root = ancestor.is_root()
        num_leaves_older = len(node_o.get_leaves())
        num_leaves_younger = len(node_y.get_leaves())
        num_ancestors_older = root.get_distance(o, topology_only=True)
        num_ancestors_younger = root.get_distance(y, topology_only=True)
        fout.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cons_li[0],cons_li[1],cons_li[2],cons_li[3],o_age,y_age,delta_age,delta_nodes,delta_dist,across_the_root,num_leaves_older,num_leaves_younger, num_ancestors_older, num_ancestors_younger))

