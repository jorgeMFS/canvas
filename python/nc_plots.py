#!python
#!/usr/bin/env python
#Python script:

import os
import sys
import statistics
import numpy as np
from math import log
import pandas as pd

import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib.pyplot as plt
import seaborn as sns
from group_by_family import read_file, eprint

def remove_no_result(list_of_lists):
    return [l for l in list_of_lists if len(l)==12]

def grouping_by_index(list_of_lists, index):
    index_list=list(set([x[index] for x in list_of_lists]))
    index_list.sort()
    nc_ll=[]
    la=[]
    nbdm1=[]
    nbdm2=[]
    ll=[]
    for elem in index_list:
        matching = [lst for lst in list_of_lists if elem in lst] 
        ll.append(matching)
        la.append([float(ll[4]) for ll in matching])
        nbdm1.append([float(ll[5]) for ll in matching])
        nbdm2.append([float(ll[6]) for ll in matching])
        nc_ll.append([float(ll[7]) for ll in matching])
    return index_list, nc_ll,la, nbdm1, nbdm2, ll

def average_by_index(list_of_lists, index):
    unique_ele=list(set([x[index] for x in list_of_lists]))
    unique_ele.sort()
    average_by_index=[]
    for ue in unique_ele:
        matching = [lst for lst in list_of_lists if ue in lst]

        len_list = [float(ll[4]) for ll in matching  if ll[4]]
        nbdm1_list = [float(ll[5]) for ll in matching if ll[5]]
        nbdm2_list = [float(ll[6]) for ll in matching if ll[6]]
        nc_list = [float(ll[7]) for ll in matching]
        la=round(sum(len_list) / len(len_list))
        nc=(sum(nc_list) / len(nc_list))
        nbdm1=(sum(nbdm1_list) / len(nbdm1_list))
        nbdm2=(sum(nbdm2_list) / len(nbdm2_list))
        len_std = round(statistics.stdev(len_list))
        print(nc_list)
        nc_std = statistics.stdev(nc_list)
        nbdm1_std = statistics.stdev(nbdm1_list)
        nbdm2_std = statistics.stdev(nbdm2_list)
        n_elen=len(matching)
        
        tax=""
        if index==0:
            genomic_type=ue
            order=""
            family=""
        elif index==1:
            genomic_type=ue
            order=matching[0][1]
            family=""

        elif index==2:   
            genomic_type=ue
            order=matching[0][1]
            family=matching[0][2]
        line = [genomic_type, order, family, tax, la, nbdm1, nbdm2, nc, len_std, nbdm1_std, nbdm2_std, nc_std, n_elen]
        average_by_index.append(line)
    return average_by_index

def average_by_taxid2(list_of_lists):
    taxonomy=list(set([x[3] for x in list_of_lists]))
    taxonomy.sort()
    average_by_taxonomy_id=[]
 
    for tax in taxonomy:
        nbdm1=3
        nbdm2=1
        matching = [lst for lst in list_of_lists if tax in lst] 
        len_list = [float(ll[4]) for ll in matching  if ll[4]]
        nbdm1_list = [float(ll[5]) for ll in matching if ll[5]]
        nbdm2_list = [float(ll[6]) for ll in matching if ll[6]]
        nc_ir0_list = [float(ll[7]) for ll in matching]
        nc_ir1_list = [float(ll[8]) for ll in matching]
        nc_ir2_list = [float(ll[9]) for ll in matching]

        la=(sum(len_list) / len(len_list))
        if nbdm1_list:
            nbdm1=(sum(nbdm1_list) / len(nbdm1_list))
        if nbdm2_list:
            nbdm2=(sum(nbdm2_list) / len(nbdm2_list))
        if nc_ir0_list:
            nc_ir0_list=(sum(nc_ir0_list) / len(nc_ir0_list))
            nc_ir1_list=(sum(nc_ir1_list) / len(nc_ir1_list))
            nc_ir2_list=(sum(nc_ir2_list) / len(nc_ir2_list))
        else:
            print(matching)
            print("ERROR line in 102")
            sys.exit()
            
        line =  [tax, la, nbdm1, nbdm2, nc_ir0_list, nc_ir1_list, nc_ir2_list] + matching[0][10:]
        average_by_taxonomy_id.append(line)
    eprint("size of list average by tax id :",len(average_by_taxonomy_id))
    return average_by_taxonomy_id    

def average_by_taxid(list_of_lists):
    taxonomy=list(set([x[5] for x in list_of_lists]))
    taxonomy.sort()
    average_by_taxonomy_id=[]
 
    for tax in taxonomy:
        nbdm1=3
        nbdm2=1
        matching = [lst for lst in list_of_lists if tax in lst] 
        len_list = [float(ll[7]) for ll in matching  if ll[7]]
        nbdm1_list = [float(ll[8]) for ll in matching if ll[8]]
        nbdm2_list = [float(ll[9]) for ll in matching if ll[9]]
        nc_list = [float(ll[10]) for ll in matching]
        la=(sum(len_list) / len(len_list))
        if nbdm1_list:
            nbdm1=(sum(nbdm1_list) / len(nbdm1_list))
        if nbdm2_list:
            nbdm2=(sum(nbdm2_list) / len(nbdm2_list))
        if nc_list:
            nc=(sum(nc_list) / len(nc_list))
        else:
            print(matching)
            [print(ll[10]) for ll in matching]
            sys.exit()
        genomic_type=matching[0][2]
        order=matching[0][3]
        family=matching[0][4]
        line = [genomic_type, order, family, tax, la, nbdm1, nbdm2, nc]
        
        average_by_taxonomy_id.append(line)
    eprint("size of list average by tax id :",len(average_by_taxonomy_id))
    return average_by_taxonomy_id    

