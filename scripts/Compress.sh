#!/bin/bash
# 
function GECO_COMPRESS(){

rm -f ../reports/REPORT_COMPLEXITY_NC;

for directory in  ../VirusDB/Virus_by_taxid/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- ${directory})
        for file in ${directory}"/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- $file)"
            name=$f
            taxid=$dir
            original=`ls -la $file | awk '{ print $5;}'`;
            GeCo3 -l $1 $file
            compressed=`ls -la $file.co | awk '{ print $5;}'`;
            entropy1=`echo "scale=10; ($compressed) / $original" | bc -l | awk '{printf "%f", $0}'`;

            echo -e "$taxid\t$name\t$entropy1" >> ../reports/$2
        done
    fi
done
}





GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_1 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_2 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_3 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_4 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_5 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_6 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_7 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_8 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_9 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_10 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_11 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_12 &
GECO_COMPRESS 1 REPORT_COMPLEXITY_NC_13 &
P=$!
wait $P
cd ../
#
