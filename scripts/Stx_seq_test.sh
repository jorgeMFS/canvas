#!/bin/bash
#


CMIXPATH="../cmix-19.1/";

create_seq_reverse_comp(){

    cat "$1" | gto_reverse | gto_genomic_complement  > seq2
    cat "$1" seq2 > seq_ir
    rm seq2 
}

synthetic_sequence(){
    gto_genomic_gen_random_dna -s 101 -n 5000 > A.seq
    gto_reverse < A.seq | gto_genomic_complement > B.seq
    cat A.seq B.seq > AB.seq
    # rm A.seq B.seq
}

mutate_sequence(){
    gto_genomic_dna_mutate -d 0 -i 0 -m "$1" <  "$2" > "$3"
}



function GECO2_IR_COMPRESS_NEW(){
    rm -f ../reports/"$3";
    file=$2;
    Level_1="-tm 1:1:$1:0:0.7/0:0:0 -tm 12:50:$1:1:0.97/0:0:0.97"
    echo "Running $file ...";
    f="$(basename -- "$file")"
    name=$f
    for i in {0..100}
    do
        mutation_rate=$(echo "scale=10; ($i) / 100" | bc -l | awk '{printf "%f", $0}')
        # echo $mutation_rate
        mutate_sequence "$mutation_rate" "$file" LLL.seq
        GeCo2 -v "$Level_1" LLL.seq 1> report_stdout_"$1" 2> report_stderr_"$1"
        
        BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
        entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
        echo -e "$mutation_rate\t$name\t$entropy1" >> ../reports/"$3"

    done
    rm  LLL.seq*
    rm report_std*
}

function GECO3_IR_COMPRESS_NEW(){

    rm -f ../reports/"$3";
    file=$2;

    echo "Running $file ...";
    f="$(basename -- "$file")"
    name=$f

    for i in {0..100}
    do
        mutation_rate=$(echo "scale=10; ($i) / 100" | bc -l | awk '{printf "%f", $0}')
        mutate_sequence "$mutation_rate" "$file" LLL.seq
        GeCo3 -v -tm 1:1:$1:0:0.7/0:0:0 -tm 12:50:$1:1:0.97/0:0:0.97 LLL.seq 1> report_stdout_"$1" 2> report_stderr_"$1"
        BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
        entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
        echo -e "$mutation_rate\t$name\t$entropy1" >> ../reports/"$3"
    done

    rm  LLL.seq*
    rm report_std*
}

function GECO3_COMPRESS(){

    rm -f ../reports/"$3";
    file=$2;

    Level_1="-tm 1:1:0:0:0.7/0:0:0 -tm 12:50:1:1:0.97/0:0:0.97"

    echo "Running $file ...";
    f="$(basename -- "$file")"
    name=$f

    for i in {0..100}
    do
        mutation_rate=$(echo "scale=10; ($i) / 100" | bc -l | awk '{printf "%f", $0}')
        mutate_sequence "$mutation_rate" "$file" LLL.seq
        GeCo3 -v "$Level_1" LLL.seq 1> report_stdout_"$1" 2> report_stderr_"$1"
        BPS1=$(grep "Total bytes" report_stdout_"$1" | awk '{ print $6; }');
        entropy1=$(echo "scale=10; ($BPS1) / 2" | bc -l | awk '{printf "%f", $0}')
        echo -e "$mutation_rate\t$name\t$entropy1" >> ../reports/"$3"
    done

    rm  LLL.seq*
    rm report_std*
}

function NBDM2_SNT(){
    rm -f ../reports/"$2";
    file=$1;
    echo "Running $file ...";
    f="$(basename -- "$file")"
    name=$f

    for i in {0..100}
    do
        mutation_rate=$(echo "scale=10; ($i) / 100" | bc -l | awk '{printf "%f", $0}')
        mutate_sequence "$mutation_rate" "$file" LLL.seq
        NBDM2=$(python3.6 ../python/nbdm2d2.py LLL.seq | awk '{printf "%f", $0}');       
        echo -e "$mutation_rate\t$name\t$NBDM2" >> ../reports/"$2"
    done
}

function CMIX_COMPRESS(){
    rm -f ../reports/"$2";
    file=$1;

    echo "Running $file ...";
    f="$(basename -- "$file")"
    name=$f

    for i in {0..100}
    do
        mutation_rate=$(echo "scale=10; ($i) / 100" | bc -l | awk '{printf "%f", $0}')
        mutate_sequence "$mutation_rate" "$file" LLL.seq  
        ${CMIXPATH}cmix -c LLL.seq output.seq
        original=$(ls -la LLL.seq | awk '{ print $5;}');
        compressed=$(ls -la output.seq | awk '{ print $5;}');
        entropy=$(echo "scale=10; ($compressed * 8.0) / ($original*2.0)" | bc -l | awk '{printf "%f", $0}');
        echo -e "$mutation_rate\t$name\t$entropy" >> ../reports/"$2"
    done
    rm ./paq8l
    rm  LLL.seq* output.seq
    
}

function PAQ_COMPRESS(){

    rm -f ../reports/"$2";
    file=$1;

    echo "Running $file ...";
    f="$(basename -- "$file")"
    name=$f

    for i in {0..100}
    do
        mutation_rate=$(echo "scale=10; ($i) / 100" | bc -l | awk '{printf "%f", $0}')
        mutate_sequence "$mutation_rate" "$file" LLL.seq  
        ./paq8l -8 LLL.seq
        original=$(ls -la LLL.seq | awk '{ print $5;}');
        compressed=$(ls -la LLL.seq.paq8l | awk '{ print $5;}');
        entropy=$(echo "scale=10; ($compressed * 8.0) / ($original*2.0)" | bc -l | awk '{printf "%f", $0}');
        echo -e "$mutation_rate\t$name\t$entropy" >> ../reports/"$2"
    done
    rm ./paq8l
    rm  LLL.seq*
}


echo -e "\033[1;32mCreating synthetic sequence...\033[0m"

synthetic_sequence
seq_analyse="AB.seq"
wc -m $seq_analyse
cp ../paq8l/paq8l .
chmod +x ./paq8l
echo -e "\033[1;32mCompressing synthetic sequence...\033[0m"
CMIX_COMPRESS $seq_analyse CMIX_COMPRESS
PAQ_COMPRESS $seq_analyse PAQ_COMPRESS
GECO3_COMPRESS 0 $seq_analyse NC_GECO3_OPTIMAL
GECO3_IR_COMPRESS_NEW 0 $seq_analyse IR_0_GECO3_OPTIMAL
GECO3_IR_COMPRESS_NEW 1 $seq_analyse IR_1_GECO3_OPTIMAL
GECO3_IR_COMPRESS_NEW 2 $seq_analyse IR_2_GECO3_OPTIMAL
NBDM2_SNT $seq_analyse IR_NBMD_OPTIMAL

rm -f AB.seq A.seq B.seq  > /dev/null
echo -e "\033[1;32mCreating plot of synthetic sequence...\033[0m"
cd ../python || exit;
python3.6 stx_analysis.py
echo -e "\033[1;32mProcess successfully completed!\033[0m"
