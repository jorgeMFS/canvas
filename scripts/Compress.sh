#!/bin/bash
# 
function GECO_COMPRESS(){

rm -f ../reports/"$2";

for directory in  ../VirusDB/Virus_by_taxid/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- "${directory}")
        for file in "${directory}/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- "$file")"
            name=$f
            taxid=$dir
            GeCo3 -v -l "$1" "$file" 1> report_stdout_nc_"$1" 2> report_stderr_nc_"$1"
            BPS1=$(grep "Total bytes" report_stdout_nc_"$1" | awk '{ print $6; }');
            entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            echo -e "$taxid\t$name\t$entropy1" >> ../reports/"$2"
        done
    fi
    rm report_stdout_nc_"$1" report_stderr_nc_"$1"
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
echo "Starting Compression of the complete viral genome..."
echo "This process might take a few hour/days to complete..."

GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_1 &
GECO_COMPRESS 2 REPORT_COMPLEXITY_NC_2 & 
GECO_COMPRESS 3 REPORT_COMPLEXITY_NC_3 &
GECO_COMPRESS 4 REPORT_COMPLEXITY_NC_4 &
GECO_COMPRESS 5 REPORT_COMPLEXITY_NC_5 &
GECO_COMPRESS 6 REPORT_COMPLEXITY_NC_6 &
GECO_COMPRESS 7 REPORT_COMPLEXITY_NC_7 &
GECO_COMPRESS 8 REPORT_COMPLEXITY_NC_8 &
GECO_COMPRESS 9 REPORT_COMPLEXITY_NC_9 &
GECO_COMPRESS 10 REPORT_COMPLEXITY_NC_10 &
GECO_COMPRESS 11 REPORT_COMPLEXITY_NC_11 &
GECO_COMPRESS 12 REPORT_COMPLEXITY_NC_12 &
GECO_COMPRESS 13 REPORT_COMPLEXITY_NC_13 &
P=$!
wait $P

GECO_COMPRESS_OTHER "-tm 1:1:0:0:0.7/0:0:0 -tm 12:20:1:1:0.97/1:1:0.97" "1" REPORT_COMPLEXITY_NC_OTHER_1 &
GECO_COMPRESS_OTHER "-tm 1:1:0:0:0.7/0:0:0 -tm 12:20:1:1:0.97/2:1:0.97" "2" REPORT_COMPLEXITY_NC_OTHER_2 &
GECO_COMPRESS_OTHER "-tm 1:1:0:0:0.7/0:0:0 -tm 12:50:1:1:0.97/0:0:0.97" "3" REPORT_COMPLEXITY_NC_OTHER_3 &
GECO_COMPRESS_OTHER "-tm 1:1:0:0:0.7/0:0:0 -tm 12:20:1:1:0.97/0:0:0.97 -lr 0.05 -hs 40" "4" REPORT_COMPLEXITY_NC_OTHER_4 &
GECO_COMPRESS_OTHER "-tm 1:1:0:0:0.7/0:0:0 -tm 12:20:1:1:0.97/0:0:0.97 -lr 0.15 -hs 40" "5" REPORT_COMPLEXITY_NC_OTHER_5 &
GECO_COMPRESS_OTHER "-tm 1:1:0:0:0.7/0:0:0 -tm 12:20:1:1:0.97/0:0:0.97 -lr 0.3 -hs 40" "6" REPORT_COMPLEXITY_NC_OTHER_6 &
P=$!
wait $P
echo "Compression Complete!"