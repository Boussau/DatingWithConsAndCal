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
TASKS="5"
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
PROGRAMS=("bash balancedNoConstraint.sh" "bash balanced1Constraint.sh" "bash balanced5Constraint.sh" "bash balanced10Constraint.sh" "bash balanced15Constraint.sh")

#### Dating the tree without constraints, with balanced calibrations:
for id in "${!PROGRAMS[@]}"; do
srun --mem-per-cpu=${MEMORY} --ntasks-per-node=4 -n ${TASKS} -c $THREADS -o ${JOBNAME}_%j.jobout -p $PARTITIONS -J ${JOBNAME}_0 --time $TIME -- ${PROGRAMS[$id]} > ${JOBNAME}_$id_%j_rb.out &
sleep 1
done


# wait for sruns to finish
