#!python
#!/usr/bin/env python
#Python script:
from __future__ import print_function
import os
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read_organism_path(path):
    organism_list=[]
    with open( path, 'r') as file:
        data = file.read()
    data = data.splitlines()
    for line in data:
       
        line = line.split('\t')
        line = [s.strip() for s in line]
        if "fasta" in line[0]:
            info= line[0:2]
            species_structure = breakdown(line[2])
            rest=line[3:]
            if len(rest)>1:
                rest=[""]
            rest = [val for val in rest if "taxon" not in val and "segment" not in val and "DNA" not in val and "RNA" not in val]
            organism_list.append(info+species_structure+[rest])
    
    eprint("virus_organism_type_list :",len(organism_list))
    return organism_list

def breakdown(virus_str):
    vr_list = virus_str.split(';')
    vr_list = [s.strip() for s in vr_list]
    return vr_list

def read_genomic_type_path(path):
    virus_genomic_type_list=[]
    with open( path, 'r') as file:
        data = file.read()
    data = data.splitlines()
    for line in data:
        line = line.split('\t')
        line = [s.strip() for s in line]
        if "fasta" in line[0]:
            virus_genomic_type_list.append(line)
    virus_genomic_type_list = [rg for rg in virus_genomic_type_list if len(rg)==4]
    eprint("virus_genomic_type_list :",len(virus_genomic_type_list))
    return virus_genomic_type_list

def process_virus_files():
    rootdir = '../Virus/'
    virus_by_type_path_list=[]
    genome_type=[]
    for subdir, dirs, _ in os.walk(rootdir):
        for d in dirs:
            virus_by_type_path_list.append(os.path.join(rootdir, d))
            genome_type.append(d)
    genome_dict={}

    for path, genome in zip(virus_by_type_path_list,genome_type):
        onlyfiles = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        types_virus = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        virus_taxa_list = list() 
        for path, virus_type in zip(onlyfiles, types_virus):
            pair_list=[]
            viral_list = path_to_list(path)
            pair_list.append([virus_type])
            pair_list.append(viral_list)
            virus_taxa_list.append(pair_list)
        genome_dict[genome]=virus_taxa_list
    return genome_dict

def path_to_list(path):
    with open( path, 'r') as file:
        data = file.read()
    data = data.splitlines()

    vl=[]
    for line in data:
        line = ''.join([str(a).replace('-','').strip() for a in line])
        vl.append(line)
    return vl
    
def match_files(list1, list2):
    grouped_list=[]
    for l1 in list1:
        var=False
        for l2 in list2:
            if l1[0] == l2[0]:
                grouped_list.append(l1[0:]+l2[2:])
                var=True
        if not var:
            eprint("Error in matching!!")
            sys.exit()

    eprint("virus_match_list :",len(grouped_list))
    return grouped_list
    
def save_to_file(list_of_lists, path):
    with open(path, 'w') as f:
        for _list in list_of_lists:
            list_str = "\t".join([str(a) for a in _list])
            f.write(list_str + '\n')

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


def find_taxonomy_group(processed_list, baltimore_info):
    x=[]
    y=[]
    for l in processed_list:
        genomic_string=["dsDNA","ssDNA","dsRNA","ssRNA+","ssRNA-","cRNA","RT"]
        var=False
        for key in genomic_string:
            a = find_virus(baltimore_info[key], l[5:-1])
            if a:
                x.append(l[0:2]+[key] + a)
                var=True
                break
        if not var:
            y.append(l[0:2])
    eprint("taxa list found :", len(x))
    eprint("taxa list not found :", len(y))
    return x,y

def find_virus(b_info, v_list):
    var = False
    for fileb in b_info:
        for v in v_list:
            if v in fileb[1]:
                return [v, fileb[0][0]]

def process_files(path):
    nc_list = []
    for n in range(1,14):
        newpath = path + str(n)
        list_nc = read_file(newpath)
        list_nc.sort(key = lambda x: x[1]) 
        list_nc = [l[0:2]+[100 if float(l[2])==0 else float(l[2])] for l in list_nc]
        if nc_list:
            nc_list = [l+[l2[2]] for l,l2 in zip(nc_list, list_nc) if l[1]==l2[1] ]
        else: 
            nc_list= list_nc
    
    best_nc = [l[0:2]+[min(l[2:])] + [l[2:].index(min(l[2:]))] for l in nc_list]
    eprint("len nc file :", len(best_nc))
    return best_nc

