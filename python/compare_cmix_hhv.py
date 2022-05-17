#!python
#!/usr/bin/env python

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from group_by_family import read_file

def get_transformed_list(joined_variables):
    reshaped_list=[]
    for x in joined_variables:
        reshaped_list.append(x[0:2] +["cmix"])
        reshaped_list.append([x[0]] + [x[2], "geco3"] )
    return reshaped_list



if __name__ == "__main__": 
    HHV_path="../reports/REPORT_CMIX_GECO3_HHV"
    hhv = read_file(HHV_path)
    hhv = [[x[0],round(float(x[1]),3),round(float(x[2]),3),round(float(x[3]),3),round(float(x[4]),3)] for x in hhv]
    data=[x[1:] for x in hhv]
    avg = list(map(lambda x: round(sum(x)/len(x),3), zip(*data)))
    hhv.append(["Average"]+avg)
    p = pd.DataFrame.from_records(hhv)
    p.columns =["Species","duration_cmix(s)","duration_geco3(s)","NC_cmix","NC_geco3"]
    print(p.to_string()) 

    names=[x[0] for x in hhv]
    time=[x[0:3] for x in hhv]
    NC=[[x[0],x[3],x[4]] for x in hhv]
    nc=get_transformed_list(NC)
    time=get_transformed_list(time)
    hue_order=["cmix","geco3"]
    df = pd.DataFrame.from_records(nc)
    df.columns =["Species","Normalized_Compression","Program"]
    df2 = pd.DataFrame.from_records(time)
    df2.columns =["Species","Time","Program"]
    hue_order = ["cmix", "geco3"]
    g = sns.barplot(x="Species", y="Normalized_Compression", data=df,order=names, hue="Program", hue_order=hue_order, palette="Set2")
    g.set(ylim=(0.8, 1))
    g.set_ylabel("Normalized Compression",fontsize='medium', fontweight = "semibold")
    g.set_xlabel("Species",fontsize='medium', fontweight = "semibold")
    g.xaxis.set_tick_params(labelsize='small')
    g.set_xticklabels(names, fontweight = "semibold")
    plt.savefig("../plots/cmix_geco_nc.pdf",  bbox_inches='tight')
    plt.clf()

    hue_order = ["cmix", "geco3"]
    g2 = sns.barplot(x="Species", y="Time", data=df2,order=names, hue="Program", hue_order=hue_order, palette="Set2")
    g2.set_yscale('log')
    g2.set_ylabel("Duration \n (seconds)",fontsize='medium', fontweight = "semibold")
    g2.set_xlabel("Species",fontsize='medium', fontweight = "semibold")
    g2.xaxis.set_tick_params(labelsize='small')
    g2.set_xticklabels(names, fontweight = "semibold")
    plt.savefig("../plots/cmix_geco_time.pdf",  bbox_inches='tight')
    plt.clf()