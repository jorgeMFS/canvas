#!python
#!/usr/bin/env python
#Python script:

import re
import sys
import os

class sequence():
    def __init__(self, line):
        self.filename = int(str(line[0]).split(".")[0].replace('out',''))
        self.taxid = line[1]
        self.info = line[2]
        self.name = line[3]
        self.setid = line[4]
        self.host = line[5]
        self.country = line[6]
        self.indicator=""

    def __str__(self):
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (self.filename, self.taxid, self.info, self.name,self.setid,self.host,self.country,self.indicator)
    
    def to_list(self):
        return [self.filename,
                self.taxid,
                self.info,
                self.name,
                self.setid,
                self.host,
                self.country,
                self.indicator]
    
    def add_to_seq(self,ind):
        self.indicator=ind

def taxid_filter(taxid, seqlist):
    same_virus=[]
    for virus in seqlist:
        if taxid == virus.taxid:
            same_virus.append(virus)
    return same_virus

def country_filter(country, seqlist):
    same_virus=[]
    for virus in seqlist:
        if country == virus.country:
            same_virus.append(virus)
    return same_virus

def host_filter(host, seqlist):
    same_virus=[]
    for virus in seqlist:
        if host == virus.host:
            same_virus.append(virus)
    return same_virus

### concatenate files
def conc_files(path, list_files):
    for l in list_files:
        conc_list=l[0]
        tax=l[1][0]
        conc_files_len=len(conc_list)
        filename = str(conc_list[0])
        filename = "out" + filename +"-"+ str(conc_files_len) + ".fasta"
        savepath = path+"/"+str(tax)+"/"
        create_path(savepath)
        savefile = savepath + filename
        with open(savefile, 'w') as outfile:
            for fname in conc_list:
                with open("../VirusDB/seqs_no_header/"+"out" +str(fname)+".fasta") as infile:
                    for line in infile:
                        outfile.write(line)

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

## Retrive concatenating factors:
def remove_wordset(entry_list):
    output_list=[]
    for entry in entry_list:
        entry = entry.replace(',', '').replace(':',"").replace("_","").replace("dsRNA","").replace("dsDNA","").replace("RNA","").replace("DNA","")
        word_set = {'segment','rna','dna','dsdna','dsrna','seg'}
        resultwords  = [word for word in re.split("\W+",entry) if word.lower() not in word_set]
        resultwords = list(filter(None, resultwords))    
        output_list.append( ['.'.join(resultwords)])

    output_list = [item for sublist in output_list for item in sublist]
    if len(output_list) == len(entry_list):
        return output_list
    else:
        print("ERROR")
        print(len(output_list),len(entry_list))

def get_unique_ind(virus_of_same_tax):
    unique_ind = {seq.indicator for seq in virus_of_same_tax}
    unique_ind = sorted_nicely(unique_ind)
    virus_of_same_tax = [seq.to_list() for seq in virus_of_same_tax]
    info =[last for *_, last in virus_of_same_tax]
    count_values = [[uid, info.count(uid)] for uid in unique_ind]
    # [print(a) for a in count_values]
    unique_elements = sum(i[1] > 1 for i in count_values)<1
    return count_values, unique_elements

def separate_lists(list_of_lists):
    remainder=[]
    merger=[]
    for l in list_of_lists:
        if len(l)==1:
            remainder.append(l[0])
        else:
            merger.append(l)
    return merger, remainder

def filter_by_set_id(seq_list):
    unique_setid = {seq.setid for seq in seq_list}
    if list(unique_setid):
        seq_set_list=[]
        for setid in unique_setid:
            setid_list=[]
            for seq in seq_list:
                if seq.setid == setid:
                    setid_list.append(seq)
            seq_set_list.append(setid_list)
        
        seq_set_list, not_good = separate_ll_setid(seq_set_list)
        can_be_joined = len(seq_set_list)+len(not_good)<len(seq_list)
    else:
        return list(seq_list),list(),False
    return seq_set_list,not_good ,can_be_joined   

def separate_ll_setid(ll):
    no_setid_list=[]
    grouped_ll=[]
    for l in ll:
        if not l[0].setid:
            [no_setid_list.append(x) for x in l]
        else:
            grouped_ll.append(l)
    return grouped_ll,no_setid_list


def sorted_nicely( l ):
    """ Sorts the given iterable in the alphanumeric form.
 
    Required arguments:
    l -- The iterable to be sorted.
    """

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
   
    return sorted(l, key = alphanum_key)

def sort_by_indicator(list_virus):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list_virus, key=lambda x: alphanum_key(x.indicator), reverse=False)

