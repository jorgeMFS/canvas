
<p align="center">
<img src="imgs/canvas.png" alt="Panther" width="300" border="0" /></p>
<br>
<h2 align="center">
 Complexity ANalysis VirAl Sequences 
</h2>

[![License: MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

## Install GIT LFS (GIT LARGE FILE STORAGE)

If git LFS, please intall it using the following steps:

```bash
mkdir -p gitLFS
cd gitLFS/
wget https://github.com/git-lfs/git-lfs/releases/download/v2.9.0/git-lfs-linux-amd64-v2.9.0.tar.gz
tar -xf git-lfs-linux-amd64-v2.9.0.tar.gz
chmod 755 install.sh
sudo ./install.sh
```

## Download Project
Get CANVAS project using:
```bash
git clone https://github.com/jorgeMFS/canvas.git
cd canvas/
```

## Using Docker
To perform installation correctly, docker and docker compose must be installed in the system (see https://docs.docker.com/engine/install/ubuntu/). 


Then follow these instructions:
```sh
git clone https://github.com/jorgeMFS/canvas.git
cd canvas
docker-compose build
docker-compose up -d && docker exec -it canvas bash && docker-compose down
```

## Install Tools
Give run permissions to the files and Install Tools:
``` bash
chmod +x *.sh
bash Make.sh;
```

## Result Replication
To run the pipeline and obtain all the Reports in the folder reports, use the following commands.
Note that it is not required to perform database reconstruction and feature recreation to perform any other tasks.  However, if you wish to recreate the features reports, you must perform the database reconstruction task.

### Cmix vs GeCo3 time-compression Analysis
To obtain the Human Herpesvirus plot run:
```bash
cd scripts || exit;
python compare_cmix_hhv.py 
``` 

### Compression Benchmark Analysis
To obtain the Compression Benchmark plots run:
```bash
cd python || exit;
python select_best_nc_model.py;
``` 

### Synthetic Sequence Analysis
To perform the synthetic sequence test run:
```bash
cd scripts || exit;
bash Stx_seq_test.sh;
``` 

### Classification
To perform classification run the following code:

```bash
cd python || exit;
python prepare_classification.py; #recreate classification dataset
python classifier.py; #perform classifications
``` 

### IR Analysis
To perform the complete IR analysis and create:
- boxplots;
- 2d scatter plots;
- 3d scatter plots;
- top taxonomic group lists;
- Occurrence of each Genus.

Execute this code:

```bash
cd python || exit;
python ir_analysis.py; # Performs complete IR analysis
``` 

### Human Herpesvirus Analysis
To obtain the Human Herpesvirus plot run:
```bash
cd scripts || exit;
bash Herpesvirales.sh;
``` 
### Cmix vs GeCo3 time-compression Analysis
To obtain the Human Herpesvirus plot run:
```bash
cd scripts || exit;
python compare_cmix_hhv.py 
``` 

## Database reconstruction
If you wish to reconstruct the Viral database, run the following script:

```bash
cd scripts || exit;
bash Build_DB.sh;
``` 

### Create Features for Analysis and Classification
To create the features for analysis and classification (very time consuming, may take several days) run: 
```bash
cd scripts || exit;
bash Process_features.sh;
``` 

### Benchmarck Compression Reports
To recreate the compression reports used for benchmark (very time consuming, may take several days) run: 
```bash
cd scripts || exit;
bash Compress.sh;
``` 

## Phylogenetic Trees
The Phylogenetic Trees require GUI application. As such, the reproduction of the trees has to be performed outside of the docker on the Ubuntu system on the /canvas folder:

```bash
chmod +x *.sh
bash so_dependencies.sh #install Ubuntu system dependencies required for the script to run and Anaconda
conda create -n canvas python=3.6
conda activate canvas
bash Make.sh #install python libs
bash Install_programs.sh #install tools using conda
``` 
Afterwards, to obtain the Phylogenetic Tree plots run:
```bash
cd python || exit;
python phylo_tree.py;
``` 

## Website

Check out the website of this project: https://asilab.github.io/canvas/

## CITE
Please cite the followings, if you use CANVAS:

Processing...

```bib

```
## Requirements
- Ubunto 18.0 or higher
- Docker and docker-compose
- Anaconda
- Python3.6

## ISSUES
Please let us know if there is any
[issues](https://github.com/jorgeMFS/canvas/issues).

## LICENSE
CANVAS is under MIT license. For more information, click
[here](https://opensource.org/licenses/MIT).