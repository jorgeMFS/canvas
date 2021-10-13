#!/bin/bash
#
./GeCo3 $PARAMR -r $2 $1 

function RunGeCo3 {
    PARAMR=" -rm 20:500:1:35:0.95/3:100:0.95 -rm 13:200:1:1:0.95/0:0:0 -rm 10:10:0:0:0.95/0:0:0 -lr 0.03 -hs 64 ";
    PARAMH=" -rm 20:500:1:35:0.95/3:100:0.95 -rm 13:200:1:1:0.95/0:0:0 -rm 10:10:0:0:0.95/0:0:0 -tm 4:1:0:1:0.9/0:0:0 -tm 17:100:1:10:0.95/2:20:0.95 -lr 0.03 -hs 64 ";
   # 1 - TARGET
   # 2 - REFERENCE
if test -f "../../datasets/$1" && test -f "../../datasets/$2"; then
   cp ../../datasets/$1 .
   cp ../../datasets/$2 .
   rm -f $1.co
   (/usr/bin/time -v ./GeCo3 $PARAMR -r $2 $1 ) &> ../../results/C_GECO3R_REFO_$1-$2
   ls -la $1.co | awk '{ print $5;}' > ../../results/BC_GECO3R_REFO_$1-$2

   (/usr/bin/time -v ./GeCo3 $PARAMH -r $2 $1 ) &> ../../results/C_GECO3H_REFO_$1-$2
   ls -la $1.co | awk '{ print $5;}' > ../../results/BC_GECO3H_REFO_$1-$2
   rm -f $2 $1 $1.co;
fi
}