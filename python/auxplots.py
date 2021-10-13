    
def filter_and_plot_measure_vs_len(var_to_filter, filtername, dataframe, var1, var2, group_var, title, savepath):
    df_filter = dataframe[(dataframe[var_to_filter] == filtername)]
    df_measure = df_filter.sort_values([var1, var2], ascending=[True, True])
    plt.clf()
    ax = sns.boxplot(x=group_var, y=var2, data=df_measure, palette="Set3", showfliers = False)
    ax2 = plt.twinx()
    ax = sns.lineplot(x=group_var, y=var1,marker="o", data=df_measure,markers=True, palette="Set3",sizes=(.05, 0.5))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.tick_params(labelrotation=45)
    ax.set_title(title)
    ax.set_yscale('log')
    plt.savefig(savepath)

def plot_avg_process(merged_info):

    info = [x[7:-1] for x in merged_info]
    unique_elements = list(set([item for sublist in info for item in sublist]))
    unique_elements = list(filter(None, unique_elements))
    unique_elem_metrics=[]
    all_elem_metrics=[]
    bs=[]
    for elem in unique_elements:
        matching = [lst for lst in merged_info if elem in lst] 
        index = matching[0].index(elem)
        values=[]
        
        for i in range(1,7):
            lst =[x[i] for x in merged_info] 
            avg = sum(lst)/len(lst) if lst else 1
            values.append(avg)
        if index==7:
            s="Genome Type"
        else:
            s=matching[0][index-1]

        for l in matching:
            val = [s] + [elem] + l[1:7]
            all_elem_metrics.append(val)
            v1 = [s] + [elem] + [l[1]] + [l[4]] + ["IR 0"] 
            v2 = [s] + [elem] + [l[1]] + [l[5]] + ["IR 1"]
            v3 = [s] + [elem] + [l[1]] + [l[6]] + ["IR 2"]
            bs.append(v1)
            bs.append(v2)
            bs.append(v3)

        line = [s] + [elem] + values
        unique_elem_metrics.append(line)

    return unique_elem_metrics, all_elem_metrics, bs


def filter_by_human(organism_complete_list):
    hosts = list(set([x[-1] for x in organism_complete_list]))
    hosts.sort()
    homo_sapiens_alies_list=["Homo sapiens", "human", "human CSF",
                "human blood from multiple sclerosis patient",
                "human dermatitis",
                "human lung biopsy",
                "human sera",
                "human serum",
                "human serum with hepatic dysfunction, without virus infection of HBV,HCV etc"]

    homo_sapiens_alies_list = [h.lower() for h in homo_sapiens_alies_list]
    human_ls=[]
    for organism in organism_complete_list:
        if organism[-1].lower() in homo_sapiens_alies_list:
            organism[-1]="Homo sapiens"
            human_ls.append(organism)
    
    return human_ls
        
def unify_hosts(hosts):
    hosts_list = list(set([item for sublist in hosts for item in sublist]))
    country_list = read_to_list("../aux/countries.txt")
    tx_ign_list = read_to_list("../aux/ign_host.txt")

    
    eprint(len(hosts_list))
    for cnt in country_list:
        hosts_list = [ hst for hst in hosts_list if cnt.lower() not in hst.lower()]
    eprint(len(hosts_list))
    for cnt in tx_ign_list:
        hosts_list = [ hst for hst in hosts_list if cnt.lower() != hst.lower()]
    hosts_list.sort()
    for x in hosts_list:
        print(x)

def merge_pdfs(pdf1,pdf2,final_save):

    # PDF1
    input1 = PdfFileReader(open(pdf1, 'rb'))
    page1 = input1.getPage(0)

    # PDF2
    input2 = PdfFileReader(open(pdf2, 'rb'))
    page2 = input2.getPage(0)
    page2.scaleBy(4)
    # Merge
    page2.mergePage(page1)

    # Output
    output = PdfFileWriter()
    output.addPage(page1)
    outputStream = open(final_save, "wb")
    output.write(outputStream)
    outputStream.close()
    

