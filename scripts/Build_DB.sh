#!/bin/bash
#
DIVIDE=0
MAKE_TABLE=0;
CREATE_DB=1;
## Sequence Split
mkdir -p ../VirusDB/seqs_no_header/;
mkdir -p ../VirusDB/seqs_header/;

mkdir -p ../VirusDB/SeqSplit/;


# cat "../VirusDB/SeqSplit/out2236.fasta" "../VirusDB/SeqSplit/out2237.fasta" "../VirusDB/SeqSplit/out2238.fasta" "../VirusDB/SeqSplit/out2239.fasta" "../VirusDB/SeqSplit/out2240.fasta" > "../VirusDB/SeqSplit/out2236.fasta"
# rm "../VirusDB/SeqSplit/out2237.fasta" "../VirusDB/SeqSplit/out2238.fasta" "../VirusDB/SeqSplit/out2239.fasta" "../VirusDB/SeqSplit/out2240.fasta"
if [ "$DIVIDE" -eq "1" ];
    then
    gto_fasta_split_reads -l "../VirusDB/SeqSplit" < ../VirusDB/seq_ref.fasta;
    for file in ../VirusDB/SeqSplit/*.fasta
            do
            file_name="${file##*/}";
            head -n 1 $file > HEADER;
            tail -n +2 $file > FASTA
            if grep -q "N" FASTA; then
                gto_fasta_rand_extra_chars < $file > A;
                tail -n +2 A > FASTA
            fi
        
            header_l=$(wc -l HEADER | awk '{print $1}');
            fasta_l=$(wc -l FASTA |  awk '{print $1}');
            file_l=$(wc -l $file  |  awk '{print $1}');
            cat HEADER FASTA > FILE;
            sum=$(( $header_l + $fasta_l ))
            if [ "$sum" -eq "$file_l" ]; then
                cat FILE > "../VirusDB/seqs_header/""${file_name}"
                gto_fasta_to_seq < FILE > "../VirusDB/seqs_no_header/"${file_name}
            else
                cat HEADER FASTA
                echo "-------------"
                cat "$file"
                echo "-------------"
                cat A;
                echo "-------------"
                echo "wc sum : $sum, wc file: $ $file_l"            
                echo "ERROR";
                exit;
            fi 
                
    done
    rm A HEADER FASTA FILE
fi

### Get id 

if [ "$MAKE_TABLE" -eq "1" ];
    then
    touch ../VirusDB/Viral_Seq.info
    # rm ../VirusDB/Viral_Seq.info;
    for file in ../VirusDB/SeqSplit/*.fasta
        do
            filename="${file%.*}"
            fil="$(basename -- "$filename")"     

            if ! ( < ../VirusDB/Viral_Seq.info grep -q "$fil".fasta);then  
                GenBank_Accn=$(head -n 1 "$file" | awk '{print $1}'| tr -d '>')
                Geno_info=$(head -n 1 "$file" | awk -F "|" '{print $2,"\t"$4,"\t"$5,"\t"$6,"\t"$7}');
                echo "$GenBank_Accn"

                if grep -q "$GenBank_Accn"  "../VirusDB/ViralRefSeq.catalog"; then
                    taxinfo=$(grep "$GenBank_Accn"  "../VirusDB/ViralRefSeq.catalog" |awk 'NR==1{print $1}')
                    echo -e "$fil.fasta\t${taxinfo}\t${Geno_info}" >> ../VirusDB/Viral_Seq.info;
                else
                    taxinfo=$(grep "$GenBank_Accn"  "../VirusDB/ViralRefSeq.catalog" |awk 'NR==1{print $1}')
                    echo "$taxinfo";
                    echo -e "$fil.fasta\t${taxinfo}\t${Geno_info}" >> ../VirusDB/Viral_Seq.info;
                fi
               
            fi
    done
fi


if [ "$CREATE_DB" -eq "1" ];
    then
    python3.6 ../python/merge_sequences.py
fi
rm ../VirusDB/Virus_by_taxid/out*
