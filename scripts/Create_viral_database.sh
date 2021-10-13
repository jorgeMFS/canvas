#!/bin/bash
#
BUILD_VIRAL_TXT=0;
BUILD_VIRAL=0;
THREADS=4;
MAKE_TABLE=0;
MATCH_TABLE=0;
MATCH_AND_MERGE_SEQ_FROM_TABLE=1;


############### PROCESS DATA ##########################

if [ "$BUILD_VIRAL" -eq "1" ];
  then
  cd ../ViralDB/ || exit
  mkdir -p GB_DB_VIRAL/
  rm -f GB_DB_VIRAL/*.fa.gz
  cat ASCG.txt | xargs -I{} -n1 -P$THREADS wget -P GB_DB_VIRAL {}/*_genomic.fna.gz
  mkdir -p GB_DB_VIRAL_CDS/
  mkdir -p GB_DB_VIRAL_RNA/
  rm -f GB_DB_VIRAL_CDS/*.fa.gz
  rm -f GB_DB_VIRAL_RNA/*.fa.gz
  mv GB_DB_VIRAL/*_cds_from_genomic.fna.gz GB_DB_VIRAL_CDS/
  mv GB_DB_VIRAL/*_rna_from_genomic.fna.gz GB_DB_VIRAL_RNA/
  rm -f VDB.fa.gz;
  zcat GB_DB_VIRAL/*.fna.gz | gzip -9 > VDB.fa.gz
fi


if [ "$BUILD_VIRAL_TXT" -eq "1" ];
  then
  cd ../ViralDB/ || exit #remove
  #rm -f assembly_summary.txt;
  #wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/viral/assembly_summary.txt
  #awk -F '\t' '{if($12=="Complete Genome"||$12=="Chromosome") print $20}' assembly_summary.txt > ASCG.txt
  mkdir -p GB_DB_VIRAL_INFO/
    while read p; do
        b=$(basename "$p")/*_assembly_report.txt
        if ! (ls GB_DB_VIRAL_INFO | grep -q "$b");then
            echo "$p"/*_assembly_report.txt
            #wget -P GB_DB_VIRAL_INFO "${p}/*_assembly_report.txt"         
        fi
    done < ASCG.txt 
  #cat Q | xargs -n1 -P$THREADS wget -P GB_DB_VIRAL_INFO
  #rm -f GB_DB_VIRAL_INFO/*.txt
  #cat ASCG.txt | xargs -I{} -n1 -P$THREADS wget -P GB_DB_VIRAL_INFO {}/*_assembly_report.txt
fi


if [ "$BUILD_VIRAL" -eq "1" ];
  then
  cd ../ViralDB/ || exit #remove
  #rm -f assembly_summary.txt;
  #wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/viral/assembly_summary.txt
  #awk -F '\t' '{if($12=="Complete Genome"||$12=="Chromosome") print $20}' assembly_summary.txt > ASCG.txt
  mkdir -p GB_DB_VIRAL_INFO/
    while read p; do
        b=$(basename "$p")/*_assembly_report.txt
        if ! (ls GB_DB_VIRAL_INFO | grep -q "$b");then
            echo "$p"/*_assembly_report.txt
            #wget -P GB_DB_VIRAL_INFO "${p}/*_assembly_report.txt"         
        fi
    done < ASCG.txt 
  #cat Q | xargs -n1 -P$THREADS wget -P GB_DB_VIRAL_INFO
  #rm -f GB_DB_VIRAL_INFO/*.txt
  #cat ASCG.txt | xargs -I{} -n1 -P$THREADS wget -P GB_DB_VIRAL_INFO {}/*_assembly_report.txt
fi

if [ "$MAKE_TABLE" -eq "1" ];
    then
    rm ../ViralDB/summary_reports.txt;
    for file in ../ViralDB/GB_DB_VIRAL_INFO/*_assembly_report.txt
        do
            taxid=$(cat "$file" | grep "Taxid" | awk '{print $3}');
            taxid=${taxid%?};
            organism_name=$(cat "$file" | grep "Organism name" | sed s/"# Organism name:  "//|tr '\n' ' '|sed 's/.$//');
            organism_name=${organism_name%?};
            assembly_level=$(cat "$file" | grep "Assembly level" | sed s/"# Assembly level: "// | tr '\n' ' '|sed 's/.$//');
            assembly_level=${assembly_level%?};
            genome_complete=$(cat "$file" | grep "Genome representation:" | sed s/"# Genome representation: "// | tr '\n' ' '|sed 's/.$//');
            genome_complete=${genome_complete%?};
            sq_nb=$(tail -n 1 "$file" | awk -F "\t" '{print $5}'|tr '\n' ' '|sed 's/.$//');
            gbaa=$(cat "$file" | grep  "GenBank assembly accession" | sed s/"# GenBank assembly accession: "// | tr '\n' ' '|sed 's/.$//');
            gbaa=${gbaa%?};
            echo -e -n "${sq_nb}\t${gbaa}\t${taxid}\t${organism_name}\t${assembly_level}\t${genome_complete}\n" >> ../ViralDB/summary_reports.txt;
    done 
fi

if [ "$MATCH_TABLE" -eq "1" ];
    then
    mkdir -p ../ViralDB/TaxSQ

    for file in ../ViralDB/SplitSQ/*.fasta
        do
        GenBank_Accn=$(head -n 1 "$file" | awk '{print $1}'| tr -d '>')
        filename="${file%.*}"
        fil="$(basename -- "$filename")"
        if ! grep -q "$GenBank_Accn" ../ViralDB/summary_reports.txt  
        then
            rm "$file"
        else
            taxid=$(grep "$GenBank_Accn" ../ViralDB/summary_reports.txt | awk '{print $3}');
            mkdir -p "../ViralDB/TaxSQ/${taxid}"
            gto_fasta_to_seq < "$file" > "../ViralDB/TaxSQ/${taxid}/${fil}_${taxid}.seq"; 
        fi
    done
fi




exit;
mkdir -p ../ViralDB/
mkdir -p ../ViralDB/SplitSQ

cd ../ViralDB/ || exit

# gto_build_dbs.sh -vi
gzip -d VDB.fa.gz
gto_fasta_extract_read_by_pattern -p "complete genome" < VDB.fa > CG_VDB_pre.fa
gto_fasta_rand_extra_chars < CG_VDB_pre.fa > CG_VDB.fa
rm CG_VDB_pre.fa;
gto_fasta_split_reads -l "SplitSQ" < CG_VDB.fa


