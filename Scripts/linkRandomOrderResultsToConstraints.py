import sys

random_order_file = sys.argv[1] # file containing results from launchAnalysisRandomOrder.sh and the subsequent grep
chosen_order_file = sys.argv[2] # file containing results from launchAnalysis.sh and the subsequent grep
constraints_file = sys.argv[3] # list of 15 constraints
out = sys.argv[4]

constraints_list = list()
with open(constraints_file, "r") as fin:
    for l in fin:
        constraints_list.append(l.strip())

with open(out, "w") as fout:
    fout.write("TreeId\tnumCalib\tnumCons\tbalanced\told_biased\tcorrelation\trmsd\trmsd_norm\tcor_bls\trmsd_bls\tnum_nodes\tnumInHPD\tfracInHPD\tpercent0\tpercent25\tpercent50\tpercents75\tpercent100\trep\tlistCons\t" )
    for constraint in constraints_list:
        fout.write(constraint.replace("\t",",", 1).replace("\t","->", 1).replace("\t",",", 1)+"\t")
    fout.write("\n")
    #Getting the results from the chosen order
    with open(chosen_order_file, "r") as fin:
        for l in fin:
            num_1s = int(l.split()[2])
            fout.write(l.strip() + "\t15")
            for i in range(num_1s):
                fout.write("\t1")
            for i in range(15-num_1s):
                fout.write("\t0")
            fout.write("\n")
    #Getting the results from the random order
    with open(random_order_file, "r") as fin:
        for l in fin:
            li = l.split("\t")
            rep = li[18].strip()
            numCons = li[2]
            liCons = str()
            filename = "RandomConstraintOrders/Rep_"+ rep +"/constraints_"+ numCons +".Rev"
            with open(filename, 'r') as fcons:
                for l2 in fcons:
                    liCons += l2.strip() + "||"
            presence_absence = str()
            for constraint in constraints_list:
                if constraint in liCons:
                    presence_absence = presence_absence + "1\t"
                else:
                    presence_absence = presence_absence + "0\t"
            fout.write(l.strip() + "\t" + liCons + "\t"+ presence_absence + "\n")
