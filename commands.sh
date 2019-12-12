
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
