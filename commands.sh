pick up one larger tree with ~100 leaves. Then consider situations where:
calibrations are placed in an unbalanced way
calibrations are placed in a balanced way
(edited)
Then we place constraints. Constraints can be informative or not. They are informative if they provide node order information between nodes that have similar ages and are not in an ancestor-descendant relationship. We have not really decided yet if we want to pay attention to the informativeness of a constraint.
In the next few days, Gergely is going to get the tree with 102 sp from Betts et al. he is going to extract speciation times from that tree, and simulate a new tree with a random topology but keeping those node ages. That's a good way to simulate many trees ; we will choose one of them for our experiments.
I will write a script to build calibrations from a given tree. This script will be able to produce sets of k calibrations, either balanced or unbalanced.
Hopefully in a few days we can look at trees and sets of calibrations. Once we're happy with those, we move on to putting constraints in the simulations.

#### Test tree with 102 leaves
# Simulating the Birth-death tree
  Rscript Scripts/simulateTreeWith102Leaves.R
  mkdir SimulatedTrees
  mv *.dnd SimulatedTrees
  mkdir SimulatedTreesPDF
  mv *.pdf SimulatedTreesPDF

# our tree of interest is SimulatedTrees/extantTree.dnd

# Rescaling the trees
for i in SimulatedTrees/extantTree*.dnd ; do python Scripts/rescaleTree.py $i 0.3 ; done > statsOnRescaledTrees.txt

# Introducing deviations from the clock
for i in SimulatedTrees/extantTree*_rescaled.dnd ; do python Scripts/alterBranchLengths.py $i 0.03 0.1 1.0 0.2 0.01 ${i/.dnd}_altered.dnd n ; done

# unrooting the tree, because revbayes does not like rooted branch length trees
for i in SimulatedTrees/extantTree*_rescaled_altered.dnd ; do python Scripts/unrootTree.py $i ; done

# Get statistics on branch lengths of the altered and unrooted trees
for i in SimulatedTrees/extantTree*_rescaled_altered_unrooted.dnd ; do python Scripts/getBranchLengthStats.py $i ; done > statsOnRescaledAlteredTrees.txt

# Simulate alignments
mkdir Alignments
cd SimulatedTrees
for i in extantTree*_rescaled_altered_unrooted.dnd ; do echo "tree_file=\"$i\"; source (\"../Scripts/simu_HKY.Rev\");" | rb ; done
mv *.fasta ../Alignments
cd ..

# Reconstruction of branch length tree distributions using RevBayes
echo "aln_file=\"Alignments/extantTree_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb

#########################################################
# Now we are going to sample calibrations and constraints
#########################################################

# First, calibrations:
# 4 ways of sampling constraints:
- balanced (both sides of the root)
- unbalanced (one side of the root only)
- randomly (all nodes have the same probability to be picked)
- old-biased (older nodes are more likely to be picked; the weight is according to their order in the list of node ages)


# Getting old and young calibrations, on both sides:
python Scripts/extractCalibrations.py SimulatedTrees/extantTree.dnd 10 y both

# Getting old and young calibrations, on one side only:
python Scripts/extractCalibrations.py SimulatedTrees/extantTree.dnd 10 n both

# Second, constraints, by hand a priori:
# python Scripts/extractRelativeConstraints.py SimulatedTrees/extantTree.dnd



#########################################################
# Dating with branch lengths, constraints and calibrations
#########################################################

# Little test:

echo "tree_file=\"Alignments/10First.trees\"; source(\"Scripts/DatingRevScripts/computeMeanAndVarBl.Rev\");" | rb

# This gave us 10First.trees_meanBL.nex and 10First.trees_varBL.nex
# We select calibrations:
python Scripts/sampleCalibrations.py SimulatedTrees/extantTree_calibrations.Rev SimulatedTrees/extantTree_calibrations_5.Rev 5
# And we select constraints, by hands to produce file SimulatedTrees/extantTree_constraints_5.txt


#### Dating the tree:
echo "tree_file=\"SimulatedTrees/extantTree.dnd\"; calibration_file=\"SimulatedTrees/extantTree_calibrations_5.Rev\" ; constraint_file=\"SimulatedTrees/extantTree_constraints_5.txt\" ; clade_file=\"SimulatedTrees/extantTree_clades.Rev\" ; mean_tree_file=\"Alignments/10First.trees_meanBL.nex\" ; var_tree_file=\"Alignments/10First.trees_varBL.nex\" ; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb





#########################################################
#########################################################
#########################################################
#########################################################
#########################################################
### Previous plans:
#########################################################
#########################################################
#########################################################
#########################################################


# Simulating the Birth-death trees
  Rscript Scripts/simulate10Trees.R
  mkdir SimulatedTrees
  mv *.dnd SimulatedTrees
  mkdir SimulatedTreesPDF
  mv *.pdf SimulatedTreesPDF

# Rescaling the trees
for i in SimulatedTrees/extantTree*.dnd ; do python Scripts/rescaleTree.py $i 0.3 ; done > statsOnRescaledTrees.txt

# Introducing deviations from the clock
for i in SimulatedTrees/extantTree*_rescaled.dnd ; do python Scripts/alterBranchLengths.py $i 0.03 0.2 1.0 0.4 0.01 ${i/.dnd}_altered.dnd n ; done

# unrooting the tree, because revbayes does not like rooted branch length trees
for i in SimulatedTrees/extantTree*_rescaled_altered.dnd ; do python Scripts/unrootTree.py $i ; done

# Get statistics on branch lengths of the altered and unrooted trees
for i in SimulatedTrees/extantTree*_rescaled_altered_unrooted.dnd ; do python Scripts/getBranchLengthStats.py $i ; done > statsOnRescaledAlteredTrees.txt

# Simulate alignments
mkdir Alignments
cd SimulatedTrees
for i in extantTree_*_rescaled_altered_unrooted.dnd ; do echo "tree_file=\"$i\"; source (\"../Scripts/simu_HKY.Rev\");" | rb ; done
mv *.fasta ../Alignments
#for i in extantTree_*_rescaled_altered_unrooted.dnd ; do bppseqgen input.tree.file=$i output.sequence.file=../Alignments/${i/_rescaled_altered.dnd}.fa number_of_sites=1000 "rate_distribution=Gamma(n=20, alpha=0.3)" 'model=HKY85([kappa=3, theta=0.6, theta1=0.55, theta2=0.35 ])' ; done
cd ..

# Reconstruction of branch length tree distributions using RevBayes
echo "aln_file=\"Alignments/extantTree_1_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_1_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_2_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_2_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_3_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_3_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_4_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_4_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_5_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_5_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_6_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_6_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_7_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_7_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_8_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_8_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_9_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_9_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
echo "aln_file=\"Alignments/extantTree_10_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/extantTree_10_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb


# We extract from these tree distributions mean branch lengths and variances, and build trees with such branch lengths

# Now we are going to sample calibrations and constraints
for i in SimulatedTrees/extantTree_[123456789].dnd SimulatedTrees/extantTree_10.dnd ; do python Scripts/extractRelativeConstraints.py $i ; done

# Cleaning and backing up in case.
mv BUPAlignments Alignments OLDCOMMANDS SimulatedTrees SimulatedTreesPDF ExperimentsTrees30Leaves
