
#### Dating the tree with 5 informative constraints, with balanced calibrations:
#echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_informative.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDatingInfoUninfo/Cal_10_y_y_Cons_info\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb


#### Dating the tree with 5 informative constraints, with unbalanced calibrations:
echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_n_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_informative.Rev\" ; clade_file=\"Calibrations_10_n_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDatingInfoUninfo/Cal_10_n_y_Cons_info\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb


#### Dating the tree with 5 uninformative constraints, with balanced calibrations:
#echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_y_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_uninformative.Rev\" ; clade_file=\"Calibrations_10_y_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDatingInfoUninfo/Cal_10_y_y_Cons_info\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb


#### Dating the tree with 5 uninformative constraints, with unbalanced calibrations:
#echo "tree_file=\"SimulatedTrees/proposedTree.dnd\"; calibration_file=\"Calibrations_10_n_y/proposedTree_calibrations.Rev\" ; constraint_file=\"Constraints/constraints_uninformative.Rev\" ; clade_file=\"Calibrations_10_n_y/proposedTree_clades.Rev\" ; mean_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_meanBL.nex\" ; var_tree_file=\"Alignments/proposedTree_rescaled_altered_unrooted.dnd.fasta.trees_varBL.nex\"; handle=\"OutputDatingInfoUninfo/Cal_10_n_y_Cons_info\"; source(\"Scripts/DatingRevScripts/mainScript.Rev\");" | rb
