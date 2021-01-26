# Here we run analyses by changing the order of constraints.
# We do 10 replicates, in which constraints are included 1 by 1, from 1 to 14.
# Computations with 0 or 15 constraints do not need to be redone since we have them already.
# That's 140 RevBayes runs in total, times 2 because we use balanced or unbalanced calibrations.
# 280 additional computations total.

# First, producing the Random orders.
mkdir RandomConstraintOrders
python Scripts/makeRandomConstraintOrders.py Constraints/constraints_15.Rev RandomConstraintOrders 10

# Now we have 10 folders each containing 14 (1 to 14 constraints) files.
# We need to launch RevBayes for each set of constraints, on Elte.

#########################################################
# Dating with branch lengths, constraints and calibrations
#########################################################
# We run computations on mellifera.elte.hu
mkdir OutputDatingRandomOrder

# Preparing the bash scripts.
python Scripts/buildScriptsForRandomOrdersOnElte.py RandomConstraintOrders 10

# Preparing the launchers for elte:
python Scripts/buildElteLaunchers_RandomOrder.py FolderWithLaunchersRandomOrder RandomConstraintOrders launchDatingBalancedRandomOrder_Elte.sh 10


# dating the tree with balanced calibrations and varying numbers of constraints, Random Orders, on mellifera.elte:
chmod +x launchAllBalancedJobsRO_Elte.sh
nohup ./launchAllBalancedJobsRO_Elte.sh &

# dating the tree with balanced calibrations and varying numbers of constraints, Random Orders, on mellifera.elte:
chmod +x launchAllUnbalancedJobsRO_Elte.sh
nohup ./launchAllUnbalancedJobsRO_Elte.sh &



# Then we can make map trees for each file.
cd /scratch/boussau/DatingWithConsAndCal/OutputDatingRandomOrder/RandomConstraintOrders
for i in Rep_*/*.trees ; do echo "fname_stem=\"${i/.trees}\" ; source(\"../../Scripts/DatingRevScripts/makeMAPTree.Rev\") ;" | rb ; done
cd ..

# Transferring the trees to my local computer
mkdir Rep_0 Rep_1 Rep_2 Rep_3 Rep_4 Rep_5 Rep_6 Rep_7 Rep_8 Rep_9
for i in Rep* ; do scp mellifera.elte.hu:~/DatingWithConsAndCal/OutputDatingRandomOrder/RandomConstraintOrders/$i/*.tree $i ; done


## Analysing the dated trees
./launchAnalysis.sh > resultAllTrees.txt

grep -A1 "fracInHPD" resultAllTrees.txt | grep -v "fracInHPD" | grep -v "-" > resultAllTreesExcerpt.txt
# then analysis in Analysis of constraints vs calibrations.ipynb
