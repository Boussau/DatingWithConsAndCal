import sys
from ete3 import Tree, TreeStyle, NodeStyle
from collections import OrderedDict, deque
from sortedcontainers import SortedSet

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



def getMRCA(t, species_list):
    nodes = list()
    for i in range(len(species_list)):
        #print(type(t.search_nodes(name=species_list[i])))
        nodes.append(t.search_nodes(name=species_list[i])[0])
    common =  t.get_common_ancestor(nodes)
    subtree = common.detach()
    return(subtree)


def getNameToLeavesAndIdToDescendantIdsLink( t ):
    node2leaves = t.get_cached_content()
    nodeId2LeafList = dict()
    leafList2NodeId = dict()
    for k in node2leaves.keys():
        if len(node2leaves[k]) == 1: #leaf node
            pass
        else:
            nodelist = list()
            for n in node2leaves[k]:
                nodelist.append( n.name )
            nodelist.sort()
            nodeId2LeafList[k.support] = nodelist
            leafList2NodeId[tuple(nodelist)] = int(k.support) # Need to transform the mutable list into an immutable tuple
    # Now we are going to get the list of descendant nodes for a given node
    nodeIdToDescendantIds = dict()
    for k,v in node2leaves.items():
        if (not k.is_leaf()):
            tCopy = t.copy()
            names = list()
            for i in v:
                names.append(i.name)
            subtree = getMRCA(tCopy, names)
            listOfIds = list()
            for node in subtree.traverse("postorder"):
                if not node.is_leaf() and node.name!=k.name:
                    listOfIds.append(node.name)
            nodeIdToDescendantIds[k.name] = listOfIds
    return nodeId2LeafList, leafList2NodeId, nodeIdToDescendantIds



def getInternalNodeHeights( t ):
    node2Height = dict()
    id2Height = dict()
    root = t.get_tree_root()
    farthest, totalHeight = root.get_farthest_node()
    for node in t.traverse("postorder"):
        if node not in node2Height :
            dist = root.get_distance(node.name)
            node2Height[node] = totalHeight-dist
            if not node.is_leaf():
                id2Height[node.name] = totalHeight-dist
        if node.up:
            if node.up.name =='':
                leaves = node.up.get_leaves()
                name=""
                for l in leaves:
                    name += l.name
                node.up.name=name
            node2Height[node.up] = node2Height[node] + node.dist
            id2Height[str(node.up.name)] = node2Height[node] + node.dist
      # print node.name + " : " + str(node2Height[node])
    #return node2Height,id2Height
    return id2Height


def getNodeHeights( t ):
    node2Height = dict()
    id2Height = dict()
    root = t.get_tree_root()
    farthest, totalHeight = root.get_farthest_node()
    for node in t.traverse("postorder"):
        if node not in node2Height:
            dist = root.get_distance(node.name)
            node2Height[node] = totalHeight-dist
            id2Height[node.name] = totalHeight-dist
        if node.up:
            if node.up.name =='':
                leaves = node.up.get_leaves()
                name=""
                for l in leaves:
                    name += l.name
                node.up.name=name
            node2Height[node.up] = node2Height[node] + node.dist
            id2Height[str(node.up.name)] = node2Height[node] + node.dist
      # print node.name + " : " + str(node2Height[node])
    #return node2Height,id2Height
    return id2Height


def getLeftRightTips(node):
    if node.is_leaf():
        print("Error: leaf node in getLeftRightTips")
        exit(-1)
    else:
        l = node.children[0].get_leaves()[0].name
        r = node.children[1].get_leaves()[0].name
    return l,r
