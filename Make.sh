#!/bin/bash
#

# conda create -n canvas python=3.6
# shellcheck disable=SC1091
# source activate canvas
cd scripts/ || exit;

chmod +x ./*.sh
bash Install_programs.sh 
python3.6 -m pip install --upgrade pip
python3.6 -m pip install  -r ../requirements.txt

# ./Create_viral_database.sh
