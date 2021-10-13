#!/bin/bash
#

mkdir -p "../Canvas.github.pages/groups/"

while read -r virus;
    do
    if [[ -f "../Canvas.github.pages/ir_plot/"$virus".jpg" ]]
        then
            if [[ -f ../Canvas.github.pages/trees/$virus.png ]]
            then            
            mkdir -p "../Canvas.github.pages/groups/$virus";
            cp "../Canvas.github.pages/figure/$virus.jpg"  "../Canvas.github.pages/groups/$virus/1.jpg"
            cp "../Canvas.github.pages/ir_plot/$virus.jpg"  "../Canvas.github.pages/groups/$virus/2.jpg"
            cp "../Canvas.github.pages/trees/$virus.png"  "../Canvas.github.pages/groups/$virus/3.png"
        fi
    fi
done < A
exit;

for entry in "../Canvas.github.pages/figure/"/*
do
  echo "$entry"
done