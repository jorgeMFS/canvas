#!/bin/bash
#
RUN_COMP=1;
RUN_PLOT=1;
#
# ==============================================================================
#
if [[ "$RUN_COMP" -eq "1" ]]; then
  declare -a NAMES=( "ALBRECHT_DURER" "AMEDEO_MODIGLIANI" "ANDREA_MANTEGNA" "ANDY_WARHOL" "ARSHILLE_GORKY" "CAMILLE_COROT" "CARAVAGGIO" "CASPAR_DAVID_FRIEDRICH" "CLAUDE_LORRAIN" "CLAUDE_MONET" "DANTE_GABRIEL_ROSSETTI" "DAVID_HOCKNEY" "DIEGO_VELAZQUEZ" "EDGAR_DEGAS" "EDVARD_MUNCH" "EDWARD_HOPPER" "EGON_SCHIELE" "EL_LISSITZKY" "EUGENE_DELACROIX" "FERNAND_LEGER" "FRANCISCO_DE_GOYA" "FRANCISCO_DE_ZURBARAN" "FRANCIS_BACON" "FRANS_HALS" "FRANZ_MARC" "FRA_ANGELICO" "FRIDA_KAHLO" "Frederic_Edwin_Church" "GENTILESCHI_ARTEMISIA" "GEORGES_BRAQUE" "GEORGES_DE_LA_TOUR" "GEORGES_SEURAT" "GEORGIA_OKEEFE" "GERHARD_RICHTER" "GIORGIONE" "GIORGIO_DE_CHIRICO" "GIOTTO_DI_BONDONE" "GUSTAVE_COURBET" "GUSTAVE_MOREAU" "GUSTAV_KLIMT" "HANS_HOLBEIN_THE_YOUNGER" "HANS_MEMLING" "HENRI_MATISSE" "HIERONYMUS_BOSCH" "JACKSON_POLLOCK" "JACQUES-LOUIS_DAVID" "JAMES_ENSOR" "JAMES_MCNEILL_WHISTLER" "JAN_VAN_EYCK" "JAN_VERMEER" "JASPER_JOHNS" "JEAN-ANTOINE_WATTEAU" "JEAN-AUGUSTE-DOMINIQUE_INGRES" "JEAN-MICHEL_BASQUIAT" "JEAN_FRANCOIS_MILLET" "JOACHIM_PATINIR" "JOAN_MIRO" "JOHN_CONSTABLE" "JOSEPH_MALLORD_WILLIAM_TURNER" "KAZIMIR_MALEVICH" "LUCIO_FONTANA" "MARC_CHAGALL" "MARK_ROTHKO" "MAX_ERNST" "NICOLAS_POUSSIN" "PAUL_CEZANNE" "PAUL_GAUGUIN" "PAUL_KLEE" "PETER_PAUL_RUBENS" "PIERRE-AUGUSTE_RENOIR" "PIETER_BRUEGEL_THE_ELDER" "PIET_MONDRIAN" "Picasso" "RAPHAEL" "REMBRANDT_VAN_RIJN" "RENE_MAGRITTE" "ROGER_VAN_DER_WEYDEN" "ROY_LICHTENSTEIN" "SALVADOR_DALI" "SANDRO_BOTTICELLI" "THEODORE_GERICAULT" "TINTORETTO" "TITIAN" "UMBERTO_BOCCIONI" "VINCENT_VAN_GOGH" "WASSILY_KANDINSKY" "WILLEM_DE_KOONING" "WILLIAM_BLAKE" "WILLIAM_HOGARTH" "WINSLOW_HOMER" "РDOUARD_MANET" )
  #
  #
  rm -f NC_AVERAGE_TMP;
  for i in "${NAMES[@]}"
  do
    SUM=`cat REPORT_COMPLEXITY | grep $i | awk 'BEGIN {t=0}; {t+=$3} END {print t}'`;
    CAR=`cat REPORT_COMPLEXITY | grep $i | wc -l`;
    printf "\"$i\"" >> NC_AVERAGE_TMP;
    echo "scale=8; ($SUM / $CAR)" | bc -l | awk '{printf "\t%f\t", $0}' >> NC_AVERAGE_TMP;
    printf "$CAR\n" >> NC_AVERAGE_TMP;
  done
  #
  sort -k 2 -V NC_AVERAGE_TMP > NC_AVERAGE;
  #
fi
# ==============================================================================
#
if [[ "$RUN_PLOT" -eq "1" ]]; then
  echo "set terminal pdfcairo enhance color
  set term pdfcairo font 'Tahoma,7'
  set key under nobox
  set style histogram clustered gap 1 title offset 1,0.25
  set style fill solid noborder
  unset xtics
  set output 'average.pdf'
  set auto
  set boxwidth 1
  set style fill solid 1.00
  set ylabel 'NC' font 'Tahoma,8'
  set xlabel 'Authors' font 'Tahoma,8'
  set grid ytics lc rgb '#C0C0C0'
  set key ins horiz font 'Tahoma,8'
  set key center top
  set style fill solid 1.0 border 0.5
  set xtics rotate nomirror
  set tics textcolor rgb 'black'
  set yrange[0:1]
  set y2range [0:57]
  set y2label 'Number of images' font 'Tahoma,8'
  set grid
  set ytics 0.2 nomirror font 'Tahoma,8'
  set y2tics 10 nomirror font 'Tahoma,8'
  plot 'NC_AVERAGE' using 3:xtic(1) title 'Number of images' with boxes lc rgb '#396AB1' linetype 2 axes x1y2, 'NC_AVERAGE' using 2:xtic(1) title 'Average NC' with boxes lc rgb '#cc0000' linetype 1 axes x1y1, 'NC_AVERAGE' using 4:xtic(1) title 'NCC' with boxes lc rgb 'white' linetype 2 axes x1y1, " | gnuplot -p
fi
#
# ==============================================================================
