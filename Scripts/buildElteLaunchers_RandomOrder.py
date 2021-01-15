import os
import random
import sys

folder_with_launchers = sys.argv[1]
folder_with_scripts = sys.argv[2]
base_launcher = sys.argv[3]
num = int(sys.argv[4])  # Number of random orders


lines = str()
with open(base_launcher, "r") as fin:
    for l in fin:
        lines = lines + l

for i in range(num):
    # Folder for replicate i
    out_i = os.path.join(folder_with_scripts, "Rep_"+str(i))
    all_scripts_balanced = str()
    all_scripts_unbalanced = str()
    for j in range(1, 15):
        # write down 1 string for the balanced case,
        # and 1 string for the unbalanced case.
        all_scripts_balanced = all_scripts_balanced + " \"" + \
            os.path.join(out_i, "balanced_" + str(j) + ".sh\"")
        all_scripts_unbalanced = all_scripts_unbalanced + " \"" + \
            os.path.join(out_i, "unbalanced_" + str(j) + ".sh\"")
    with open(os.path.join(folder_with_launchers, "launcher_Rep_" + str(i) + ".sh"), "w") as fout:
        fout.write(lines.replace("\"TOREPLACEWITH28JOBS\"", all_scripts_balanced +
                                 " " + all_scripts_unbalanced))
