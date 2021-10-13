#!/bin/bash
#

function GECO_IR_COMPRESS_OTHER(){

rm -f ../reports/"$3";

for directory in  ../VirusDB/$2/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- ${directory})
        for file in ${directory}"/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- $file)";
            name=$f ;
            taxid=$dir ;
            GeCo3 -v -tm 1:1:$1:0:0.7/0:0:0 -tm 12:50:$1:1:0.97/0:0:0.97 "$file" 1> report_stdout_other_"$1" 2> report_stderr_other_"$1" ;
            BPS1=$(grep "Total bytes" report_stdout_other_"$1" | awk '{ print $6; }');
            entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}');
            echo -e "$taxid\t$name\t$entropy1" >> ../reports/"$3" ;
        done
    fi
    rm report_stdout_other_"$1" report_stderr_other_"$1" ;
done

}

GECO_IR_COMPRESS_OTHER 0 "Virus_by_taxid1" Report_NC_IR_OPTIMAL_0
GECO_IR_COMPRESS_OTHER 1 "Virus_by_taxid2" Report_NC_IR_OPTIMAL_1
GECO_IR_COMPRESS_OTHER 2 "Virus_by_taxid3" Report_NC_IR_OPTIMAL_2

P=$!
wait $P

cd ../
