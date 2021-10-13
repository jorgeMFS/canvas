#!python
#!/usr/bin/env python


import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
A=[['out924.fasta', 1, 'Albetovirus', 'Viruses', 'Riboviria', 'Albetovirus', 'Nicotiana benthamiana'],
['out12054.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Levivirus', 'mat'],
['out11811.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'unclassified Leviviridae'],
['out9957.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Levivirus'],
['out12127.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Allolevivirus', 'SP_1'],
['out7910.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Levivirus'],
['out7908.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Levivirus'],
['out7937.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Levivirus', 'Escherichia coli J53 (plasmid RIP69)'],
['out11205.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'unclassified Leviviridae'],
['out12060.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Levivirus', 'Escherichia coli'],
['out11543.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Allolevivirus', 'Escherichia coli'],
['out5567.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'Allolevivirus'],
['out8027.fasta', 1, 'Allassoviricetes', 'Viruses', 'Riboviria', 'Orthornavirae', 'Lenarviricota', 'Allassoviricetes', 'Levivirales', 'Leviviridae', 'unclassified Leviviridae', 'Caulobacter crescentus'],
['out7892.fasta', 0.9465, 'Alphabaculovirus', 'Viruses', 'Baculoviridae', 'Alphabaculovirus', 'Thysanoplusia orichalcea'],
['out11492.fasta', 0.931, 'Alphabaculovirus', 'Viruses', 'Baculoviridae', 'Alphabaculovirus', 'enhancer; replication origin'],
['out11380.fasta', 0.963, 'Alphabaculovirus', 'Viruses', 'Baculoviridae', 'Alphabaculovirus', 'SenVgp001']]


