#!python
#!/usr/bin/env python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from group_by_family import read_file

def get_transformed_list(joined_variables):
    reshaped_list=[]
    for x in joined_variables:
        reshaped_list.append(x[0:2] + [x[2], "IR 0"])
        reshaped_list.append(x[0:2] + [x[3], "IR 1"] )
        reshaped_list.append(x[0:2] + [x[4], "IR 2"])
    return reshaped_list


if __name__ == "__main__": 
    HHV_path="../reports/REPORT_HHV"
    hhv = read_file(HHV_path)
    hhv = [[x[0],int(x[1]),float(x[2]),float(x[3]),float(x[4])] for x in hhv]
    hhv_reshaped = get_transformed_list(hhv)
    
    virus=[x[0] for x in hhv]
    length=[x[1] for x in hhv]
    NC_IR0=[x[2] for x in hhv]
    NC_IR1=[x[3] for x in hhv]
    NC_IR2=[x[4] for x in hhv]

    df = pd.DataFrame.from_records(hhv_reshaped)
    df.columns =["Species","Sequence_Length","Normalized_Compression","Program"]
    
    hue_order = ["IR 0", "IR 1","IR 2"]
    g2 = sns.lineplot(x=virus, y=length, marker="o", markers=True,sort=False, palette="Set3",sizes=(.001, 0.01))
    g2.set_ylabel("Sequence Length",fontsize='medium', fontweight = "semibold")
    g2.xaxis.set_tick_params(labelsize='small')
    g2.set_xticklabels(virus, fontweight = "semibold")
    g2.set(yscale="log") 
    for x, y in zip(virus, length):
        plt.text(x = x, 
        y = y-0.006, 
        s = '{:.0f}'.format(y), 
        fontsize = "x-small",
        fontweight = "bold",
        color = 'steelblue') 

    ax2 = plt.twinx()
    ax2.set_xlabel("Virus",fontsize='small')
    ax2.set_ylabel("Normalized Compression",fontsize='medium', fontweight = "semibold")
    ax2.set(ylim=(0.8, 1))
    g = sns.barplot(x="Species", y="Normalized_Compression", data=df,order=virus,hue="Program",hue_order=hue_order, palette="Set3",ax=ax2)
    plt.savefig("../plots/HHV_barplot.pdf",  bbox_inches='tight')
    plt.clf()