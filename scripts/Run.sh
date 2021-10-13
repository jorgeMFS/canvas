#!/bin/bash
#
chmod +x *.sh
#
./Install_programs.sh 
./Create_viral_database.sh


./Compress.sh
./BDM_run.sh
./Average.sh

