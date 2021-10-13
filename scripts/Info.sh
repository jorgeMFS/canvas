#!/bin/bash
#

GenomeInfo () {
    for file in "../VirusDB/SeqSplit/out"*".fasta"
        do
        filename="${file%.*}"
        fil="$(basename -- $filename)"
        if ! ( cat ../VirusDB/ViralSeq_Genome.info | grep -q $fil.fasta);then
            GenBank_Accn=$(head -n 1 $file | awk '{print $1}'| tr -d '>')
            esearch -db nuccore -query "$GenBank_Accn [ACCN]" | efetch -format gpc > $1
            Genometype=$(cat $1 | xtract -insd INSDSeq_moltype| awk -F '\t' '{print $2}')
            strand=$(cat $1 | xtract -insd INSDSeq_strandedness| awk -F '\t' '{print $2}')
            echo -e "$fil.fasta\t${GenBank_Accn}\t${Genometype}\t${strand}" >> ../VirusDB/ViralSeq_Genome.info; 
            rm $1
        fi
        if ! ( cat ../VirusDB/ViralSeq_Org.info | grep -q $fil.fasta);then
            GenBank_Accn=$(head -n 1 $file | awk '{print $1}'| tr -d '>')
            esearch -db nuccore -query "$GenBank_Accn [ACCN]" | efetch -format gpc > $1
            taxonomy_name=$(cat $1 | xtract -insd INSDSeq_taxonomy| awk -F '\t' '{print $2}')
            organism=$(cat $1 | xtract -insd INSDSeq_organism| awk -F '\t' '{print $2}')
            host=$(cat $1 | xtract -insd INSDQualifier_value| awk -F '|' '{print $4}')
            echo -e "$fil.fasta\t${organism}\t${taxonomy_name}\t${host}" >> ../VirusDB/ViralSeq_Org.info; 
            rm $1
        fi
    done
}

GenomeInfo "A" &


