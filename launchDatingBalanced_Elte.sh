#!/bin/bash
# RevBayes starter
#
# Usage:
# 1. place this executable where the input files are
# 2. make it executable with chmod +x revbayes_starter.sh
# 3. execute with: nohup ./revbayes_starter.sh &
#
# Logs:
# The output will be saved to XXX.jobout
# If some error happens before srun it will be outputted to $HOME/nohup.out
#
# number of tasks for a file (in same order as files)
TASKS="1"
# comma separated list of partitions
PARTITIONS="high"
# threads per instance of program needed
THREADS="1"
# expected runtime
TIME="0"
# jobname prefix
JOBNAME="balancedRuns"
#
MEMORY="1500"
#in Mb per CPU
# program to launch
PROGRAM=“bash balancedNoConstraint.sh”

#### Dating the tree without constraints, with balanced calibrations:
srun --mem-per-cpu=${MEMORY} --ntasks-per-node=4 -n ${TASKS} -c $THREADS -o ${JOBNAME}_%j.jobout -p $PARTITIONS -J ${JOBNAME}_0 --time $TIME -- $PROGRAM > ${JOBNAME}_%j_rb.out &
sleep 1



# wait for sruns to finish

#
#
# #### Dating the tree without constraints, with balanced calibrations:
# echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_0.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDating/Cal_10_y_y_Cons_0\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb
#
# #### Dating the tree with 1 constraint, with balanced calibrations:
# echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_1.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDating/Cal_10_y_y_Cons_1\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb
#
# #### Dating the tree with 5 constraints, with balanced calibrations:
# echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_5.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDating/Cal_10_y_y_Cons_5\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb
#
# #### Dating the tree with 10 constraints, with balanced calibrations:
# echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_10.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDating/Cal_10_y_y_Cons_10\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb
#
# #### Dating the tree with 15 constraints, with balanced calibrations:
# echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_15.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDating/Cal_10_y_y_Cons_15\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb
