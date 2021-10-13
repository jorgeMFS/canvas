
#!python
#!/usr/bin/env python
import os
import statistics
import matplotlib.pyplot as plt
import matplotlib as mpl
from ete3 import Tree
try:
    from ete3 import TreeStyle, TextFace, NodeStyle, faces, RectFace, CircleFace, ImgFace, add_face_to_node
except ImportError as e:
    print(e)

    
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

def nc_process_no_floor(path):
    list_nc = read_file(path)
    return [l[0:2]+[float(min(l[2:]))] + [l[2:].index(min(l[2:]))] for l in list_nc]

def max_min(list_nc):
    nc_v=[x[2] for x in list_nc]
    std = statistics.stdev(nc_v)
    average = sum(nc_v)/len(nc_v)
    max_v=average+(3*std)
    min_v=average-(3*std)

    return max_v, min_v

def nc_diff(nc1_list,nc2_list): 
    diff_nc=[]
    for nc1, nc2 in zip(nc1_list,nc2_list):
        if nc1[1]==nc2[1]:
            diff_nc.append( nc1[0:2]+[float(nc1[2])-float(nc2[2])] + [nc1[3]] )
        else:
            eprint(nc1,nc2)
    return diff_nc

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
            eprint("ERROR files do not coincide")
            eprint(ln, gc, nc, ir0, ir1, ir2)
            sys.exit()    

    return  new_len_list, new_gc_list, new_nc_list, new_ir0_list, new_ir1_list, new_ir2_list


def flatten(regular_list):
    return [item for sublist in regular_list for item in sublist]

def filter_organism_list(organism_names):
    new_org=[]
    for org_des in organism_names:
        if len(org_des)>=8:
            not_detected=True
            for org in org_des:
                if "unclassified" in org:
                    not_detected=False
            if not_detected:
                new_org.append(org_des)
    new_org=[x[:-1] if len(x)>8  else x for x in new_org ] 
    return new_org

def read_to_list(ignore_taxa_file):
    corrections=[line.replace("\n","") for line in open(ignore_taxa_file, 'r')]
    return corrections

def filter_from_ll(list_ir, ign_taxa):
    for taxa in ign_taxa:
        list_ir = [[ele for ele in sub if ele != taxa] for sub in list_ir]
    return list_ir

def breakdown(virus_str):
    vr_list = virus_str.split(';')
    vr_list = [s.strip() for s in vr_list]
    return vr_list

def tree_average(nc_value_list):
    build_avg=[]
    elements_list=[]
    nc_list=[]
    ul=[]
    for x in nc_value_list:
        ul.append(x[1:])
    ul=list(set([item for sublist in ul for item in sublist])) 
    for elem in ul:
        avg_list=[]
        for x in nc_value_list:
            if elem in x:
                avg_list.append(x[0])
        build_avg.append([elem, sum(avg_list) / len(avg_list)])
    
    return build_avg

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


def process_organism_lists(organism_list_lists):
    unique_organims = [list(x) for x in set(tuple(x) for x in organism_list_lists)]
    unique_organims = [list(filter(None, lst)) for lst in unique_organims]
    unique_tax_list = list(set(flatten(unique_organims)))
    unique_taxa_occurance = list()
    for x in unique_tax_list:
        counter=0
        indices = set()
        for l in unique_organims:
            for i in range(0,len(l)):
                if x == l[i]:
                    counter+=1
                    indices.add(i)
                    
        taxa=[x, counter] + list(indices)
        unique_taxa_occurance.append(taxa)
        if len(list(indices))>1:
            print("Error With taxonomy")
    unique_taxa_occurance.sort(key=lambda x: x[1],reverse=True)

    return unique_taxa_occurance

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

def process_meta_information(meta_information_list):
    metainfo=[]
    for meta_information in meta_information_list :
        strand = meta_information[2:4]
        strand.reverse()
        strand = [''.join(strand).replace("double","ds").replace("single","ss")]
        taxic_info = meta_information[0:2] + strand + meta_information[4:]
        metainfo.append(taxic_info)
    return metainfo

def join_nc_taxa(nc_list,taxa_result_list):
    taxa_result_list.sort(key = lambda x: x[0])
    print("input taxa list len:", len(taxa_result_list))
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

    print("len merged file :", len(final_merge))
    return final_merge, not_merged


def bfs_edge_lst(graph, n):
    return list(nx.bfs_edges(graph, n))

def tree_from_edge_lst(elst):
    tree = {"Viruses": {}}
    for src, dst in elst:
        subt = recursive_search(tree, src)
        if subt:
            print(subt)
            subt[dst] = {}
    return tree

def recursive_search(dicts, key):
    if key in dicts:
        return dicts[key]
    for k, v in dicts.items():
        item = recursive_search(v, key)
        if item is not None:
            return item

def tree_to_newick(tree):
    items = []
    for k in tree.keys():
        s = ''
        if len(tree[k].keys()) > 0:
            subt = tree_to_newick(tree[k])
            if subt != '':
                s += '(' + str(subt) + ')'
        s += str(k)
        items.append(s)
    return ','.join(items)

def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b

def rgb2(minimum, maximum, value):
    value= (1-0)/(maximum-minimum)*(value-maximum)+1
    # color1=[255,255,0]
    color1=[0,0,255] # RGB for our 1st color (blue in this case).
    color2=[255,0,0]  #RGB for our 2nd color (red in this case)

    red   = int((color2[0] - color1[0]) * value + color1[0])     # Evaluated as -255*value + 255.
    green = int((color2[1] - color1[1]) * value + color1[1])      # Evaluates as 0.
    blue  = int((color2[2] - color1[2]) * value + color1[2])      # Evaluates as 255*value + 0.
    
    return red,green,blue


def colorbar(mn, mx, xvar, savepath):
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    cnorm = mpl.colors.Normalize(vmin=mn, vmax=mx)
    cm1 = mpl.colors.LinearSegmentedColormap.from_list("MyCmapName",["b","r"])
    cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cm1,
                                    norm=cnorm,
                                    orientation='horizontal')
    cb1.set_label(xvar)
    plt.savefig(savepath,  bbox_inches='tight',dpi=1000)
    plt.clf()
    plt.close(1)



def filter_based_on_list(meta_info, avg_list):
    unique_list=list(set(flatten(meta_info)))
    return [x for x in avg_list if x[0] in unique_list]


def set_default_TreeStyle(tree, draw_nodes):
    ts = TreeStyle()
    ts.mode = "c"
    ts.arc_start = -180
    ts.arc_span = 180
    ts.root_opening_factor = 1
    ts.show_branch_length = False
    ts.show_branch_support = True
    ts.force_topology = False
    ts.show_leaf_name = False
    ts.min_leaf_separation=10
    ts.root_opening_factor=1
    ts.complete_branch_lines_when_necessary=True


    return ts, tree


def various_trees_2(organism_names, average_join_var,save_folder):
    if not os.path.exists(save_folder):
        print("creating folder...")
        os.makedirs(save_folder)

    tax_g=["Super-Realm","Realm","Kingdom","Phylum","Class","Order","Family"]
    for x in range(0,len(tax_g)):
        save_folder2=save_folder+"/"+tax_g[x]
        if not os.path.exists(save_folder2):
            print("creating folder for trees in",tax_g[x],"...")
            os.makedirs(save_folder2)
        unique_list=list(set([m[x] for m in organism_names ]))
        pre_tree_list= [m[x:] for m in organism_names]

        for root in unique_list:
            if "incertae_sedis" not in root:
                savefolder=save_folder2+'/'+root
                tree_lst=[lst for lst in pre_tree_list if lst[0]==root]
                avg_list_used = filter_based_on_list(tree_lst,average_join_var)
                create_original_tree(tree_lst, avg_list_used, root, savefolder, True, "NC")


def various_trees(meta_information_list,avg_list, root, name,sci,save_labels,save_folder):
    if not os.path.exists(save_folder):
        print("creating folder...")
        os.makedirs(save_folder)

    tax_g=["Super-Realm","Realm","Kingdom","Phylum","Class","Order","Family","Genus"]
    for x in range(1,len(meta_information_list[0])+1):
        met=[m[0:x] for m in meta_information_list]
        met=[m for m in met if "incertae_sedis" not in m[-1]]
        sv_name= save_folder+"/"+name+"_"+tax_g[x-1]
        avg_list_used = filter_based_on_list(met,avg_list)
        save_labels=name.split("_")[0]
        create_original_tree(met,avg_list_used, root,sv_name,sci,save_labels)


