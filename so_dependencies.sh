#!/bin/bash
# 
echo -e "\033[1mStart Installation of dependencies...\033[0m"
sudo apt update && apt install -y python3-pip wget

sudo apt-get install -y bc

sudo apt-get install -y unzip

sudo apt-get install -y gcc-multilib

sudo apt-get install -y build-essential

sudo apt-get install -y qt5-default

wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh #get anaconda

bash /tmp/Anaconda3-2020.02-Linux-x86_64.sh #install anaconda

echo -e "\033[1;32mSuccessfully installed tools!\033[0m";
