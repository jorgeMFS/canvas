#!/bin/bash
#

Check_Installation() {
    if ! [ -x "$(command -v "$1")" ]; then
        echo -e "\033[6;31mERROR\033[0;31m: $1 is not installed!" >&2;
        exit 1;
    else
        echo -e "\033[1;32mSUCCESS!\033[0m";
    fi
}

Cmix_Installation() {
    mkdir -p tmp
    wget https://github.com/byronknoll/cmix/archive/refs/tags/v19.1.zip -P tmp
    unzip tmp/v19.1.zip 
    cd cmix-19.1/ 
    chmod +x cmix
    make
    cd ..
    rm -rf tmp
}

echo -e "\033[1mStart Tool Installation...\033[0m"


conda install -c bioconda geco3 --yes
Check_Installation "GeCo3";
conda install -c bioconda entrez-direct --yes
Check_Installation "efetch";
conda install -c cobilab gto --yes 
Check_Installation "gto";
Cmix_Installation

echo -e "\033[1;32mSuccessfully installed tools!\033[0m";
