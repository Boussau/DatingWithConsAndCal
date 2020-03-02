from ete3 import Tree
import re


exec (open("/home/boussau/Data/TransferRelated/datingWithTransfers/ReplicatedAnalysis_112019/Scripts/usefulFunctions.py").read ())

def readMAPChronogramFromRBOutput (file):
    try:
        f=open(file, 'r')
    except IOError:
        print ("Unknown file: "+file)
        sys.exit()
    line = ""
    treeStrings = list()
    for l in f:
        if "tree TREE1 = [&R]" in l:
            line = l.replace("tree TREE1 = [&R]", "")
            tree = re.sub('\[&index=\d+([,\w=\d,%\.\{\}])*\]', "", line)#[&index=102,posterior=1.000000,ccp=1.000000,height_95%_HPD={0.025722,0.071446}]
            #print(tree)
            return Tree(tree)


def readAnnotatedChronogramWithoutAnnotations (l):
    line = l.replace("tree TREE1 = [&R]", "")
    line = re.sub('\[&index=\d+([,\w=\d,%\.\{\}])*\]', "", line)
    line = re.sub('\[&branch_rates=\d+([,\w=\d,%\.\{\}e-])*\]', "", line)
    return Tree(line)


def readMAPChronogramFromRBOutputAndExtract95Hpd (file):
    try:
        f=open(file, 'r')
    except IOError:
        print ("Unknown file: "+file)
        sys.exit()
    line = ""
    for l in f:
        if "tree TREE1 = [&R]" in l:
            line = l.replace("tree TREE1 = [&R]", "")
            #print("line: "+line)
            # We are going to create a tree string with node indices
            # At the same time, we'll store 95% HPD along with the node indices.
            # We'll return the tree and a map between the node indices and the 95% HPD.
#            line2 = re.sub('\[&index=(\d+)]', '', line)
            line1 = re.sub('\[&index=(\d+)\]', "[&index=\g<1>,posterior=1.000000,age_95%_HPD={0.0,0.0}]", line)
            #print("line1: "+line1)
            line2 = re.sub('([^)])\[&index=(\d+)([,\w=\d,%\.\{\}])+\]', r'\g<1>', line1)
            #print("line2: "+line2)
#            tree = re.sub('\[&index=(\d+)([,\w=\d,%\.\{\}])+\]', r'\g<1>', line2)#[&index=102,posterior=1.000000,ccp=1.000000,height_95%_HPD={0.025722,0.071446}]
            line3 = re.sub('\[&index=(\d+)([,\w=\d,%\.\{\}])+\]', r'\g<1>', line2)#[&index=102,posterior=1.000000,ccp=1.000000,height_95%_HPD={0.025722,0.071446}]
            #print("line3: "+line3)
            tree = re.sub('\[&branch_rates_range=\{\d+\.\d+e*-*\d*,\d+\.\d+e*-*\d*\},branch_rates=\d+\.\d+e*-*\d*\]', "", line3)#[&branch_rates_range={0.0022512,0.0159078},branch_rates=0.006652]
            #print("tree: "+tree)
            brackets = re.findall('\[&index=[,\w=\d,%\.\{\}]*\]', line2)
            idToHPD = dict()
            #print(brackets)
            for i in brackets:
                index = re.findall('\[&index=(\d+)', i)
                hpd = re.findall('age_95%_HPD={(\d+\.*\d*,\d+\.*\d*)}', i)
                idToHPD[index[0]] = list()
                if (len(hpd) > 0 ):
                    idToHPD[index[0]].append(float(hpd[0].split(",")[0]))
                    idToHPD[index[0]].append(float(hpd[0].split(",")[1]))
                else:
                    idToHPD[index[0]].append(0.0)
                    idToHPD[index[0]].append(0.0)
            return Tree(tree), idToHPD

### The two following functions are used to number nodes in a tree according to another tree. This is necessary to compare node ages between two trees.

def getNameToLeavesLink( t ):
    node2leaves = t.get_cached_content()
    nodeId2LeafList = dict()
    leafList2NodeId = dict()
    for k in node2leaves.keys():
        if len(node2leaves[k]) == 1: #leaf node
            #print("Leaf node " + str(node2leaves[k]))
            pass
        else:
            nodelist = list()
            for n in node2leaves[k]:
                nodelist.append( n.name )
            nodelist.sort()
            nodeId2LeafList[k.support] = nodelist
            leafList2NodeId[tuple(nodelist)] = int(k.support) # Need to transform the mutable list into an immutable tuple
    return nodeId2LeafList, leafList2NodeId


def numberNodes( treeToAnnotate ):
    #print treeToAnnotate.get_ascii(attributes=[ "name"], show_internal=False)
    node2leaves = treeToAnnotate.get_cached_content()
    i = 0
    for k in node2leaves.keys():
        if len(node2leaves[k]) == 1: #leaf node
            pass
        else:
            k.support = i
            k.name = i
            i = i + 1
    return treeToAnnotate