def final_merge(nc_file_list, taxa_result_list):
    taxa_result_list.sort(key = lambda x: x[0])
    eprint("input taxa list len:", len(taxa_result_list))
    final_merge=[]
    not_merged=[]
    for file_nc in nc_file_list:
        filename=file_nc[1]
        filename=filename.split("-")[0]+".fasta"
        var=False
        for file_taxa in taxa_result_list:
            if filename in file_taxa[0]:
                merger = file_taxa + file_nc
                final_merge.append(merger)
                var=True
        if not var:
            not_merged.append([file_nc[0],filename,file_nc[2],file_nc[3],file_nc[4],file_nc[5]])
    
    eprint("len merged file :", len(final_merge))
    return final_merge, not_merged

def join_nc_taxa(nc_list,taxa_result_list):
    taxa_result_list.sort(key = lambda x: x[0])
    eprint("input taxa list len:", len(taxa_result_list))
    final_merge=[]
    not_merged=[]
    for file_nc in nc_list:
        filename=file_nc[1]
        filename=filename.split("-")[0]+".fasta"
        var=False
        for file_taxa in taxa_result_list:
            if filename in file_taxa[0]:
                merger = [filename, file_nc[2], file_taxa[-1]] + file_taxa[3:-1]
                final_merge.append(merger)
                var=True
        if not var:
            if len(file_nc)>3:
                not_merged.append([file_nc[0],filename,file_nc[2],file_nc[3]])
            else:
                not_merged.append([file_nc[0],filename,file_nc[2]])

    eprint("len merged file :", len(final_merge))
    return final_merge, not_merged

def assert_merge(nm, other):
    nm = [a[1]for a in nm]
    other = [a[0]for a in other]
    for a in nm:
        if a not in other:
            eprint("ERROR not suitable")
            sys.error()

def merge_measures(len_seqs, l_nbdm1, l_nbdm2, l_nc):
    len_seqs.sort(key = lambda x: x[1]) 
    l_nbdm1.sort(key = lambda x: x[1]) 
    l_nbdm2.sort(key = lambda x: x[1])
    l_nc.sort(key = lambda x: x[1]) 
    measure_list=[] 
    for ls, bdm1, bdm2, nc in zip(len_seqs, l_nbdm1, l_nbdm2, l_nc):
        if ls[1]==bdm1[1]==bdm2[1]==nc[1]:
            bdm=[bdm1[2]]+[bdm2[2]]
            bdm=[float(a) if a else a for a in bdm ]
            values= ls+bdm+nc[2:]
            measure_list.append(values)
    eprint("len merged measures :", len(measure_list))
    return measure_list

def merge_measures2(len_seqs, l_nbdm1, l_nbdm2, l_nc_IR_0, l_nc_IR_1, l_nc_IR_2):

    len_seqs.sort(key = lambda x: x[1]) 
    l_nbdm1.sort(key = lambda x: x[1]) 
    l_nbdm2.sort(key = lambda x: x[1])
    l_nc_IR_0.sort(key = lambda x: x[1])
    l_nc_IR_1.sort(key = lambda x: x[1])
    l_nc_IR_2.sort(key = lambda x: x[1])
     
    measure_list=[] 
    for ls, bdm1, bdm2, nc_IR0, nc_IR1, nc_IR2 in zip(len_seqs, l_nbdm1, l_nbdm2, l_nc_IR_0, l_nc_IR_1, l_nc_IR_2):
        if ls[1]==bdm1[1]==bdm2[1]==nc_IR0[1]==nc_IR1[1]==nc_IR2[1]:
            bdm=[bdm1[2]]+[bdm2[2]]
            bdm=[float(a) if a else a for a in bdm ]
            values= ls+bdm+[nc_IR0[2]]+[nc_IR1[2]]+[nc_IR2[2]]
            measure_list.append(values)
    eprint("len merged measures :", len(measure_list))
    return measure_list

