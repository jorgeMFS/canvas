#!/bin/bash
# 
# ===============================================================================================
# RUN NBDM ===============================================================================
# ===============================================================================================

function NBDM(){
  rm -f ../reports/REPORT_COMPLEXITY_NBDM1_T;
  rm -f ../reports/REPORT_COMPLEXITY_NBDM2_T;
  for directory in  ../VirusDB/Virus_by_taxid1/*; do
      if [ -d "${directory}" ]; then
        dir=$(basename -- ${directory})
        for file in ${directory}"/"*".fasta"; do
          echo "Running $file ... in ${directory}...";
          f="$(basename -- $file)"
          name=$f
          taxid=$dir
          NBDM1=$(python3.6 ../python/nbdm2d1.py $file | awk '{printf "%f", $0}');
          echo -e "$taxid\t$name\t$NBDM1" >> ../reports/REPORT_COMPLEXITY_NBDM1_T;
          NBDM2=$(python3.6 ../python/nbdm2d2.py $file | awk '{printf "%f", $0}');
          echo -e "$taxid\t$name\t$NBDM2" >> ../reports/REPORT_COMPLEXITY_NBDM2_T;
         done
      fi
  done
}

NBDM &
P=$!
wait $P
cd ../
#