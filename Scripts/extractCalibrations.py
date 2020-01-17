import sys
from ete3 import faces, Tree, TreeStyle, NodeStyle, CircleFace, RectFace
from collections import OrderedDict, deque
from sortedcontainers import SortedSet
import numpy.random as nprd
import random

exec (open("/home/boussau/Data/TransferRelated/datingWithTransfers/ReplicatedAnalysis_112019/Scripts/usefulFunctions.py").read ())


def layout(n):
    nstyle_bg = NodeStyle()
    nstyle_bg["size"] = 0
    n.set_style(nstyle_bg)
    if n.calibration_red:
        n.set_style(nstyle_bg)
        C = CircleFace(radius=8, color="red", style="sphere")
#        C = RectFace(width=20, height=5, fgcolor="red", bgcolor="red")
        # Let's make the sphere transparent
        C.opacity = 0.7
        # place as a float face over the tree
        faces.add_face_to_node(C, n, 0, position="float")
#        faces.add_face_to_node(C, n, 0, position="branch-right")
    if n.calibration_blue:
        n.set_style(nstyle_bg)
        C = CircleFace(radius=8, color="blue", style="sphere")
#        C = RectFace(width=20, height=5, fgcolor="red", bgcolor="red")
        # Let's make the sphere transparent
        C.opacity = 0.7
        # place as a float face over the tree
        faces.add_face_to_node(C, n, 0, position="float")


def computeAvgCalibrationAge(calibrated_nodes, id2Height):
    avg = 0.0
    for n in calibrated_nodes:
        avg = avg + id2Height[n]
    return (avg/(len(calibrated_nodes)))


def uniformWeights(d):
    weight = 1.0/float(len(d))
    weights=[weight]*len(d_ascending)
    return weights

def biasedWeights(d):
    weights = list(range(1, len(d)+1))
    sum_weights = sum(weights)
    for i in range (len(weights)):
        weights[i] = weights[i]/float(sum_weights)
    return weights


def outputCalibrations(clades, ages, fout2, fout, sentence):
    index = 0
    fout2.write("\n############"+ sentence)
    fout2.write("####### Internal node calibrations #######\n")
    fout.write("######### Clade file ##########")
    for c in clades:
        name_clade = "clade_"+str(index)
        fout.write(name_clade+" = clade(")
        start=True
        for tax in c:
            if start:
                fout.write("\""+tax+"\"")
                start=False
            else:
                fout.write(",\""+tax+"\"")
        fout.write(")\n")
        fout2.write("### we create a deterministic node for the age of the MRCA of each clade with a fossil calibration\n")
        fout2.write("tmrca_"+name_clade+" := tmrca(psi,"+name_clade+")\n")
        fout2.write("age_fossil_"+name_clade+" <- tmrca(psi,"+name_clade+")\n")
        fout2.write("width_age_prior_"+name_clade+" <- tmrca_" + name_clade + " / 5  # By default we decide that the width of the calibration interval is fossil_age/5\n")
        fout2.write("mean_age_prior_"+name_clade+" <- tmrca_" + name_clade + "\n")
        fout2.write("obs_age_"+name_clade+" ~ dnSoftBoundUniformNormal(min=age_fossil_"+name_clade+" - width_age_prior_"+name_clade+", max=age_fossil_"+name_clade+" + width_age_prior_"+name_clade+", sd=2.5, p=0.95\n")
        fout2.write("obs_age_"+name_clade+".clamp( mean_age_prior_"+name_clade +")\n" )
        index = index+1


