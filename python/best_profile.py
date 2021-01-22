#!python
#!/usr/bin/env python
#Python script:

import sys
from operator import itemgetter
import numpy as np

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

f = open("demofile2.txt", "a")
for line in new_list: 
    line[1]+=".fasta"
    line[2]=str(line[2])
    sentence = '\t'.join(line) +"\n"
    f.write(sentence)

f.close()