def plot_measure_vs_len(var1, var2, group_var, dataframe, average_dataframe, savepath ):
    df_measure = dataframe.sort_values([var1, var2], ascending=[True, True])
    cnt = dataframe[group_var].value_counts()
    
    gnc=average_dataframe[[group_var,var1]].sort_values(var1, ascending=True)
    medians = gnc[var1].values
    n = [str(x)+"*" for x in cnt.values]
    if len(n)==7:
        nobs = [n[6],n[1],n[2],n[4],n[3],n[5],n[0]]
    plt.clf()
    ax = sns.boxplot(x=group_var, y=var2, data=df_measure, palette="Set3", showfliers = False)
    ax2 = plt.twinx()
    ax = sns.lineplot(x=group_var, y=var1,marker="o", data=df_measure,markers=True, palette="Set3",sizes=(.05, 0.5))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.1f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points')
    if len(n)==7:
        pos = range(len(nobs))
        for tick,label in zip(pos,ax.get_xticklabels()):
            ax.text(pos[tick], medians[tick] + 0.03, nobs[tick],
                horizontalalignment='center', size='x-small', color='k', weight='semibold')

    ax.set_yscale('log')
    
    plt.savefig(savepath)
    plt.clf()

def filter_and_plot_measure_vs_len(var_to_filter, filtername, dataframe, var1, var2, group_var, savepath):
    df_filter = dataframe[(dataframe[var_to_filter] == filtername)]
    df_measure = df_filter.sort_values([var1, var2], ascending=[True, True])
    plt.clf()
    ax = sns.boxplot(x=group_var, y=var2, data=df_measure, palette="Set3", showfliers = False)
    ax2 = plt.twinx()
    ax = sns.lineplot(x=group_var, y=var1,marker="o", data=df_measure,markers=True, palette="Set3",sizes=(.05, 0.5))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.tick_params(labelrotation=45)
    ax.set_title(filtername)
    ax.set_yscale('log')
    plt.savefig(savepath)
    plt.clf()

if __name__ == "__main__":
    merged_nc_info=read_file('../VirusDB/ViralSeq_Merged.info')

    merged_nc_info=remove_no_result(merged_nc_info)
    ll = average_by_taxid(merged_nc_info)

    avg_genome=average_by_index(ll,0)
    avg_gen = pd.DataFrame.from_records(avg_genome)
    avg_gen.columns =["Genome_Type", "Match", "Group", "Taxonomy_ID", "Sequence_Length", "NBDM1","NBDM2","Normalized_Compression", "sq_std", "nbdm1_std", "nbdm2_std", "nc_std", "n_elem" ]
    

    df = pd.DataFrame.from_records(ll)
    df.columns =["Genome_Type", "Match", "Group", "Taxonomy_ID", "Sequence_Length", "NBDM1","NBDM2","Normalized_Compression"]
    #####Scatterplot###########
    g = sns.scatterplot(x="Sequence_Length", y="Normalized_Compression", hue="Genome_Type" , data=df, palette="Set1")
    g.set_xscale('log')
    plt.savefig('../plots/gen_nc.pdf')
    plt.clf()
    ################
    plot_measure_vs_len('Sequence_Length', "Normalized_Compression", "Genome_Type", df, avg_gen, '../plots/gen_nc_len_2d.pdf' )
    plot_measure_vs_len('Sequence_Length', "NBDM1", "Genome_Type", df, avg_gen, '../plots/gen_nbdm1_len.pdf' )
    plot_measure_vs_len('Sequence_Length', "NBDM2", "Genome_Type", df, avg_gen, '../plots/gen_nbdm2_len.pdf' )
    ###########
    
    # sns.catplot(x="Group", y="Normalized_Compression",col="Genome_Type", data=df, kind="box", height=4, aspect=.7)
    filter_and_plot_measure_vs_len("Genome_Type", "dsDNA", df, "Sequence_Length", "Normalized_Compression", "Group", "../plots/dsDNA.pdf")
    filter_and_plot_measure_vs_len("Genome_Type", "ssDNA", df, "Sequence_Length", "Normalized_Compression", "Group", "../plots/ssDNA.pdf")
    filter_and_plot_measure_vs_len("Genome_Type", "dsRNA", df, "Sequence_Length", "Normalized_Compression", "Group", "../plots/dsRNA.pdf")
    filter_and_plot_measure_vs_len("Genome_Type", "ssRNA-", df, "Sequence_Length", "Normalized_Compression", "Group", "../plots/ssRNA-.pdf")
    filter_and_plot_measure_vs_len("Genome_Type", "ssRNA+", df, "Sequence_Length", "Normalized_Compression", "Group", "../plots/ssRNA+.pdf")
    filter_and_plot_measure_vs_len("Genome_Type", "RT", df, "Sequence_Length", "Normalized_Compression", "Group", "../plots/RT.pdf")
    filter_and_plot_measure_vs_len("Genome_Type", "cRNA", df, "Sequence_Length", "Normalized_Compression", "Group", "../plots/cRNA.pdf")
