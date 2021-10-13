#!python
#!/usr/bin/env python

from collections import Counter
import numpy as np
import statistics
import os

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

def to_dict(lst):
    d = {}
    for el,i in zip(lst, range(0,len(lst))):
        d[el] = i
    return d


def max_min(list_nc):
    nc_v=[x[2] for x in list_nc]
    std = statistics.stdev(nc_v)
    average = sum(nc_v)/len(nc_v)
    max_v=average+(3*std)
    min_v=average-(3*std)

    return max_v, min_v

def filter_outliers(list_len, list_gc, list_nc, list_ir0, list_ir1, list_ir2):
    max_nc, min_nc = max_min(list_nc)
    max_ir0, min_ir0 = max_min(list_ir0)
    max_ir1, min_ir1 = max_min(list_ir1)
    max_ir2, min_ir2 = max_min(list_ir2)
    new_len_list=[]
    new_gc_list=[]
    new_nc_list=[]
    new_ir0_list=[]
    new_ir1_list=[]
    new_ir2_list=[]
    for ln, gc, nc, ir0, ir1, ir2 in zip(list_len, list_gc, list_nc, list_ir0, list_ir1, list_ir2):
        
        if (ln[1]==gc[1]==nc[1]==ir0[1] == ir1[1] == ir2[1]) and (nc[2]>min_nc and nc[2]<max_nc) and (ir0[2]>min_ir0 and ir0[2]<max_ir0) and (ir1[2]>min_ir1 and ir1[2]<max_ir1) and (ir2[2]>min_ir2 and ir2[2]<max_ir2):
            new_len_list.append(ln)
            new_gc_list.append(gc)
            new_nc_list.append(nc)
            new_ir0_list.append(ir0)
            new_ir1_list.append(ir1)
            new_ir2_list.append(ir2)
        elif(ln[1]==gc[1]==nc[1]==ir0[1] == ir1[1] == ir2[1])==False:
            print("ERROR files do not coincide")
            print(ln, gc, nc, ir0, ir1, ir2)
            sys.exit()    

    return  new_len_list, new_gc_list, new_nc_list, new_ir0_list, new_ir1_list, new_ir2_list

def nc_process_no_floor(path):
    list_nc = read_file(path)
    return [l[0:2]+[float(min(l[2:]))] + [l[2:].index(min(l[2:]))] for l in list_nc]

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
    print("virus_genomic_type_list :",len(virus_genomic_type_list))
    return virus_genomic_type_list

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
    
    print("virus_organism_type_list :",len(organism_list))
    return organism_list

def match_files(list1, list2):
    grouped_list=[]
    for l1 in list1:
        var=False
        for l2 in list2:
            if l1[0] == l2[0]:
                grouped_list.append(l1[0:]+l2[2:])
                var=True
        if not var:
            print("Error in matching!!")
            sys.exit()

    print("virus_match_list :",len(grouped_list))
    return grouped_list

def process_meta_information(meta_information_list):
    metainfo=[]
    for meta_information in meta_information_list :
        strand = meta_information[2:4]
        strand.reverse()
        strand = [''.join(strand).replace("double","ds").replace("single","ss")]
        taxic_info = meta_information[0:2] + strand + meta_information[4:]
        metainfo.append(taxic_info)
    return metainfo

def read_to_list(ignore_taxa_file):
    corrections=[line.replace("\n","") for line in open(ignore_taxa_file, 'r')]
    return corrections

def read_and_correct(file_path, organism_list):
    corrections=[line.split() for line in open(file_path, 'r')]
    item_list=[x[-1] for x in corrections]
    ind=0
    for item in item_list:
        for org in organism_list:
            if item in org:
                pos=org.index(item)
                if org[pos-1]==corrections[ind][0]:
                    org[pos:pos] = corrections[ind][1:-1]
        ind+=1
    return organism_list

def filter_from_ll(list_ir, ign_taxa):
    for taxa in ign_taxa:
        list_ir = [[ele for ele in sub if ele != taxa] for sub in list_ir]
    return list_ir

def filter_meta_info(meta_info):
    new_org=[]
    for meta in meta_info:
        if len(meta)>=12:
            not_detected=True
            for org in meta:
                if "unclassified" in org:
                    not_detected=False
            if not_detected:
                new_org.append(meta)
    l=[]
    for x in new_org:
        if len(x)>12:
            x.pop(len(x)-2)
        l.append(x)
    return l

