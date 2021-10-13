#!/bin/bash
# 
function SEQ_LEN(){

rm -f ../reports/"$1";

for directory in  ../VirusDB/Virus_by_taxid1/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- "${directory}")
        for file in "${directory}/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- "$file")"
            name=$f
            taxid=$dir

            len_x=$(wc -m <"$file")

            echo -e "$taxid\t$name\t$len_x" >> ../reports/"$1"
        done
    fi
done
}

SEQ_LEN REPORT_SEQ_LEN_T


