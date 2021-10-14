#!python
#!/usr/bin/env python
#Python script:
import sys
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def show_values_on_bars(axs, total, input_str=""):
    def _show_on_single_plot(ax):        
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + p.get_height()
            value = '{:.2f}'.format(p.get_height())
            ax.text(_x, _y, value+input_str,rotation=45, ha="center", fontsize=8,weight="bold" ) 

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)

def read_result_path(path):
    with open( path, 'r') as file:
        data = file.read()
    data = data.splitlines()
    list_of_lists=[]
    for line in data:
        line = line.split('\t')
        line = [s.strip() for s in line]
        list_of_lists.append(line)
    return list_of_lists

    

def process_files(path):
    nc_list = []
    for n in range(1,14):
        newpath = path + str(n)
        list_nc = read_result_path(newpath)
        list_nc.sort(key = lambda x: x[1]) 
        list_nc = [l[0:2]+[float(l[2])] for l in list_nc]
        if nc_list:
            nc_list = [l+[l2[2]] for l,l2 in zip(nc_list, list_nc) if l[1]==l2[1] ]
        else: 
            nc_list= list_nc
    best_nc = [l[0:2]+[min(l[2:])] + [l[2:].index(min(l[2:]))] for l in nc_list]
    return best_nc


def process_nc(path):
    nc_ll=[]
    for n in range(1,14):
        newpath = path + str(n)
        nc_list=read_result_path(newpath)
        nc_list.sort(key = lambda x: x[1])
        nc_ll.append(nc_list)
    for n in range(1,7):
        newpath = path + "OTHER_" + str(n)
        nc_list=read_result_path(newpath)
        nc_list.sort(key = lambda x: x[1])
        nc_ll.append(nc_list)

    new_nc_ll=[]
    #TODO remove nc_one
    for nc1, nc2, nc3, nc4, nc5, nc6, nc7, nc8, nc9, nc10, nc11, nc12, nc13, nc14, nc15, nc16, nc17, nc18, nc19 in zip(nc_ll[0], nc_ll[1], nc_ll[2], nc_ll[3], nc_ll[4], nc_ll[5], nc_ll[6], nc_ll[7], nc_ll[8], nc_ll[9], nc_ll[10], nc_ll[11], nc_ll[12], nc_ll[13], nc_ll[14], nc_ll[15], nc_ll[16], nc_ll[17], nc_ll[18]):
        if(nc1[1] == nc2[1] == nc3[1] == nc4[1] == nc5[1] == nc6[1] == nc7[1] == nc8[1] == nc9[1] == nc10[1] == nc11[1] == nc12[1] == nc13[1] == nc14[1] == nc15[1] == nc16[1] == nc17[1] == nc18[1] == nc19[1]):
            nc_values = [nc1[2], nc2[2], nc3[2], nc4[2], nc5[2], nc6[2], nc7[2], nc8[2], nc9[2], nc10[2], nc11[2], nc12[2], nc13[2], nc14[2], nc15[2], nc16[2], nc17[2], nc18[2], nc19[2]]
            nc_values = list(map(float, nc_values))
            new_nc_ll.append(nc1[0:2]+ nc_values)
    return new_nc_ll


def locate_min(list_of_values):
    smallest = min(list_of_values)
    return [index for index, element in enumerate(list_of_values) 
                      if smallest == element]

def frequency_histogram(nc_list, save_path):

    nc_info=[]
    nc=[]
    
    for row in nc_list:
        nc_values=row[2:]
        nc_info.append(nc_values)
        minimum_values = locate_min(nc_values)
        nc += minimum_values

    nc_val = [[x+1,nc.count(x)] for x in set(nc)]
    sum_val=sum([val[1] for val in nc_val])
    level14 = [14,0]
    level15 = [15,0]
    nc_val.insert(13, level14)
    nc_val.insert(14, level15)
    level = [x[0] for x in nc_val]
    frequencies = [x[1]*100/sum_val for x in nc_val]

    plt.figure(figsize=(16,9))
    sns.set()
    pal = sns.color_palette("Greens_d", len(frequencies))
    rank = np.array(frequencies).argsort().argsort() 
    ax = sns.barplot(x=level, y=frequencies, palette=np.array(pal[::-1])[rank])
    ax.set(xlabel='Compression Level', ylabel='Frequency')
    show_values_on_bars(ax,len(nc_list), "%")
    plt.savefig(save_path, dpi=900)
    

def sum_total_compression(nc_list, save_path):
    nc_info = [row[2:] for row in nc_list]

    max_range = len(nc_info[0])+1
    total_sum = [sum(x) for x in zip(*nc_info)]
    sum_val = [[num, sum_val] for num, sum_val in zip(range(1,max_range),total_sum)]
    level = [x[0] for x in sum_val]
    totalsum = [x[1] for x in sum_val]

    plt.figure(figsize=(16,9))
    sns.set()
    pal = sns.color_palette("Greens_d", len(totalsum))
    rank = np.array(totalsum).argsort().argsort() 
    ax = sns.barplot(x=level, y=totalsum, palette=np.array(pal[::-1])[rank])
    ax.set(xlabel='Compression Level', ylabel='Sum of Normalized Compression of Each Viral Genome')
    show_values_on_bars(ax,len(nc_list))
    plt.ylim(10000, 11000)
    plt.savefig(save_path, dpi=900)

if __name__ == "__main__":
    print(f"{bcolors.OKGREEN}Performing GeCo3 Level Benchmark for Viral Genome Analysis...{bcolors.ENDC}")
    nc_result_path="../reports/REPORT_COMPLEXITY_NC_"
    print(f"{bcolors.BOLD}Processing results...{bcolors.ENDC}")
    nc_list = process_nc(nc_result_path)
    print(f"{bcolors.BOLD}Creating frequency plot...{bcolors.ENDC}")
    frequency_histogram(nc_list, '../plots/frequency_of_model_selection.pdf')
    print(f"{bcolors.BOLD}Creating sum plot...{bcolors.ENDC}")
    sum_total_compression(nc_list,'../plots/sum_total_nc_models.pdf')
    print(f"{bcolors.OKBLUE}To view results, go to the ./plots folder and see:{bcolors.ENDC}", "frequency_of_model_selection.pdf and sum_total_nc_models.pdf.")
    print(f"{bcolors.OKGREEN}Finished!{bcolors.ENDC}")
    sys.exit()


