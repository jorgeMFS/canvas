#!/bin/bash
# NCCD
NCCD() {
    rm "$2"
    while read -r p; do
    x=$(echo "$p" | awk '{print $1}')
    y=$(echo "$p" | awk '{print $2}')
    len_x=$(wc -m <"$x")
    len_y=$(wc -m <"$y")
    C_value "$x" "$len_x" Cx &
    C_value "$x" "$len_y" Cy &
    C_ref "$x" "$y" "$len_x" Cx_y &
    C_ref "$y" "$x" "$len_y" Cy_x &
    wait
    Cx=$(awk '{print $1}' Cx)
    Cy=$(awk '{print $1}' Cy)
    Cx_y=$(awk '{print $1}' Cx_y)
    Cy_x=$(awk '{print $1}' Cy_x)
    echo -e "$x\t$y\t$Cx\t$Cy\t$Cx_y\t$Cy_x" >> "$2"
    done < "$1"
    rm Cx Cy Cx_y Cy_x
}

C_value(){
    Cs=$(GeCo3 -tm 1:1:0:0:0.7/0:0:0 -tm 3:1:0:0:0.9/0:0:0 -tm 7:10:1:0:0.9/0:0:0  -tm 13:50:1:1:0.95/0:0:0 -tm 17:200:1:10:0.95/3:50:0.95 -lr 0.03 -hs 64 $1)
    compressed=$(echo "$Cs" |awk -F "," '{ print $4;}'| awk '{print $1}');
    len_s=$2
    local  myCs=$(echo "scale=4; ($len_s * $compressed)"|bc)
    echo "$myCs" > "$3"
}

C_ref(){
    seq=$1
    ref=$2
    len_seq=$3
    Cref=$(GeCo3 -tm 1:1:0:0:0.7/0:0:0 -tm 3:1:0:0:0.9/0:0:0 -tm 7:10:1:0:0.9/0:0:0  -tm 13:50:1:1:0.95/0:0:0 -tm 17:200:1:10:0.95/3:50:0.95 -rm 5:1:0:0:0.9/0:0:0 -rm 8:10:1:0:0.9/0:0:0  -rm 13:200:1:1:0.95/0:0:0 -tm 17:500:1:10:0.95/5:20:0.95 -lr 0.03 -hs 64 -r $ref $seq)
    comp_ref=$(echo $Cref |awk -F "," '{ print $4;}'| awk '{print $1}');
    local  myCref=$(echo "scale=4; ($len_seq * $comp_ref)"|bc)
    echo $myCref > $4
}

NCCD "../VirusDB/Virus_NCCD_process_list" "../reports/REPORT_NCCD"