def join_for_class_array(len_seq, gc_seq, nc_file, best_nc_for_file_0, best_nc_for_file_1, best_nc_for_file_2,meta_info, index):
    clsf_list=list(set([x[index] for x in meta_info if "incertae_sedis" not in x[index]]))
    cnt = Counter([x[index] for x in meta_info if "incertae_sedis" not in x[index]])
    
    remove_list=[]
    for name, count in cnt.items():
        if count<=2:
            remove_list.append(name)
    [clsf_list.remove(r) for r in remove_list]
    clsf = to_dict(clsf_list)
    virus=[]
    classifier=[]
    for x in meta_info:
        num_x=x[0].replace('.fasta','')
        for l_sq, gc_sq, nc, ir_0, ir_1, ir_2 in zip(len_seq, gc_seq, nc_file, best_nc_for_file_0, best_nc_for_file_1, best_nc_for_file_2):
            num_y=l_sq[1].split("-")[0]
            if num_x == num_y and "incertae_sedis" not in x[index] and x[index] not in remove_list:
                num_x=num_x.replace('out','')
                classifier.append(clsf.get(x[index]))    
                virus.append([int(num_x),int(l_sq[2]),float(gc_sq[2]),float(nc[2]), float(ir_0[2]),float(ir_1[2]),float(ir_2[2])])   
    virus=np.array(virus)
    classifier=np.array(classifier).astype('int32')
    return virus, classifier



def restructure_data(save_folder, len_seq, gc_seq, nc_file, best_nc_for_file_0, best_nc_for_file_1, best_nc_for_file_2,meta_info ):
    index_lst=[2,4,5,6,7,8,9,10]
    clss=["Genome","Realm","Kingdom","Phylum","Class","Order","Family","Genus"]
    if not os.path.exists(save_folder):
        print("creating folder...")
        os.makedirs(save_folder)
    for index,tx in zip(index_lst, clss):
        data, labels = join_for_class_array(len_seq, gc_seq, nc_file, best_nc_for_file_0, best_nc_for_file_1, best_nc_for_file_2,meta_info, index)
        print("Number of labels for "+ tx+ " =", len(set(labels)))
        np.save(save_folder+'/'+tx+'_'+'y_data.npy', labels)
        np.save(save_folder+'/'+tx+'_'+'x_data.npy', data)

if __name__ == "__main__": 
    
    ## Paths
    #Metadata for labels
    organism_path="../VirusDB/ViralSeq_Org.info"
    genomic_type_path="../VirusDB/ViralSeq_Genome.info"
    #Features
    LQ_PATH="../reports/REPORT_SEQ_LEN"
    GC_PATH="../reports/REPORT_SEQ_GC"
    NC_PATH="../reports/REPORT_COMPLEXITY_NC_OTHER_3"
    IR_0_PATH="../reports/Report_NC_IR_OPTIMAL_0"
    IR_1_PATH="../reports/Report_NC_IR_OPTIMAL_1"
    IR_2_PATH="../reports/Report_NC_IR_OPTIMAL_2"

    #Process meta_information into list
    print(f"{bcolors.OKGREEN}Processing metagenomic information to create labels...{bcolors.ENDC}")
    rg_list = read_genomic_type_path(genomic_type_path)
    ro_list = read_organism_path(organism_path)
    ll = match_files(rg_list,ro_list)
    meta_info = process_meta_information(ll)
    meta_info = read_and_correct("../VirusDB/correct_taxa.txt", meta_info)
    tax_ign=read_to_list("../VirusDB/ignoretax.txt")
    meta_info=filter_from_ll(meta_info, tax_ign)
    meta_info=filter_meta_info(meta_info)

    ## Process Features
    print(f"{bcolors.OKGREEN}Processing features...{bcolors.ENDC}")
    # Normal NC
    nc_file=nc_process_no_floor(NC_PATH)
    #Context model Compression
    best_nc_for_file_0 = nc_process_no_floor(IR_0_PATH)
    #Mixed Compression
    best_nc_for_file_1 = nc_process_no_floor(IR_1_PATH)
    #IR-based Compression
    best_nc_for_file_2 = nc_process_no_floor(IR_2_PATH)
    #GC-Content 
    gc_seq=read_file(GC_PATH)
    #Sequence Length
    len_seq=read_file(LQ_PATH)

    #Filter outliers in data
    len_seq, gc_seq, nc_file, best_nc_for_file_0, best_nc_for_file_1, best_nc_for_file_2 = filter_outliers(len_seq, gc_seq, nc_file,best_nc_for_file_0, best_nc_for_file_1,best_nc_for_file_2)
    
    #Save to numpy array
    print(f"{bcolors.OKGREEN}Creating dataset...{bcolors.ENDC}")
    restructure_data('../data',len_seq, gc_seq, nc_file, best_nc_for_file_0, best_nc_for_file_1, best_nc_for_file_2,meta_info)
    print(f"{bcolors.OKGREEN}The dataset was successfully stored in the /data folder.{bcolors.ENDC}")
