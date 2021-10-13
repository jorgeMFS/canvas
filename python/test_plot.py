#!python
#!/usr/bin/env python
import matplotlib.pyplot as plt
import seaborn as sns

x = ['day 1', 'day 2', 'day 3']
y = [1, 5, 4]
z=[10,7,2]
g2 = sns.lineplot(x=x, y=y, marker="o", markers=True, palette="Set3",sizes=(.05, 0.5))
g2.set_ylabel("Sequence Length",fontsize='small')
g2.xaxis.set_tick_params(labelsize='x-small')
g2.set_xlabel("Day",fontsize='small')
g2.set_xticklabels(x)
g2.set_xticklabels(g2.get_xticklabels(), rotation=30)
g2.set(yscale="log") 
ax2 = plt.twinx()
ax2.set_xlabel(y,fontsize='small')
ax2.set_ylabel(y,fontsize='small')
g = sns.boxplot(x=x, y=z,ax=ax2, showfliers = False)
plt.show()