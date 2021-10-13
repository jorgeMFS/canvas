
<p align="center">
<img src="imgs/canvas.png" alt="Panther" width="300" border="0" /></p>
<br>
<h2 align="center">
 Complexity ANalysis VirAl Sequences 
</h2>


## Download Project
Get CANVAS project using:
```bash
git clone https://github.com/jorgeMFS/canvas.git
cd canvas/
```

## Install Tools
Give run permissions to the files:
``` bash
chmod +x *.sh
bash Make.sh
```

## Using Docker

```sh
git clone https://github.com/jorgeMFS/canvas.git
cd canvas
docker-compose build
docker-compose up -d && docker exec -it canvas bash && docker-compose down
```


## Result Replication
To run the pipeline and obtain all the Reports in the folder reports, use the following commands.

### Simple Compression Reports
To recreate the compression reports used for benchmark (very time consuming) run: 
```bash
cd scripst || exit;
bash Compress.sh
``` 

### Compression Benchmark
To obtain the Compression Benchmark plots run:
```bash
cd python || exit;
python select_best_nc.py
``` 

### Sythetic Sequence Analysis
To perform the sythetic sequence test run:
```bash
cd scripts || exit;
bash Stx_seq_test.sh
``` 

### Classification
To perform classification run the following code:

```bash
cd python || exit;
python prepare_classification.py #recreate classification dataset
python classifier.py #perform classifications
``` 

### IR Analysis
To perform the complete IR analysis and create:
- boxplots;
- 2d scatter plots;
- 3d scatter plots;
- top taxonomic group lists;
- Occurance of each Genus.

Execute this code:

```bash
cd python || exit;
python ir_analysis.py # Performs complete IR analysis
``` 

### Human Herpesvirus Analysis
To obtain the Human Herpesvirus plot run:
```bash
cd scripts || exit;
bash Herpersvirales.sh
``` 

### Phylogenetic Trees
To obtain the Phylogenetic Tree plots run:
```bash
cd python || exit;
python phylo_tree.py
``` 

## Website

Check out the website of this project: https://asilab.github.io/canvas/

## CITE
Please cite the followings, if you use CANVAS:

Processing...

```bib

```

## ISSUES
Please let us know if there is any
[issues](https://github.com/jorgeMFS/canvas/issues).

## LICENSE
CANVAS is under MIT license. For more information, click
[here](https://opensource.org/licenses/MIT).