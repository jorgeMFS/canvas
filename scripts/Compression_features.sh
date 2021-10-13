#!/bin/bash
#

function GECO_IR_COMPRESS_OTHER(){
rm -f ../reports/"$3";
for directory in  ../VirusDB/$2/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- "${directory}")
        for file in ${directory}"/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- "$file")";
            name=$f ;
            taxid=$dir ;
            GeCo3 -v -tm 1:1:"$1":0:0.7/0:0:0 -tm 12:50:"$1":1:0.97/0:0:0.97 "$file" 1> report_stdout_other_"$1" 2> report_stderr_other_"$1" ;
            BPS1=$(grep "Total bytes" report_stdout_other_"$1" | awk '{ print $6; }');
            entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}');
            echo -e "$taxid\t$name\t$entropy1" >> ../reports/"$3" ;
        done
    fi
    rm report_stdout_other_"$1" report_stderr_other_"$1" ;
done
}

function GECO_COMPRESS_OTHER(){
rm -f ../reports/"$3";
for directory in  ../VirusDB/Virus_by_taxid/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- "${directory}")
        for file in "${directory}/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- "$file")"
            name=$f
            taxid=$dir
            GeCo3 -v "$1" "$file" 1> report_stdout_other_"$2" 2> report_stderr_other_"$2"
            BPS1=$(grep "Total bytes" report_stdout_other_"$2" | awk '{ print $6; }');
            entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            echo -e "$taxid\t$name\t$entropy1" >> ../reports/"$3"
        done
    fi
    rm report_stdout_other_"$2" report_stderr_other_"$2"
done
}

echo -e "\033[1;32mStarting Compression of the complete viral genome...\033[0m"
echo -e "\033[1mThis process might take a few hour/days to complete...\033[0m"

GECO_IR_COMPRESS_OTHER 0 "Virus_by_taxid" Report_NC_IR_OPTIMAL_0 &
GECO_IR_COMPRESS_OTHER 1 "Virus_by_taxid" Report_NC_IR_OPTIMAL_1 &
GECO_IR_COMPRESS_OTHER 2 "Virus_by_taxid" Report_NC_IR_OPTIMAL_2 &
GECO_COMPRESS_OTHER "-tm 1:1:0:0:0.7/0:0:0 -tm 12:50:1:1:0.97/0:0:0.97" "3" REPORT_COMPLEXITY_NC_OTHER_3 &
P=$!
wait $P
echo -e "\033[1;32mCompression of the viral genome Complete!\033[0m"
echo -e "\033[1mResults in the /reports folder:\033[0m"
echo "Report_NC_IR_OPTIMAL_0, Report_NC_IR_OPTIMAL_1, Report_NC_IR_OPTIMAL_2,REPORT_COMPLEXITY_NC_OTHER_3 "
cd ../