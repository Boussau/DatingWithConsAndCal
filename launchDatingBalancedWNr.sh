
#### Dating the tree without constraints, with balanced calibrations:
echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_0.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignment_WNr/alignment.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignment_WNr/alignment.fasta.trees_varBL.nex\"; handle=\"OutputDatingWNr/Cal_10_y_y_Cons_0\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb

#### Dating the tree with 1 constraint, with balanced calibrations:
echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_1.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignment_WNr/alignment.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignment_WNr/alignment.fasta.trees_varBL.nex\"; handle=\"OutputDatingWNr/Cal_10_y_y_Cons_1\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb

#### Dating the tree with 5 constraints, with balanced calibrations:
echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_5.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignment_WNr/alignment.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignment_WNr/alignment.fasta.trees_varBL.nex\"; handle=\"OutputDatingWNr/Cal_10_y_y_Cons_5\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb

#### Dating the tree with 10 constraints, with balanced calibrations:
echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_10.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignment_WNr/alignment.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignment_WNr/alignment.fasta.trees_varBL.nex\"; handle=\"OutputDatingWNr/Cal_10_y_y_Cons_10\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb

#### Dating the tree with 15 constraints, with balanced calibrations:
echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_15.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignment_WNr/alignment.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignment_WNr/alignment.fasta.trees_varBL.nex\"; handle=\"OutputDatingWNr/Cal_10_y_y_Cons_15\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb
