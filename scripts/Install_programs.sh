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


echo "Start Installation..."

conda install -c cobilab gto --yes
conda install -y -c bioconda geco3
conda install -c bioconda entrez-direct --yes
conda install -c https://conda.anaconda.org/biocore scikit-bio
conda install -c etetoolkit ete3 ete_toolchain
conda install -c anaconda scipy --yes
conda install -c conda-forge xgboost


Check_Installation "gto";
Check_Installation "GeCo3";
Check_Installation "efetch";

# statsmodels