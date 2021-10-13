#!/bin/bash
#
# cd "/home/miguel/Documentos/PhD/tmp/agregation_plots_boxplots/" || exit
# for d in */ ; do
#     for filename in $d*.pdf; do
#         basename="${filename%.*}"
#         arrIN=(${basename//_/ })
#         basename="${arrIN[0]}" 
#         convert "$filename" "${basename}"".jpg"
#         rm "$filename"
#     done
# done
# exit;
cd "/home/miguel/Documentos/PhD/tmp/trees_2/" || exit

for d in */ ; do
    for filename in $d*.pdf; do
        if ! $(echo $filename |grep -q "_colorbar") ;
            then
            basename="${filename%.*}"
            final_name="$basename""_final.pdf"
            DIR=${filename%/*}
            output="$DIR""/output.pdf"

            pdfcrop --margins "0 0 0 -3500" "$filename" "$output"
            mv "$output" "$filename"
            colorbar=${basename}"_colorbar.pdf"
            colorbarbase="${colorbar%.*}"
            outputcolor="$colorbarbase""-converted.pdf"
            echo "$filename"
            echo "$colorbar"
            echo "$outputcolor"
            pdfjam --outfile "$outputcolor" --papersize '{1800px,360px}'  "$colorbar"
            mv "$outputcolor" "$colorbar"
            pdfcrop --margins "3416 10 3416 50" "$colorbar" "$output"
            mv "$output" "$colorbar"
            convert -append "$filename" "$colorbar" "$final_name"
            convert "$final_name" "${basename}"".jpg"
            rm "$filename"
        fi
    done
done
# cd "../../../scripts" || exit
