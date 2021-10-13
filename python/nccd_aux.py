#!python
#!/usr/bin/env python
#Python script:
import sys
import os

def create_folder_list(path,savepath):
    folder_list=[]
    for subdir, dirs, _ in os.walk(path):
        for d in dirs:
            folder_list.append(os.path.join(path, d))
    file_list=[]
    for d in folder_list:
        onlyfiles = [os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
        
        filesize_list = [os.path.getsize(f) for f in onlyfiles]
        index = filesize_list.index(min(filesize_list))
        file_list.append(onlyfiles[index])
    file_nccd_combination=[]
    for i in range(0,len(file_list)):
        for j in range(i+1, len(file_list)):
            file_nccd_combination.append([file_list[i], file_list[j]])
    
    save_to_file(file_nccd_combination, savepath)        
    
def save_to_file(list_of_lists, path):
    with open(path, 'w') as f:
        for _list in list_of_lists:
            list_str = "\t".join([str(a) for a in _list])
            f.write(list_str + '\n')

if __name__ == "__main__":
    path="../VirusDB/Virus_by_taxid/"
    fl_l= create_folder_list(path,"../VirusDB/Virus_NCCD_process_list")