def cut_pdf(pdf1,final_save):

    # PDF1
    input1 = PdfFileReader(open(pdf1, 'rb'))
    page1 = input1.getPage(0)
    (w, h) = page1.mediaBox.lowerRight
    height = int(input1.getPage(0).mediaBox[2])
    cut_size = int(input1.getPage(0).mediaBox[3])/2
    page1.cropBox.lowerRight = (height,cut_size)
    
    output = PdfFileWriter()
    output.addPage(page1)
    outputStream = open(final_save, "wb")
    output.write(outputStream)
    outputStream.close()
    os.remove(pdf1)
    os.rename(final_save, pdf1)



     ###########
if __name__ == "__main__": 
    filter_and_plot_measure_vs_len("Genome_Type", "dsDNA", df, "Sequence_Length", "Normalized_Compression", "Group", "dsDNA", "../plots/dsDNA.pdf")
    ###########
    df_dsdna = df[(df["Genome_Type"] == "dsDNA")]
    df_ssdna = df[(df["Genome_Type"] == "ssDNA")]
    df_dsrna = df[(df["Genome_Type"] == "dsRNA")]
    df_ssrnan = df[(df["Genome_Type"] == "ssRNA-")]
    df_ssrnap = df[(df["Genome_Type"] == "ssRNA+")]
    df_rt = df[(df["Genome_Type"] == "RT")]
    df_crna = df[(df["Genome_Type"] == "cRNA")]

    df_nc = df_dsdna.sort_values(['Sequence_Length', 'Normalized_Compression'], ascending=[True, True])
    plt.clf()
    ax = sns.boxplot(x="Group", y="Normalized_Compression", data=df_nc, palette="Set3", showfliers = False)
    ax2 = plt.twinx()
    ax = sns.lineplot(x="Group", y="Sequence_Length",marker="o", data=df_nc,markers=True, palette="Set3",sizes=(.05, 0.5))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax.tick_params(labelrotation=45)
    ax.set_title('dsDNA')
    ax.set_yscale('log')
    plt.savefig('../plots/dsDNA.pdf')
    
    ############
    #3d plot of NC vs len
    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    fx =[x for x in range(1,len(average_dataframe["Genome Type"])+1)]
    fy =[log(avg[4]) for avg in avg_genome] #average_dataframe["seq_len"]
    fz = [avg[7] for avg in avg_genome] #average_dataframe["NC"]
    occurrence = [avg[-1] for avg in avg_genome]
    lgn = [avg[0] for avg in avg_genome]
    #avg_gen["Genome Type"]
    xerror = [0,0,0,0,0,0,0]
    yerror = [0,0,0,0,0,0,0] #avg_gen["sq_std"]  
    zerror = [avg[11] for avg in avg_genome]
    colors =['#4682b4','#deb887','#FFFF00','#adff2f','#ff6347','#3cb371','#FFA500']

    #plot errorbars
    for i in np.arange(0, len(fx)):
        print(lgn[i])
        ax.plot(fx[i], fy[i], fz[i], linestyle="None", marker="s",markerfacecolor=colors[i],mec=colors[i],label=lgn[i])
        ax.plot([fx[i]+xerror[i], fx[i]-xerror[i]], [fy[i], fy[i]], [fz[i], fz[i]], marker="_",markerfacecolor=colors[i],mec=colors[i],markeredgewidth=1.)
        ax.plot([fx[i], fx[i]], [fy[i]+yerror[i], fy[i]-yerror[i]], [fz[i], fz[i]], marker="_",color=colors[i],markerfacecolor=colors[i],mec=colors[i], markeredgewidth=1.)
        ax.plot([fx[i], fx[i]], [fy[i], fy[i]], [fz[i]+zerror[i], fz[i]-zerror[i]], marker="_",color=colors[i],markerfacecolor=colors[i],mec=colors[i], markeredgewidth=1.)
        ax.text(fx[i]+0.1, fy[i]+0.1, fz[i]+0.01,  '%s' % (str(occurrence[i])), size=9, zorder=1,color='k') 
        ax.legend(bbox_to_anchor=(1.04,1), loc="upper left",title= "Genomic Type")

    ax.set_xticklabels(lgn)
    #configure axes
    ax.set_xlim3d(1, 7)
    ax.set_ylim3d(6, 12) 
    ax.set_zlim3d(0.2, 0.45)
    ax.set_xlabel('Genomic Type')
    ax.set_ylabel('Log. of the Average \n Sequence Length')
    ax.set_zlabel('Normalized Complexity')
    plt.savefig('../plots/gen_nc_len.pdf')
    ##############