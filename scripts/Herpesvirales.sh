#!/bin/bash
#

# HV1 NC_001806 
# HV2 JN561323.2 
# HV3 X04370.1 
# HV4 DQ279927.1 
# HV5 NC_006273 
# HV6A NC_001664.4 
# HV6B NC_000898.1 
# HV7 NC_001716 
# HV8 AF148805.2

function GECO_COMPRESS(){
    rm ../reports/"$1";

    for file in  "../VirusDB/HHV/noheader/"*".fa"; do
    
        f="$(basename -- "$file")"
        name=$f
        name="${name%.*}"
        GeCo3 -v -tm 1:1:0:0:0.7/0:0:0 -tm 12:50:0:1:0.97/0:0:0.97 "$file" 1> report_stdout 2> report_stderr # IR 0
        BPS1=$(grep "Total bytes" report_stdout | awk '{ print $6; }');
        IR0=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
        GeCo3 -v -tm 1:1:1:0:0.7/0:0:0 -tm 12:50:1:1:0.97/0:0:0.97 "$file" 1> report_stdout 2> report_stderr # IR 1
        BPS1=$(grep "Total bytes" report_stdout | awk '{ print $6; }');
        IR1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
        GeCo3 -v -tm 1:1:2:0:0.7/0:0:0 -tm 12:50:2:1:0.97/0:0:0.97 "$file" 1> report_stdout 2> report_stderr # IR 2
        BPS1=$(grep "Total bytes" report_stdout | awk '{ print $6; }');
        IR2=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
        len_x=$(wc -m <"$file")
        echo -e "$name\t$len_x\t$IR0\t$IR1\t$IR2" >> ../reports/"$1"

        rm report_stdout report_stderr
    done
}



mkdir -p ../VirusDB/HHV/
mkdir -p ../VirusDB/HHV/noheader/

# HV1
efetch -db nucleotide -format fasta -id NC_001806 > ../VirusDB/HHV/HHV1.fa
# HV2
efetch -db nucleotide -format fasta -id JN561323.2 > ../VirusDB/HHV/HHV2.fa
# HV3
efetch -db nucleotide -format fasta -id X04370.1 > ../VirusDB/HHV/HHV3.fa
# HV4
efetch -db nucleotide -format fasta -id DQ279927.1 > ../VirusDB/HHV/HHV4.fa
# HV5
efetch -db nucleotide -format fasta -id NC_006273 > ../VirusDB/HHV/HHV5.fa
# HV6A
efetch -db nucleotide -format fasta -id NC_001664.4 > ../VirusDB/HHV/HHV6A.fa
# HV6B
efetch -db nucleotide -format fasta -id NC_000898.1 > ../VirusDB/HHV/HHV6B.fa
# HV7
efetch -db nucleotide -format fasta -id NC_001716  > ../VirusDB/HHV/HHV7.fa
# HV8
efetch -db nucleotide -format fasta -id AF148805.2 > ../VirusDB/HHV/HHV8.fa

for file in ../VirusDB/HHV/*.fa
        do
        file_name="${file##*/}";
        head -n 1 "$file" > HEADER;
        tail -n +2 "$file" > FASTA
        if grep -q "N" FASTA; then
            gto_fasta_rand_extra_chars < "$file" > A;
            tail -n +2 A > FASTA
        fi
    
        header_l=$(wc -l HEADER | awk '{print $1}');
        fasta_l=$(wc -l FASTA |  awk '{print $1}');
        file_l=$(wc -l $file  |  awk '{print $1}');
        cat HEADER FASTA > FILE;
        sum=$(( $header_l + $fasta_l ))
        if [ "$sum" -eq "$file_l" ]; then
            gto_fasta_to_seq < FILE > "../VirusDB/HHV/noheader/""${file_name}"
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
rm FILE FASTA HEADER A LLL.seq > /dev/null

GECO_COMPRESS REPORT_HHV
cd ../python || exit;
python3.6 hhv.py

