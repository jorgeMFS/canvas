#!/bin/bash
#

function GECO_IR_COMPRESS(){

rm -f ../reports/"$3";
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
        dir=$(basename -- "${directory}")
        for file in ${directory}"/"*".fasta"; do
            echo "Running $file ... in ${directory}...";
            f="$(basename -- "$file")"
            name=$f
            taxid=$dir
            GeCo3 -v "$Level_1" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_2" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy2=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_3" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy3=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_4" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy4=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_5" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy5=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_6" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy6=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_7" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy7=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_8" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy8=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_9" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy9=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_10" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy10=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_11" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy11=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_12" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy12=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            GeCo3 -v "$Level_13" "$file" 1> report_stdout_"$1" 2> report_stderr_"$1"
            BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
            entropy13=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
            echo -e "$taxid\t$name\t$entropy1\t$entropy2\t$entropy3\t$entropy4\t$entropy5\t$entropy6\t$entropy7\t$entropy8\t$entropy9\t$entropy10\t$entropy11\t$entropy12\t$entropy13" >> ../reports/$3
                                                                        
        done
    fi
    rm report_stdout_"$1" report_stderr_"$1"
done

}



GECO_IR_COMPRESS 0 "Virus_by_taxid1" Report_NC_IR_0_FINAL &
GECO_IR_COMPRESS 1 "Virus_by_taxid2" Report_NC_IR_1_FINAL &
GECO_IR_COMPRESS 2 "Virus_by_taxid3" Report_NC_IR_2_FINAL &

P=$!
wait $P

cd ../
