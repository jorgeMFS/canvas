#!/bin/bash
#
MAKE_TABLE=0;
MATCH_TABLE=0;
MATCH_AND_MERGE_SEQ_FROM_TABLE=0;
CREATE_DB=1;

## Sequence Split
mkdir -p ../VirusDB/seqs_no_header/;
mkdir -p ../VirusDB/SeqSplit/;

gto_fasta_rand_extra_chars < ../VirusDB/sq.fasta> ../VirusDB/CG_VDB.fasta;
gto_fasta_split_reads -l "../VirusDB/SeqSplit" < ../VirusDB/CG_VDB.fasta;

rm ../VirusDB/CG_VDB.fasta;

cat "../VirusDB/SeqSplit/out2236.fasta" "../VirusDB/SeqSplit/out2237.fasta" "../VirusDB/SeqSplit/out2238.fasta" "../VirusDB/SeqSplit/out2239.fasta" "../VirusDB/SeqSplit/out2240.fasta" > "../VirusDB/SeqSplit/out2236.fasta"
rm "../VirusDB/SeqSplit/out2237.fasta" "../VirusDB/SeqSplit/out2238.fasta" "../VirusDB/SeqSplit/out2239.fasta" "../VirusDB/SeqSplit/out2240.fasta"

for file in ../VirusDB/SeqSplit/*.fasta
        do
        file_name="${file##*/}"
        gto_fasta_to_seq < $file > "../VirusDB/seqs_no_header/"$file_name
done

### Get id 

if [ "$MAKE_TABLE" -eq "1" ];
    then
    mkdir -p ../VirusDB/TaxSQ
    # rm ../VirusDB/Viral_Seq.info;
    for file in ../VirusDB/SeqSplit/*.fasta
        do
            filename="${file%.*}"
            fil="$(basename -- $filename)"     

            if !( cat ../VirusDB/Viral_Seq.info | grep -q $fil.fasta);then  
                GenBank_Accn=$(head -n 1 $file | awk '{print $1}'| tr -d '>')
                Geno_info=$(head -n 1 $file | awk -F "|" '{print $2,"\t"$4,"\t"$5,"\t"$6,"\t"$7}');
                taxinfo=$(esearch -db nuccore -query "$GenBank_Accn [ACCN]" | efetch -format docsum |xtract -pattern DocumentSummary -element TaxId) 
                #| epost -db taxonomy |   efetch -format docsum |   xtract -pattern DocumentSummary -element TaxId, ScientificName)
                echo -e "$fil.fasta\t${taxinfo}\t${Geno_info}" >> ../VirusDB/Viral_Seq.info;
            fi
    done
fi


if [ "$CREATE_DB" -eq "1" ];
    then
    python3.6 ../python/merge_sequences.py
fi