def newickify(node_to_children, root_node) -> str:
    visited_nodes = set()

    def newick_render_node(name, distance: float) -> str:
        if name in visited_nodes:
            print(name)
        assert name not in visited_nodes, "Error: The tree may not be circular!"

        if name not in node_to_children:
            # Leafs
            return F'{name}:{distance}'
        else:
            # Nodes
            visited_nodes.add(name)
            children = node_to_children[name]
            children_strings = [newick_render_node(child, children[child]) for child in children.keys()]
            children_strings = ",".join(children_strings)
            return F'({children_strings}){name}:{distance}'

    newick_string = newick_render_node(root_node, 0) + ';'

    # Ensure no entries in the dictionary are left unused.
    assert visited_nodes == set(node_to_children.keys()), "Error: some nodes aren't in the tree"

    if visited_nodes != set(node_to_children.keys()):
        print("Error: some nodes aren't in the tree")
        return newick_string, False
    else:
        return newick_string, True




def create_original_tree(meta_information_list, avg_list, root, name,sci,save_labels):

    save_string=name+".pdf"
    save_string_colorbar=name+"_colorbar.pdf"
    final_save=name+"_final"+".pdf"
    if sci:
        nc_val=[x[1] for x in avg_list]
    else:
        nc_val=[round(x[1],3) for x in avg_list]
    if not avg_list:
        avg_list=[[root,1.0],["V",0.0]]
    
    mx=max([x[1] for x in avg_list])
    mn=min([x[1] for x in avg_list])

    if mn == mx:
        mn=mn-0.001
        mx=mx+0.001
    if sci:
        mx=math.log(mx)
        if mn==0:
            mn=0.000001
        mn=math.log(mn)
    
    colorbar(mn, mx, save_labels, save_string_colorbar)
    leaf_val=[x[0] for x in avg_list]
    tree = dict()
    for virus_info in meta_information_list:
        for index in range(0,len(virus_info)):
            virus_info[index] = virus_info[index].replace(";", "").replace(":", "")
            if virus_info[index] not in tree.keys() and index +1 < len(virus_info):
                tree[virus_info[index]] = {virus_info[index + 1]:1}
                if index < len(virus_info) and index>0:
                    d1 = {virus_info[index]: 1}
                    tree[virus_info[index-1]].update(d1)
            else:
                if index!=0:
                    d1 = {virus_info[index]: 1}
                    tree[virus_info[index-1]].update(d1)

    newick_tree, const_bool = newickify(tree, root_node=root)

    if const_bool:
        t = Tree(newick_tree, quoted_node_names=True, format=1)
        ts, t = set_default_TreeStyle(t, False)
        t.set_style(ts)
        
        count=0
        for name,value in zip(leaf_val,nc_val):          
            matching_nodes = t.search_nodes(name=name)         
            if matching_nodes:
                dst=t.get_distance(root,matching_nodes[0])
                if sci:
                    if value==0:
                        rgb_color=rgb2(mn, mx, math.log(0.000001))
                        rgb_color=('#%02x%02x%02x' % rgb_color)
                        complexity = TextFace(value,fgcolor=rgb_color, fsize=200,bold=True)
                        change_tree_branch(matching_nodes, rgb_color, dst)
                    else:
                        rgb_color=rgb2(mn, mx, math.log(value))
                        rgb_color=('#%02x%02x%02x' % rgb_color)
                        complexity = TextFace("{:.2e}".format(value),fgcolor=rgb_color, fsize=200,bold=True)
                        change_tree_branch(matching_nodes, rgb_color, dst)
                else:
                    rgb_color=rgb2(mn, mx, value)
                    rgb_color=('#%02x%02x%02x' % rgb_color)
                    complexity = TextFace(value,fgcolor=rgb_color, fsize=200,bold=True)
                    change_tree_branch(matching_nodes, rgb_color, dst)
                    
                virus_name = TextFace(matching_nodes[0].name, fgcolor=rgb_color, fsize=200,bold=True)
                # matching_nodes[0].add_face(face=complexity, column=1, position="branch-bottom")
                matching_nodes[0].add_face(face=virus_name, column=1, position="branch-top")
            else:
                print("ERROR->", avg_list[count])
            count+=1
        t.render(save_string,tree_style=ts,  dpi=1000,h=120000, w=120000,units="px")

    return const_bool


