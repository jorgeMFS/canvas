#!python
#!/usr/bin/env python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_stx_mt(nc_mr):
    nc_mr = pd.DataFrame.from_records(nc_mr)
    nc_mr.columns =["Mutation Rate (%)", "NC IR 0", "NC IR 2", "NC DIFF", "NBDM", "NC (PAQ)"]
    ax = sns.lineplot(data=pd.melt(nc_mr, ['Mutation Rate (%)'],var_name='Legend', value_name='NC'), x="Mutation Rate (%)", y='NC',hue='Legend')
    ax.set(xlim=(0, 10), ylim=(0, 1.1))
    plt.savefig("../plots/snx_nc_mt.pdf")

def process_variation(nc_list):
    mutation_rate = [round(float(x[0])*100) for x in nc_list]
    nc = [x[2] for x in nc_list]
    return mutation_rate, nc

def nc_diff(nc1_list,nc2_list): 
    diff_nc=[]
    for nc1, nc2 in zip(nc1_list,nc2_list):
        if nc1[1]==nc2[1]:
            diff_nc.append( nc1[0:2]+[float(nc1[2])-float(nc2[2])] + [nc1[3]] )
        else:
            eprint(nc1,nc2)
    return diff_nc

def nc_process_no_floor(path):
    list_nc = read_file(path)
    return [l[0:2]+[float(min(l[2:]))] + [l[2:].index(min(l[2:]))] for l in list_nc]

def read_file(path):
    organism_list=[]
    with open( path, 'r') as file:
        data = file.read()
    data = data.splitlines()
    list_of_lists=[]
    for line in data:
        line = line.split('\t')
        line = [s.strip() for s in line]
        list_of_lists.append(line)
    return list_of_lists

if __name__ == "__main__": 
    NORMAL_STX="../reports/NC_GECO3_OPTIMAL"
    IR_0_STX="../reports/IR_0_GECO3_OPTIMAL"
    IR_1_STX="../reports/IR_1_GECO3_OPTIMAL"
    IR_2_STX="../reports/IR_2_GECO3_OPTIMAL"
    IR_NBDM_STX="../reports/IR_NBMD_OPTIMAL"
    PAQ_STX = "../reports/PAQ_COMPRESS"

    best_nc_for_file_normal_stx = nc_process_no_floor(NORMAL_STX)
    best_nc_for_file_0_stx = nc_process_no_floor(IR_0_STX)
    best_nc_for_file_1_stx = nc_process_no_floor(IR_1_STX)
    best_nc_for_file_2_stx = nc_process_no_floor(IR_2_STX)
    paq_stx = nc_process_no_floor(PAQ_STX)
    nbdm2_stx = nc_process_no_floor(IR_NBDM_STX)


    mr,nc = process_variation(best_nc_for_file_normal_stx)
    _,nc_ir_0 = process_variation(best_nc_for_file_0_stx)
    _,nc_ir_1 = process_variation(best_nc_for_file_1_stx)
    _,nc_ir_2 = process_variation(best_nc_for_file_2_stx)
    _,nbdm_ir = process_variation(nbdm2_stx)
    _,paq = process_variation(paq_stx)
    
    diff_nc_stx = nc_diff(best_nc_for_file_0_stx, best_nc_for_file_2_stx)
    diff_nc_stx2 = [df[2] for df in diff_nc_stx]

    nc_mr = [[a,b,c,d,e,f] for a,b,c,d,e,f in zip(mr, nc_ir_0, nc_ir_1, diff_nc_stx2, nbdm_ir, paq)]
    plot_stx_mt(nc_mr)
    
    print("Synthetic Data : ", best_nc_for_file_0_stx[0][1],", IR O NC : ", best_nc_for_file_0_stx[0][2] )
    print("Synthetic Data : ", best_nc_for_file_1_stx[0][1],", IR 1 NC : ", best_nc_for_file_1_stx[0][2] )
    print("Synthetic Data : ", best_nc_for_file_2_stx[0][1],", IR 2 NC : ", best_nc_for_file_2_stx[0][2] )
    print("Synthetic Data : ", diff_nc_stx[0][1],", diff NC IR 0 and IR 1 : ", diff_nc_stx[0][2])
