# Pipeline used to run the analyses presented in the paper

## Part 1


### We get the trees with empirical dates but shuffled topologies from Dominik in the folder ShuffledTrees
We rename the trees to avoid confusing these artificial trees with empirical ones
```{bash}
python Scripts/renameTips.py ShuffledTrees/shuffle.tree
```

Then I arbitrarily choose tree 2:
```{bash}
cd ShuffledTrees
head -2 shuffle_renamed.dnd | tail -1 > proposedTree.dnd
figtree proposedTree.dnd& # we got proposedTree.dnd.pdf
cd ..
```

### Now we're going to use this tree for the simulation work.
```{bash}
mkdir SimulatedTrees
cp ShuffledTrees/proposedTree.dnd SimulatedTrees/
```

Rescaling the trees:
```{bash}
for i in SimulatedTrees/proposedTree.dnd ; do python Scripts/rescaleTree.py $i 0.01 ; done > statsOnRescaledTrees.txt
```

Introducing deviations from the clock:
```{bash}
for i in SimulatedTrees/proposedTree_rescaled.dnd ; do python Scripts/alterBranchLengths.py $i 0.03 0.1 1.0 0.2 0.01 ${i/.dnd}_altered.dnd n ; done
```
(NB: We can compare the distributions of branch lengths before and after alterations by looking into statsOnRescaledTrees.txt and statsOnRescaledAlteredTrees.txt (at the end).)

Unrooting the tree, because revbayes does not like rooted branch length trees:
```{bash}
for i in SimulatedTrees/proposedTree_rescaled_altered.dnd ; do python Scripts/unrootTree.py $i ; done
```

Simulating alignments:
```{bash}
mkdir Alignments
cd SimulatedTrees
for i in proposedTree_rescaled_altered_unrooted.dnd ; do echo "tree_file=\"$i\"; source (\"../Scripts/simu_HKY_No_Gamma.Rev\");" | rb ; done
mv *.fasta ../Alignments
cd ..
```

Reconstruction of branch length tree distributions using RevBayes:
```{bash}
echo "aln_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta\"; tree_file=\"SimulatedTrees/proposedTree_rescaled_altered_unrooted.dnd\"; source(\"Scripts/mcmc_JC.Rev\");" | rb
```

Computation of mean and var branch lengths:
```{bash}
cd Alignments/
echo "tree_file=\"proposedTree_rescaled_altered_unrooted.dnd.fasta.trees\"; burnin=500 ; thinning=5 ; source(\"../Scripts/DatingRevScripts/computeMeanAndVarBl.Rev\");" | rb
# this produced proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex and proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex
cd ..
```


## Now we are going to sample calibrations and constraints

### First, calibrations.
We get 10 calibrations as in Betts et al. 2018.

Getting old-biased calibrations, on both sides (balanced):
```{bash}
python Scripts/extractCalibrations.py SimulatedTrees/proposedTree.dnd 10 y y
```

Getting old-biased calibrations, on one side only (unbalanced):
```{bash}
python Scripts/extractCalibrations.py SimulatedTrees/proposedTree.dnd 10 n y
```

### Second, we get constraints
We get constraints by hand.
The result is in several files: constraints_10.Rev  constraints_15.Rev  constraints_1.Rev  constraints_5.Rev  constraints_full.txt  constraints_informative.Rev  constraints_uninformative.Rev constraints_0.Rev


## Dating with branch lengths, constraints and calibrations

### First, the effect of the number of constraints:
```{bash}
mkdir OutputDating
```

Dating the tree with balanced calibrations and varying numbers of constraints:
```{bash}
bash balancedRuns/*.sh
```

Dating the tree with unbalanced calibrations and varying numbers of constraints:
```{bash}
bash unbalancedRuns/*.sh
```

### Testing proximal and distal constraints:
```{bash}
bash proximalDistal/*.sh
```

## Analyzing the sampled trees:

### First, analysing the effect of the number of constraints:

*Warning: The tree traces have not been added to the repo, so they need to be recreated for the next few steps to work.*

First we clean the tree traces: sometimes revbayes mixes up the writing of trees, so that the newick strings are messed up. Then, these trees cannot be read back to obtain a MAP tree.
```{bash}
for i in *.trees ; do python ../Scripts/removeIncorrectLinesFromTrace.py $i ${i/.trees}noMix.trees ; done > outputCleaningTraceFiles
```

Then we can make map trees for each file:
```{bash}
for i in *noMix.trees ; do echo "fname_stem=\"${i/.trees}\" ; source(\"../Scripts/DatingRevScripts/makeMAPTree.Rev\") ;" | rb ; done
cd ..
```
*We do provide the MAP trees.*

Analysing the dated trees:
```{bash}
./launchAnalysis.sh > resultAllTrees.txt
grep -A1 "fracInHPD" resultAllTrees.txt | grep -v "fracInHPD" | grep -v "-" > resultAllTreesExcerpt.txt
```


### Same thing for the comparison of proximal and distal constraints


```{bash}
cd OutputDatingProximalDistal
for i in *.trees ; do python ../Scripts/removeIncorrectLinesFromTrace.py $i ${i/.trees}noMix.trees ; done > outputCleaningTraceFiles
```
Then we can make map trees for each file.
```{bash}
for i in *noMix.trees ; do echo "fname_stem=\"${i/.trees}\" ; source(\"../Scripts/DatingRevScripts/makeMAPTree.Rev\") ;" | rb ; done
cd ..
```

Analysing the dated trees:
```{bash}
./launchAnalysisProximalDistal.sh > resultAllTreesInfoUninfo.txt
grep -A1 "fracInHPD" resultAllTreesInfoUninfo.txt | grep -v "fracInHPD" | grep -v "-" > resultAllTreesInfoUninfoExcerpt.txt
```

Adding the data with 0 constraint from the previous experiments
```{bash}
awk '{ if ($3==0) {print} }' resultAllTreesExcerpt.txt > result0Constraints
cat result0Constraints resultAllTreesInfoUninfoExcerpt.txt > resultAllTreesInfoUninfoExcerptWith0Constraint.txt
```

## Analyses and plots in Analysis of constraints vs calibrations.ipynb




## Validation test: when the model for simulating sequences matches the reconstruction model

We use revbayes to simulate a tree using a Birth Death process, simulate rates along the tree using an Uncorrelated Gamma model, then sequences using the Jukes Cantor model.

```{bash}
mkdir SimuAndInferUGAM
cd SimuAndInferUGAM
echo "tree_file=\"../SimulatedTrees/proposedTree.dnd\"; source(\"../Scripts/DatingRevScripts/simulateThenInferUGAM.Rev\");" | rb
```

Running the UGAMr model, with Bactrian scale moves on all the parameters of UGAMr, and MC3.

```{bash}
echo "tree_file=\"../SimulatedTrees/proposedTree.dnd\"; source(\"../Scripts/DatingRevScripts/endSimulateThenInferUGAM_InferUGAMParametersBactrianMC3.Rev\");" | rb
```

Analysis:

```{bash}
python ../Scripts/analyzeMAPTree.py simulatedTree_BD.nex simuAndinferInferUGAMrParametersBactrianMC3_BD_BD_UGAMr_BL.tree y
```

It works!