if __name__ == "__main__":    

    print(f"{bcolors.OKGREEN}Starting IR Analysis...{bcolors.ENDC}")

    #Metagenomic Information Paths
    organism_path="../VirusDB/ViralSeq_Org.info"
    genomic_type_path="../VirusDB/ViralSeq_Genome.info"
    
    #Features Paths
    NC_FILE="../reports/REPORT_COMPLEXITY_NC_OTHER_3"
    len_seq_path="../reports/REPORT_SEQ_LEN"
    GC_path="../reports/REPORT_SEQ_GC"
    IR_0="../reports/Report_NC_IR_OPTIMAL_0"
    IR_1="../reports/Report_NC_IR_OPTIMAL_1"
    IR_2="../reports/Report_NC_IR_OPTIMAL_2"
    

    

    ##Process meta information
    print(f"{bcolors.OKGREEN}Processing genomic meta information...{bcolors.ENDC}")
    rg_list = read_genomic_type_path(genomic_type_path)
    ro_list = read_organism_path(organism_path)
    ll = match_files(rg_list,ro_list)
    meta_info = process_meta_information(ll)
    meta_info = read_and_correct("../VirusDB/correct_taxa.txt", meta_info)
    tax_ign=read_to_list("../VirusDB/ignoretax.txt")
    meta_info=filter_from_ll(meta_info, tax_ign)
    organism_names = [x[3:-1] for x in meta_info]
    organism_names=filter_organism_list(organism_names)    
    meta_info=filter_meta_info(meta_info)



    new_tree=[]
    unique_list = process_organism_lists(organism_names)
    print("org:",len(organism_names))
    print("meta_info:",len(meta_info))
    for x,y in zip(organism_names, meta_info):
        if x:
            new_tree.append(y + [x[7]])
        else:
            new_tree.append(y +[""])
    

    ##Process Features
    print(f"{bcolors.OKGREEN}Processing Features...{bcolors.ENDC}")
    len_seq=read_file(len_seq_path) # Sequence Length
    gc_seq=read_file(GC_path) # GC-Content
    nc_file=nc_process_no_floor(NC_FILE) #NC from the best Compression Level
    best_nc_for_file_0 = nc_process_no_floor(IR_0) #Context model Compression
    best_nc_for_file_1 = nc_process_no_floor(IR_1) #Mixed Compression
    best_nc_for_file_2 = nc_process_no_floor(IR_2) #IR-based Compression

    # Filter outliers
    print(f"{bcolors.OKGREEN}Filtering Outliers...{bcolors.ENDC}")
    len_seq, gc_seq, nc_file, best_nc_for_file_0, best_nc_for_file_1, best_nc_for_file_2 = filter_outliers(len_seq, gc_seq, nc_file,best_nc_for_file_0, best_nc_for_file_1,best_nc_for_file_2)
    print("----------------------")

    #Diff between NC(IR0)-NC(IR1)
    diff_nc = nc_diff(best_nc_for_file_0, best_nc_for_file_1)
    

    # Removing Features of Incomplete Taxonomic Metadata.
    nc_taxa,_ = join_nc_taxa(nc_file, new_tree)
    nc_taxa_ir2,_ = join_nc_taxa(best_nc_for_file_2, new_tree)
    diff_nc_taxa,_ = join_nc_taxa(diff_nc, new_tree)

    nc_taxa_list = [[a[1]] + a[3:-1] for a in nc_taxa]
    nc_taxa_ir2_list = [[1-a[1]] + a[3:-1] for a in nc_taxa_ir2 if (1-a[1])>0]
    diff_nc_taxa_list = [[a[1]] + a[3:-1] for a in diff_nc_taxa if a[1]>0]
    nc_taxa_process = [[a[1]] + a[3:-1] for a in nc_taxa]

    ##Phylogenetic Trees Leafs Ending in Different Taxonomic Groups.
    print(f"{bcolors.OKGREEN}Creating All Phylogenetic Trees...{bcolors.ENDC}")
    nc_avg_list = tree_average(nc_taxa_process)
    nc_ir2_avg_list = tree_average(nc_taxa_ir2_list)
    diff_nc_avg_list = tree_average(diff_nc_taxa_list)
    various_trees(organism_names, nc_avg_list, "Viruses", "nc_tree", False,"NC","../plots/phylo_trees")
    various_trees(organism_names, nc_ir2_avg_list, "Viruses", "nc_ir2_tree", False,"IR0","../plots/phylo_trees") #maybe invert scale
    various_trees(organism_names, diff_nc_avg_list, "Viruses", "diff_nc_tree",False,"DIFF","../plots/phylo_trees")
    ##Website Group-specific Phylogenetic Trees
    various_trees_2(organism_names, nc_avg_list,"../plots/trees_2")
    print(f"{bcolors.OKGREEN}IR Analysis Successfully Complete...{bcolors.ENDC}")