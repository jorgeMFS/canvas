#!/bin/bash
# 
function GC_SEQ(){

rm -f ../reports/"$1";

for directory in  ../VirusDB/Virus_by_taxid/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- "${directory}")
        for file in "${directory}/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- "$file")"
            name=$f
            taxid=$dir

            # len_x=$(wc -m <"$file")
            gto_genomic_count_bases < "$file" > GCTA; 
            nbases=$(sed "2q;d" GCTA | awk -F ":" '{print $2}')
            nC=$(sed "4q;d" GCTA | awk -F ":" '{print $2}')
            nG=$(sed "5q;d" GCTA | awk -F ":" '{print $2}')
            GC_p=$(echo "scale=10; (${nC}+${nG}) / ${nbases}" | bc -l | awk '{printf "%f", $0}');
            echo -e "$taxid\t$name\t$GC_p" >> ../reports/"$1"
        done
    fi
done
rm GCTA
}
echo -e "\033[1mMeasuring the GC-Content of genomes in the database......\033[0m"

GC_SEQ REPORT_SEQ_GC
echo -e "\033[1;32mProcess successfully completed!\033[0m"



