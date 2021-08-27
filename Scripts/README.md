# Scripts of interest to replicate the analyses presented in
# "Relative time constraints improve molecular dating"
*Szöllősi Gergely, Höhna Sebastian, Williams Tom A., Schrempf Dominik, Daubin Vincent, Boussau Bastien*


### Simulations of deviations from the clock
* The script to introduce deviations from the clock into an ultrametric tree is [alterBranchLengths.py](alterBranchLengths.py)
* The tree with altered branch lengths resulting from this script is [here](https://github.com/Boussau/DatingWithConsAndCal/blob/master/SimulatedTrees/proposedTree_rescaled_altered.dnd.pdf).

### Alignment simulation
* The script to simulate the alignment based on the tree rescaled with deviations from the clock is [simu_HKY_No_Gamma.Rev](simu_HKY_No_Gamma.Rev).

### Inference based on simulated data
* The script to infer branch length distributions under a Jukes-Cantor model is [mcmc_JC.Rev](mcmc_JC.Rev).
* The script to summarize the obtained posterior distributions of branch lengths by their mean and variance per branch is [DatingRevScripts/computeMeanAndVarBl.Rev](DatingRevScripts/computeMeanAndVarBl.Rev).
* The script that computes a posterior distribution of timetrees according to a birth-death prior on the tree topology and node ages, an uncorrelated Gamma prior on the rate of sequence evolution through time, and using the calibrations and constraints gathered in previous steps, with the Metropolis Coupled Markov Chain Monte Carlo algorithm is [DatingRevScripts/mainScript.Rev](DatingRevScripts/mainScript.Rev).
