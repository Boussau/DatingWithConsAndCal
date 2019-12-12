import os
import sys
from subprocess import call

file=sys.argv[1]
out=sys.argv[2]
numCalibrations=int(sys.argv[3])
numConstraints=int(sys.argv[4])
numReplicates=int(sys.argv[5])

numTree = file.split("_")[1]

prefix = numTree + "_" + str(numCalibrations) + "_" + str(numConstraints) + "_"


pbs_header = "#!/bin/bash\n#SBATCH --cpus-per-task=1\n#SBATCH --nodes=1\n#SBATCH --mem-per-cpu=4000\n#SBATCH --time=24:00:00\n#SBATCH -o /beegfs/data/boussau/TransferRelated/datingWithConstraints/ReplicatedAnalysis/Output/logs_"+prefix+".o\n#SBATCH -e /beegfs/data/boussau/TransferRelated/datingWithConstraints/ReplicatedAnalysis/Output/logs_"+prefix+".e\ncd /beegfs/data/boussau/TransferRelated/datingWithConstraints/ReplicatedAnalysis/"

#pbs_header = "#PBS -q q1day\n#PBS -l nodes=1:ppn=1\n#PBS -l mem=4gb\n#PBS -o /pandata/boussau/replicatedAnalysis/logs_"+prefix+".o\n#PBS -e /pandata/boussau/replicatedAnalysis/logs_"+prefix+".e\ncd /pandata/boussau/replicatedAnalysis\n"
#/pandata/boussau/revbayes/revbayes/projects/cmake/rb analysisConstrained.Rev


print(pbs_header)

for i in range(numReplicates):
    print("\n#Replicate "+str(i))
    index = prefix +str(i+1)
    name = index + "_RandomCalibrations.Rev"
    outCalibrations = os.path.join(out, name)
    os.system("/usr/bin/python3 sampleCalibrations.py calibrations/"+ file +"_calibrations.Rev " + outCalibrations + " " + str(numCalibrations))
    name = index + "_RandomConstraints.txt"
    outConstraints = os.path.join(out, name)
    os.system("/usr/bin/python3 randomlySampleLines.py constraints/"+ file +"_constraints.txt " + outConstraints + " " + str(numConstraints))
    rb_command = 'aln_file=\\"data/'+file+'.fa\\"; '+'tree_file=\\"'+file+'.dnd\\"; clade_file=\\"clades/'+file+'_clades.Rev\\"; calibration_file=\\"'+outCalibrations+'\\"; constraint_file=\\"'+outConstraints+'\\"; job_id=\\"'+index+'\\"; source(\\"analysisCalibratedConstrainedUnExp.Rev\\");\"'
#        rb_command = 'aln_file=\\"data/'+file+'.fa\\"; '+'tree_file=\\"'+file+'.dnd\\"; clade_file=\\"clades/'+file+'_clades.Rev\\"; calibration_file=\\"calibrations/'+file+'_calibrations.Rev\\"; constraint_file=\\"constraints/'+file+'_constraints.txt\\"; job_id=\\"'+index+'\\"; source(\\"analysisCalibratedConstrainedUnExp.Rev\\");\"'
    #print('echo \"'+ rb_command + '| /Users/boussau/programming/revbayes/projects/cmake/rb ')
#    print('echo \"'+ rb_command + '| /pandata/boussau/revbayes/revbayes/projects/cmake/rb ')
    print('echo \"' + rb_command + '| /beegfs/data/boussau/Software/revbayes/projects/cmake/rb ')