##########################################
############## The main function #########
##########################################
if __name__ == "__main__":
    file = sys.argv[1]
    calibration_file = file.split('.')[0]+'_calibrations.Rev'
    num_cal = int(sys.argv[2])
    balanced = sys.argv[3] # Do we want to sample calibrations in a balanced or unbalanced way
    old = sys.argv[4] # Do we want to sample old calibrations rather than recent ones.
    clade_file = file.split('.')[0]+'_clades.Rev'

    t = readTreeFromFile(file)

    index = 0
    for node in t.traverse("postorder"):
        if not node.is_leaf():
            node.name=str(index)
            node.support=str(index)
            index += 1

    id2Height = dict()
    nodeId2LeafListRef = dict()
    leafList2NodeIdRef = dict()
    idToDescendants = dict()
    # Now we want to get the calibrations according to the options that have been user-input.

    t_begin = Tree()

    # Balanced or not?
    if ('y' in balanced):
        # Getting calibrations from both sides of the root
        t_begin = t
    else:
        # Getting calibrations only from one side
        choices = [0,1]
        choice  = random.choice(choices)
        print("Choosing calibrations from subtree: ", choice)
        t_begin = t.get_children()[choice]
    print("Number of nodes in sampled subtree: ", len(t_begin.get_descendants()))

    id2Height = getInternalNodeHeights( t_begin )
    nodeId2LeafListRef, leafList2NodeIdRef, idToDescendants = getNameToLeavesAndIdToDescendantIdsLink( t_begin )
    # Let's order the nodes according to their heights:
    d_ascending = OrderedDict(sorted(id2Height.items(), key=lambda kv: kv[1]))

    calibrated_nodes_red = list()
    calibrated_nodes_blue = list()

    if ('y' in old):
        print("\tFavouring ancient calibrations\n")
        weights = biasedWeights(d_ascending)
        print("\t\tWeights: ", weights)
        calibrated_nodes_red = nprd.choice(a=list(d_ascending.keys()),
                           size=num_cal,
                           replace=False,
                           p=weights)
    elif old == "both":
        print("\tChoosing both ancient and random calibrations\n")
        weights = biasedWeights(d_ascending)
        # print("\t\tWeights: ", weights)
        calibrated_nodes_red = nprd.choice(a=list(d_ascending.keys()),
                           size=num_cal,
                           replace=False,
                           p=weights)
        avg_age_red = computeAvgCalibrationAge(calibrated_nodes_red, id2Height)
        print("Average age of ancient calibrations: ", avg_age_red)
        weights = uniformWeights(d_ascending)
        calibrated_nodes_blue = nprd.choice(a=list(d_ascending.keys()),
                           size=num_cal,
                           replace=False,
                           p=weights)
        avg_age_blue = computeAvgCalibrationAge(calibrated_nodes_blue, id2Height)
        print("Average age of random calibrations: ", avg_age_blue)
    else:
        print("\tChoosing random calibrations\n")
        weights = uniformWeights(d_ascending)
        #print("\t\tWeights: ", weights)
        calibrated_nodes_blue = nprd.choice(a=list(d_ascending.keys()),
                           size=num_cal,
                           replace=False,
                           p=weights)

    ###############################
    #### OUTPUTING THE CALIBRATIONS
    ###############################
    try:
        fout=open(calibration_file, 'w')
    except IOError:
        print ("Unknown file: " + calibration_file)
        sys.exit()

    try:
        fout2=open(clade_file, 'w')
    except IOError:
        print ("Unknown file: "+ clade_file)
        sys.exit()


    clades_red = list()
    ages_red =list()
    clades_blue = list()
    ages_blue = list()

    print(list(nodeId2LeafListRef.keys()))

    for n in calibrated_nodes_red:
        clades_red.append(nodeId2LeafListRef[float(n)])
        ages_red.append(id2Height[n])

    for n in calibrated_nodes_blue:
        clades_blue.append(nodeId2LeafListRef[float(n)])
        ages_blue.append(id2Height[n])

    print(len(clades_red))
    print(len(clades_blue))


    outputCalibrations(clades_red, ages_red, fout, fout2, "Old calibrations overrepresented\n")
    outputCalibrations(clades_blue, ages_blue, fout, fout2, "Random calibrations\n")


    ################
    #### PLOTTING
    ################
    for node in t.traverse("postorder"):
        if node.name in calibrated_nodes_red:
            node.calibration_red = True
        else:
            node.calibration_red = False
        if node.name in calibrated_nodes_blue:
            node.calibration_blue = True
        else:
            node.calibration_blue = False

    # Create an empty TreeStyle
    ts = TreeStyle()

    # Set our custom layout function
    ts.layout_fn = layout
    ts.min_leaf_separation= 0
    ts.scale = 200
    t.render("mytree.pdf", w=2560, units="px",tree_style=ts)

    # print(calibrated_nodes_red)
    # print(calibrated_nodes_blue)

    exit(1)