def renumberNodes( treeToAnnotate, leafList2NodeId ):
    #print treeToAnnotate.get_ascii(attributes=[ "name"], show_internal=False)
    node2leaves = treeToAnnotate.get_cached_content()
    for k in node2leaves.keys():
        if len(node2leaves[k]) == 1: #leaf node
            pass
        else:
            nodelist = list()
            for n in node2leaves[k]: # for all the leaves in the subtree
                nodelist.append( n.name )
            nodelist.sort()
            k.support = leafList2NodeId[tuple(nodelist)]


def renumberNodesAndUpdate95HPDAccordingly( treeToAnnotate, leafList2NodeId, idToHPD ):
    newIdToHPD = dict()
    #print treeToAnnotate.get_ascii(attributes=[ "name"], show_internal=False)
    node2leaves = treeToAnnotate.get_cached_content()
    #print("leafList2NodeId: " + str(leafList2NodeId))
    for k in node2leaves.keys():
        if len(node2leaves[k]) == 1: #leaf node
            pass
        else:
            nodelist = list()
            for n in node2leaves[k]: # for all the leaves in the subtree
                #print("n.name : "+ n.name )
                nodelist.append( n.name )
            nodelist.sort()
            #print("tuple(nodelist): "+str(tuple(nodelist)))
            newName = leafList2NodeId[tuple(nodelist)]
            newIdToHPD[newName] = idToHPD[str(int(k.support))]
            k.support = str(newName)
            k.name = str(newName)
    return(treeToAnnotate, newIdToHPD)


def getBranchLengths( t ):
    node2Bl = dict()
    id2Bl = dict()
    for node in t.traverse("postorder"):
        if node not in node2Bl:
            node2Bl[node] = node.dist
            id2Bl[node.support] = node.dist
        if node.up:
            if node.up.name =='':
                leaves = node.up.get_leaves()
                name=""
                for l in leaves:
                    name += l.name
                node.up.name=name
            node2Bl[node.up] = node.up.dist
            id2Bl[str(int(node.up.support))] = node.up.dist
      # print node.name + " : " + str(node2Height[node])
    #return node2Height,id2Height
    return id2Bl


def plotAndComputeCorrelation(x,y,namex, namey, logyn, logxn, limx=None, limy=None):
    print("Pearson correlation coefficient and p-value: "+ str(scipy.stats.pearsonr(x, y)))
    #Plotting:
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(x, y, 'bo')
    # draw diagonal line
    xy = x+y
    maxxy=max(xy)
    #print(maxxy)
    ax.plot([0, 2*maxxy], [0, 2*maxxy ], color='k', linestyle='--',  lw=2)
    plt.axis([0, 1.1*maxxy, 0, 1.1*maxxy])
    plt.xlabel(namex, fontsize=15)
    plt.ylabel(namey, fontsize=15)
#plt.legend(['data'], loc='upper left')
    if logyn:
        ax.yscale('log')
    if logxn:
        ax.xscale('log')
    if not limx == None:
        ax.xlim(limx)
    if not limy == None:
        ax.ylim(limy)
    fig.show()


def plotAndComputeSeveralCorrelations(x, y1, y2, y3, y4, namex, namey, namey1, namey2, namey3, namey4, logyn, logxn, limx=None, limy=None):
    print(namey1 + " : Pearson correlation coefficient and p-value: "+ str(scipy.stats.pearsonr(x, y1)))
    print(namey2 + " : Pearson correlation coefficient and p-value: "+ str(scipy.stats.pearsonr(x, y2)))
    print(namey3 + " : Pearson correlation coefficient and p-value: "+ str(scipy.stats.pearsonr(x, y3)))
    print(namey4 + " : Pearson correlation coefficient and p-value: "+ str(scipy.stats.pearsonr(x, y4)))

    #Plotting:
    fig, ax = plt.subplots(figsize=(20, 15))
    cl, = ax.plot(x, y1, 'bh')
    cal, = ax.plot(x, y2, 'gD')
    con, = ax.plot(x, y3, 'rv')
    calcon, = ax.plot(x, y4, 'co')

    # draw diagonal line
    xy = x+y1
    maxxy=max(xy)
    ax.plot([0, 2*maxxy], [0, 2*maxxy ], color='k', linestyle='--',  lw=2)
    plt.axis([0, 1.1*maxxy, 0, 1.1*maxxy])
    plt.xlabel(namex, fontsize=15)
    plt.ylabel(namey, fontsize=15)
    plt.legend([cl, cal, con,calcon], [namey1, namey2, namey3, namey4], loc='upper left')
    if logyn:
        ax.yscale('log')
    if logxn:
        ax.xscale('log')
    if not limx == None:
        ax.set_xlim(limx)
    if not limy == None:
        ax.set_ylim(limy)
    #fig.show()
