#!python
#!/usr/bin/env python
#Python script:
import sys
import numpy as np
from pybdm import BDM
from pybdm import options

options.set(raise_if_zero=False)
options.set(warn_if_missing_ctm=False)

file = sys.argv[1]

with open(file, 'r') as file:
   data = file.read()

Translator =	{
  "A": 0,
  "C": 1,
  "G": 2,
  "T": 3
}
datafile=list(map(lambda x: Translator[x],data))

datafile = np.asarray(datafile)

bdm = BDM(ndim=1,nsymbols=4)
value = bdm.bdm(datafile)
value=(value/datafile.size)
print(value)
