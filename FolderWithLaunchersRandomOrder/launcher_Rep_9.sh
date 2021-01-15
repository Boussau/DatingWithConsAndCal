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
TASKS="28"
# comma separated list of partitions
PARTITIONS="high"
# threads per instance of program needed
THREADS="4"
# expected runtime
TIME="0"
# jobname prefix
JOBNAME="balancedRuns"
#
MEMORY="1500"
#in Mb per CPU
# program to launch
PROGRAMS=( "RandomConstraintOrders/Rep_9/balanced_1.sh" "RandomConstraintOrders/Rep_9/balanced_2.sh" "RandomConstraintOrders/Rep_9/balanced_3.sh" "RandomConstraintOrders/Rep_9/balanced_4.sh" "RandomConstraintOrders/Rep_9/balanced_5.sh" "RandomConstraintOrders/Rep_9/balanced_6.sh" "RandomConstraintOrders/Rep_9/balanced_7.sh" "RandomConstraintOrders/Rep_9/balanced_8.sh" "RandomConstraintOrders/Rep_9/balanced_9.sh" "RandomConstraintOrders/Rep_9/balanced_10.sh" "RandomConstraintOrders/Rep_9/balanced_11.sh" "RandomConstraintOrders/Rep_9/balanced_12.sh" "RandomConstraintOrders/Rep_9/balanced_13.sh" "RandomConstraintOrders/Rep_9/balanced_14.sh"  "RandomConstraintOrders/Rep_9/unbalanced_1.sh" "RandomConstraintOrders/Rep_9/unbalanced_2.sh" "RandomConstraintOrders/Rep_9/unbalanced_3.sh" "RandomConstraintOrders/Rep_9/unbalanced_4.sh" "RandomConstraintOrders/Rep_9/unbalanced_5.sh" "RandomConstraintOrders/Rep_9/unbalanced_6.sh" "RandomConstraintOrders/Rep_9/unbalanced_7.sh" "RandomConstraintOrders/Rep_9/unbalanced_8.sh" "RandomConstraintOrders/Rep_9/unbalanced_9.sh" "RandomConstraintOrders/Rep_9/unbalanced_10.sh" "RandomConstraintOrders/Rep_9/unbalanced_11.sh" "RandomConstraintOrders/Rep_9/unbalanced_12.sh" "RandomConstraintOrders/Rep_9/unbalanced_13.sh" "RandomConstraintOrders/Rep_9/unbalanced_14.sh")

#### Dating the tree without constraints, with balanced calibrations:
for id in "${!PROGRAMS[@]}"; do
srun --mem-per-cpu=${MEMORY} --ntasks-per-node=4 -n ${TASKS} -c $THREADS -o ${JOBNAME}_%j.jobout -p $PARTITIONS -J ${JOBNAME}_0 --time $TIME -- ${PROGRAMS[$id]} > ${JOBNAME}_$id_%j_rb.out &
sleep 1
done


# wait for sruns to finish
