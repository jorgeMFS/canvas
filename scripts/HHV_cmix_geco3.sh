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

PATH1="../VirusDB/HHV_compressor_test/";
PATH2="../VirusDB/HHV_compressor_test/noheader/";
CMIXPATH="../cmix-19.1/";

function COMPRESSION(){
    rm ../reports/"$1";

    for file in  ${PATH2}*".fa"; do
    
        f="$(basename -- "$file")"
        name=$f
        name="${name%.*}"
        start=`date +%s.%N`
        ${CMIXPATH}cmix -c $file output.seq
        original=$(ls -la "$file" | awk '{ print $5;}');
        compressed=$(ls -la output.seq | awk '{ print $5;}');
        CMIX_NC=$(echo "scale=10; ($compressed * 8.0) / ($original*2.0)" | bc -l | awk '{printf "%f", $0}');
        end=`date +%s.%N`
        cmix_runtime=$( echo "$end - $start" | bc -l )
        start=`date +%s.%N`
        GeCo3 -v -tm 1:1:1:0:0.7/0:0:0 -tm 12:50:1:1:0.97/0:0:0.97 "$file" 1> report_stdout 2> report_stderr
        BPS1=$(grep "Total bytes" report_stdout | awk '{ print $6; }');
        GECO3_NC=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
        end=`date +%s.%N`
        geco3_runtime=$( echo "$end - $start" | bc -l )
        echo -e "$name\t${cmix_runtime}\t${geco3_runtime}\t${CMIX_NC}\t${GECO3_NC}" >> ../reports/"$1"

        rm report_stdout report_stderr output.seq
    done
}

mkdir -p $PATH1
mkdir -p $PATH2

# HV1
efetch -db nucleotide -format fasta -id NC_001806 > ${PATH1}HHV1.fa
# HV2
efetch -db nucleotide -format fasta -id JN561323.2 > ${PATH1}HHV2.fa
# HV3
efetch -db nucleotide -format fasta -id X04370.1 > ${PATH1}HHV3.fa
# HV4
efetch -db nucleotide -format fasta -id DQ279927.1 > ${PATH1}HHV4.fa
# HV5
efetch -db nucleotide -format fasta -id NC_006273 > ${PATH1}HHV5.fa
# HV6A
efetch -db nucleotide -format fasta -id NC_001664.4 > ${PATH1}HHV6A.fa
# HV6B
efetch -db nucleotide -format fasta -id NC_000898.1 > ${PATH1}HHV6B.fa
# HV7
efetch -db nucleotide -format fasta -id NC_001716  > ${PATH1}HHV7.fa
# HV8
efetch -db nucleotide -format fasta -id AF148805.2 > ${PATH1}HHV8.fa

for file in ${PATH1}*.fa
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
            gto_fasta_to_seq < FILE > ${PATH2}"${file_name}"
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
rm -f FILE FASTA HEADER A LLL.seq > /dev/null

COMPRESSION REPORT_CMIX_GECO3_HHV
cd ../python || exit;
python3.6 compare_cmix_hhv.py