def group_by_seg(viral_list):
    grouped_ll=[]
    for virus_seq in viral_list:
        a=False
        for group_seq in grouped_ll:
            ind= virus_seq.indicator
            g_ind=get_indicators(group_seq)
            if ind not in g_ind:
                group_seq.append(virus_seq)
                a=True
                break
        if not a:
            grouped_ll.append([virus_seq])
    
    return grouped_ll

def get_indicators(seq_list):
    a= [seq.indicator for seq in seq_list]
    return a
def order_by_filenumber(virus_list):
    virus_list.sort(key=lambda x: x.filename, reverse=False)
    return virus_list

def get_info_list(ll):
    return [seg.info for seg in ll]
        
def get_to_format_list(ll):
    filenames_to_merge=[]
    for l in ll:
        filenames=[x.filename for x in l]
        taxid=list(set([x.taxid for x in l]))
        filenames_to_merge.append([filenames,taxid])
    return filenames_to_merge

def rest_to_list(rest):
    rest_file = []
    for seq in rest:
        a = [[str(seq.filename)],[seq.taxid]]
        rest_file.append(a)
    return rest_file

if __name__ == "__main__":
    with open( "../VirusDB/Viral_Seq.info", 'r') as file:
        data = file.read()
    data = data.splitlines()

    sq_list=[]
    sql=[]
    for line in data:
        line = line.split('\t')
        line = [a.strip() for a in line]
        if len(line)<7:
            l = [""] * (7-len(line))
            line+=l
        sq = sequence(line)
        sq_list.append(sq)
        sql.append(sq.to_list())

    sql = sorted(sql, key=lambda x: x[0])
    sql = [sequence(line) for line in sql]
    #####Unique
    taxids = sorted(list(set([seq.taxid for seq in sq_list])))
    hosts = sorted(list(set([seq.host for seq in sq_list])))
    countries = sorted(list(set([seq.country for seq in sq_list])))
    virus_id =  sorted(list(set([seq.setid for seq in sq_list]))) 
    virus_name = sorted(list(set([seq.name for seq in sq_list])))
    virus_info = sorted(list(set([seq.info for seq in sq_list])))
    filename = sorted(list(set([seq.filename for seq in sq_list])))




    ### Split
    complete_cds=[]
    dsRNA_n_list=[]
    RNA_n_list=[]
    DNA_l_list=[]
    DNA_n_list=[]
    segment_n_list=[]
    segment_sml_list=[]
    segment_letters_list=[]
    other_seg =[]
    seg_list=[]
    all_other=[]
    greek_list=[]
    segment_string_sml_list=[]
    
    dsRNA_n_info =[]
    RNA_n_info=[]
    dna_l_info=[]
    dna_n_info=[]
    segment_n_info=[]
    segment_sml_info=[]
    segment_string_sml_info=[]
    segment_letters_info=[]
    greek_info=[]
    seg_info=[]
    segment_c_info=[]
    segment_c_list=[]
    DNA_string_sml_info=[]
    DNA_string_sml_list=[]
    RNA_string_sml_info=[]
    RNA_string_sml_list=[]
    seg_rna_info=[]
    seg_rna=[]
    alt_seg=[]
    alt_seg_info=[]
    for viral_seq in sql:
        if re.findall(r"(dsRNA\s?\d{1,2}[,|\s|a|b])", viral_seq.info):
            dsRNA_n_list.append(viral_seq)
            dsRNA_n_info.append(re.findall(r"(dsRNA\s?\d{1,2}[,|\s|a|b])", viral_seq.info)[0])
        
        elif  re.findall(r"(\sRNA[-|_]\d{1,2}\s*|\sRNA\s?\d{1,2})", viral_seq.info):
            RNA_n_list.append(viral_seq)
            RNA_n_info.append(re.findall(r"(\sRNA[-|_]\d{1,2}\s*|\sRNA\s?\d{1,2})", viral_seq.info)[0])

        elif re.findall(r"(?:segment)\sDNA-\w{1}\d{0,2}.\d{1,2}", viral_seq.info):
            DNA_n_list.append(viral_seq)
            dna_n_info.append(re.findall(r"(?:segment)\sDNA-\w{1}\d{0,2}.\d{1,2}", viral_seq.info)[0])

        elif re.findall(r"(\sDNA[-|_][A-Z]\d{0,2}\s*)", viral_seq.info):
            DNA_l_list.append(viral_seq)
            dna_l_info.append(re.findall(r"(\sDNA[-|_][A-Z]\d{0,2}\s*)", viral_seq.info)[0])
        
        elif re.findall(r"(\sDNA\s?[A-Z]\s*)", viral_seq.info):
            DNA_l_list.append(viral_seq)
            dna_l_info.append(re.findall(r"(\sDNA\s?[A-Z]\s*)", viral_seq.info)[0])
        
        elif re.findall(r"(\sDNA[-|_]\d{1,2}\s*|\sDNA\s?\d{1,2}\s*)", viral_seq.info):
            DNA_n_list.append(viral_seq)
            dna_n_info.append(re.findall(r"(\sDNA[-|_]\d{1,2}\s*|\sDNA\s?\d{1,2}\s*)", viral_seq.info)[0])
        
        elif re.findall(r"((segment\s?\d{1,2})|(segment:\s\d{1,2}))", viral_seq.info):
            segment_n_list.append(viral_seq)
            segment_n_info.append(re.findall(r"((segment\s?\d{1,2})|(segment:\s\d{1,2}))", viral_seq.info)[0])

        elif re.findall(r"(segment:\s[S,L,M]\d{0,1})", viral_seq.info):
            segment_sml_list.append(viral_seq)
            segment_sml_info.append(re.findall(r"(segment:\s[S,L,M]\d{0,1})", viral_seq.info))
        
        elif re.findall(r"(segment\s[S,L,M]\d{0,2}\s?)", viral_seq.info):
            segment_sml_list.append(viral_seq)
            segment_sml_info.append(re.findall(r"(segment\s[S,L,M]\d{0,2}\s?)", viral_seq.info))
   
        elif re.findall(r"(\s[S,L,M]\ssegment)", viral_seq.info):
            segment_sml_list.append(viral_seq)
            segment_sml_info.append(re.findall(r"(\s[S,L,M]\ssegment)", viral_seq.info))
    
        elif re.findall(r"(segment\sc\d{1,2})", viral_seq.info):
            segment_c_list.append(viral_seq)
            segment_c_info.append(re.findall(r"(segment\sc\d{1,2})", viral_seq.info)[0])

        elif re.findall(r"((segment\s(small|middle|medium|large))|((small|middle|medium|large)\ssegment))", viral_seq.info):
            segment_string_sml_list.append(viral_seq)
            segment_string_sml_info.append(re.findall(r"((segment\s(small|middle|medium|large))|((small|medium|middle|large)\ssegment))", viral_seq.info)[0][0])
        elif re.findall(r"((small|middle|medium|large)\s?DNA)",viral_seq.info):
            DNA_string_sml_list.append(viral_seq)
            DNA_string_sml_info.append(re.findall(r"((small|middle|medium|large)\s?DNA)",viral_seq.info)[0][0])
        

        elif re.findall(r"((segment|DNA|RNA)\s(alpha|beta|gamma))|((segment|DNA|RNA)-(alpha|beta|gamma))", viral_seq.info):
            greek_list.append(viral_seq)
            greek_info.append(re.findall(r"((segment|DNA|RNA)\s(alpha|beta|gamma))|((segment|DNA|RNA)-(alpha|beta|gamma))", viral_seq.info)[0])
    
        elif re.findall(r"(Seg\s\d{0,1}\s?)", viral_seq.info):
            seg_list.append(viral_seq)
            seg_info.append(re.findall(r"(Seg\s\d{0,1}\s?)", viral_seq.info))

        elif re.findall(r"\ssegment\sRNA-\w{1,3}", viral_seq.info):
            seg_rna.append(viral_seq)
            seg_rna_info.append(re.findall(r"\ssegment\sRNA-\w{1,3}", viral_seq.info)[0])

        elif re.findall(r"\ssegment\sRNA\s\w{1,3}", viral_seq.info):
            seg_rna.append(viral_seq)
            seg_rna_info.append(re.findall(r"\ssegment\sRNA\s\w{1,3}", viral_seq.info)[0])

        elif re.findall(r"(?:segment hypothetical)\s.*\d{1,1}", viral_seq.info):
            alt_seg.append(viral_seq)
            alt_seg_info.append(re.findall(r"(?:segment hypothetical)\s.*\d{1,1}", viral_seq.info)[0])
        
        elif re.findall(r"(?:segment unknown)\s.*\d{1,1}", viral_seq.info):
            alt_seg.append(viral_seq)
            alt_seg_info.append(re.findall(r"(?:segment unknown)\s.*\d{1,1}", viral_seq.info)[0])
        
        elif re.findall(r"(?:segment)\sCircle\d{1,2}", viral_seq.info):
            alt_seg.append(viral_seq)
            alt_seg_info.append(re.findall(r"(?:segment)\sCircle\d{1,2}", viral_seq.info)[0])
        elif re.findall(r"(?:segment)\sCiV\d{1,2}.\d{1,2}", viral_seq.info):
            alt_seg.append(viral_seq)
            alt_seg_info.append(re.findall(r"(?:segment)\sCiV\d{1,2}.\d{1,2}", viral_seq.info)[0])
        elif re.findall(r"(?:segment)\s\w{1,3}\d{1,2}", viral_seq.info):
            alt_seg.append(viral_seq)
            alt_seg_info.append(re.findall(r"(?:segment)\s\w{1,3}\d{1,2}", viral_seq.info)[0])
        elif re.findall(r"(?:segment)\s\w{1,4}-\w{1,2}\d{1,2}", viral_seq.info):
            alt_seg.append(viral_seq)
            alt_seg_info.append(re.findall(r"(?:segment)\s\w{1,4}-\w{1,2}\d{1,2}", viral_seq.info)[0])
        elif re.findall(r"(?:segment)\s:\s\w{1,2}", viral_seq.info):
            alt_seg.append(viral_seq)
            alt_seg_info.append(re.findall(r"(?:segment)\s:\s\w{1,2}", viral_seq.info)[0])
        elif re.findall(r"(segment\s\w{0,2}\d{0,2})", viral_seq.info):
            segment_letters_list.append(viral_seq)
            segment_letters_info.append( re.findall(r"(segment\s\w{0,2}\d{0,2})", viral_seq.info)[0])
        
        else:
            all_other.append(viral_seq)
    
    segment_sml_info = [tuple(filter(None, tp))[0] for tp in segment_sml_info]
    greek_info = [tuple(filter(None, tp))[0] for tp in greek_info]
    segment_n_info = [tuple(filter(None, tp))[0] for tp in segment_n_info]
    
    seq_to_concatenate = alt_seg+seg_rna+dsRNA_n_list+RNA_n_list+DNA_l_list+DNA_n_list+segment_n_list+segment_sml_list+segment_c_list+segment_string_sml_list+DNA_string_sml_list+segment_letters_list+greek_list+seg_list
    seq_to_concatenate_info = alt_seg_info+seg_rna_info+dsRNA_n_info+RNA_n_info+dna_l_info+dna_n_info+segment_n_info+segment_sml_info+segment_c_info+segment_string_sml_info+DNA_string_sml_info+segment_letters_info+greek_info+seg_info
    seq_to_concatenate_info = remove_wordset(seq_to_concatenate_info)
    [seq.add_to_seq(ind) for seq, ind in zip(seq_to_concatenate, seq_to_concatenate_info)]
    incomplete_seq=list()
    merger_list=[]
    incomplete_seq=[]
    for taxid in taxids:

        tax = taxid_filter(taxid, seq_to_concatenate)
        if len(tax)>1:
            cnt, unique = get_unique_ind(tax)
            if unique:
                merger_list.append(tax)

            elif(len(cnt)==1):
                incomplete_seq.append(tax)
            else:
                list_set, no_setid_group, join = filter_by_set_id(tax)
                if join:
                    grouped_l, remain_l =  separate_lists(list_set)
                    [merger_list.append(viral_g) for viral_g in grouped_l]
                    
                    no_setid_group = no_setid_group + remain_l
                    if no_setid_group:
                        no_setid_group = order_by_filenumber(no_setid_group)
                        grouped_list = group_by_seg(no_setid_group)
                        grouped_l,remain_l =  separate_lists(grouped_list)
                        [merger_list.append(viral_g) for viral_g in grouped_l]
                        incomplete_seq.append(remain_l)
                else:
                    tax = order_by_filenumber(tax)
                    grouped_list = group_by_seg(tax)
                    grouped_l,remain_l =  separate_lists(grouped_list)
                    [merger_list.append(viral_g) for viral_g in grouped_l]
                    incomplete_seq.append(remain_l)
        else:
            incomplete_seq.append(tax)
    total_list=[]
    
    incomplete_seq = list(filter(None, incomplete_seq))
    for m in merger_list:
        total_list.append(sort_by_indicator(m))
    merger_list=total_list
    
    incomplete_seq = [item for sublist in incomplete_seq for item in sublist]
    files_merge = get_to_format_list(merger_list)
    incomplete_seq_files = rest_to_list(incomplete_seq)
    
    t=get_info_list(seq_to_concatenate)
    non_concat=[]
    for seq in sql:
        if seq.info not in t:
            non_concat.append(seq)
    
    non_concat_files = rest_to_list(non_concat)
    total_files = files_merge + incomplete_seq_files + non_concat_files 
    conc_files("../VirusDB/Virus_by_taxid", total_files)
        