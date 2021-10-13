#!/bin/bash
# 
echo -e "\033[1;32mStarting process of creating the features for the complete viral genome...\033[0m"
bash LenSeq.sh #"../reports/REPORT_SEQ_LEN"
bash GC.sh #"../reports/REPORT_SEQ_GC"
scripts/Compression_features.sh # ../reports/{REPORT_COMPLEXITY_NC_OTHER_3, REPORT_COMPLEXITY_NC_OTHER_3, Report_NC_IR_OPTIMAL_0, Report_NC_IR_OPTIMAL_1, Report_NC_IR_OPTIMAL_2}
echo -e "\033[1;32mProcess successfully completed!\033[0m"
