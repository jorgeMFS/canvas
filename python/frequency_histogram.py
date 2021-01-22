#!python
#!/usr/bin/env python
#Python script:

import sys
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def show_values_on_bars(axs, total):
    def _show_on_single_plot(ax):        
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + p.get_height()
            value = '{:.2f}'.format(p.get_height()*100/total)+'%'
            ax.text(_x, _y, value, ha="center") 

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)

if __name__ == "__main__":
    
    file = sys.argv[1]
    with open(file, 'r') as file:
        data = file.read()

    data = data.splitlines()
    nc=[]
    file_info=[]
    for line in data:
        file_info.append(line.split('\t')[:2])
        nc.append(min(enumerate(list(map( float, line.split('\t')[2:]))), key=itemgetter(1))[0])

    new_list=[a+[b]for a,b in zip(file_info, nc)]
    nc_val=[[x+1,nc.count(x)] for x in set(nc)]
    level5=[5,0]
    level11=[11,0]
    nc_val.insert(4, level5)
    nc_val.insert(10, level11)
    level = [x[0] for x in nc_val]
    frequencies =  [x[1] for x in nc_val]

    plt.figure(figsize=(16,9))
    sns.set()
    pal = sns.color_palette("Greens_d", len(frequencies))
    rank = np.array(frequencies).argsort().argsort() 
    ax = sns.barplot(x=level, y=frequencies, palette=np.array(pal[::-1])[rank])
    ax.set(xlabel='Compression Level', ylabel='Frequency')
    show_values_on_bars(ax,len(data))
    plt.savefig('../plots/frequency_of_sample.pdf', dpi=900)
    plt.show()