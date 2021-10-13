#!/bin/bash
#

function GECO_IR_COMPRESS(){

rm -f ../reports/$2;
Level_1="-tm 1:1:$1:0:0.7/0:0:0 -tm 12:20:$1:1:0.97/0:0:0"
Level_2="-tm 2:1:$1:0:0.78/0:0:0 -tm 4:1:$1:0:0.78/0:0:0  -tm 11:80:$1:1:0.96/0:0:0"
Level_3="-tm 3:1:$1:0:0.80/0:0:0 -tm 4:1:$1:0:0.84/0:0:0  -tm 12:50:$1:1:0.94/2:15:0.95"
Level_4="-tm 4:1:$1:0:0.80/0:0:0 -tm 6:1:$1:0:0.84/0:0:0  -tm 13:50:$1:1:0.94/2:15:0.95"
Level_5="-tm 4:1:$1:0:0.82/0:0:0 -tm 6:1:$1:0:0.72/0:0:0  -tm 13:50:$1:1:0.95/2:15:0.95"
Level_6="-tm 4:1:$1:0:0.88/0:0:0 -tm 6:1:$1:0:0.76/0:0:0  -tm 13:50:$1:1:0.95/2:15:0.95"
Level_7="-tm 4:1:$1:0:0.90/0:0:0 -tm 6:1:$1:0:0.79/0:0:0  -tm 8:1:$1:0:0.91/0:0:0       -tm 13:10:$1:0:0.94/1:20:0.94 -tm 16:200:$1:5:0.95/4:15:0.95"
Level_8="-tm 4:1:$1:0:0.90/0:0:0 -tm 6:1:$1:0:0.80/0:0:0  -tm 13:10:$1:0:0.95/1:20:0.94 -tm 16:100:$1:5:0.95/3:15:0.95"
Level_9="-tm 4:1:$1:0:0.91/0:0:0 -tm 6:1:$1:0:0.82/0:0:0  -tm 13:10:$1:0:0.95/1:20:0.94 -tm 17:100:$1:8:0.95/3:15:0.95"
Level_10="-tm 1:1:$1:0:0.90/0:0:0 -tm 3:1:$1:0:0.90/0:0:0 -tm 6:1:$1:0:0.82/0:0:0       -tm 9:10:$1:0:0.9/0:0:0 -tm 11:10:$1:0:0.9/0:0:0 -tm 13:10:$1:0:0.9/0:20:0.94 -tm 17:100:$1:8:0.89/5:10:0.9"
Level_11="-tm 4:1:$1:0:0.91/0:0:0 -tm 6:1:$1:0:0.82/0:0:0 -tm 13:10:$1:0:0.95/1:20:0.94 -tm 17:100:$1:15:0.95/3:15:0.95" 
Level_12="-tm 1:1:$1:0:0.9/0:0:0 -tm 3:1:$1:0:0.9/0:0:0   -tm 6:1:$1:0:0.85/0:0:0       -tm 9:10:$1:0:0.9/0:0:0 -tm 11:10:$1:0:0.9/0:0:0 -tm 13:50:$1:0:0.9/0:20:0.94 -tm 17:100:$1:20:0.9/3:10:0.9" 

for directory in  ../VirusDB/$2/*; do
    if [ -d "${directory}" ]; then
        dir=$(basename -- ${directory})
        for file in ${directory}"/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- $file)"
            name=$f
            taxid=$dir
            original=$(ls -la "$file" | awk '{ print $5;}');
            GeCo3 $Level_1 $file
            compressed=$(ls -la "$file".co | awk '{ print $5;}');
            entropy1=$(echo "scale=10; ($compressed) / $original" | bc -l | awk '{printf "%f", $0}');
            GeCo3 -v $Level_1 $file 1>> report_stdout"_$3" 2>> report_stderr"_$3"

            #echo -e "$taxid\t$name\t$entropy1" # >> ../reports/$3
            exit;
        done
    fi
done
}

 
# GECO_IR_COMPRESS 0 "Virus_by_taxid" x0 
# GECO_IR_COMPRESS 1 "Virus_by_taxid" x1
GECO_IR_COMPRESS 2 "Virus_by_taxid" x2
P=$!
wait $P
cd ../