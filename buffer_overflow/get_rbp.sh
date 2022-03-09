#!/bin/bash

# Get RBP using gdb on function $2 from binary $1, where $1 and $2 are first and second command line args respectively
(echo "break $2";
echo "set logging file $1_$2.txt";
echo "set logging on";
echo "run";
echo "i r $rbp";) | gdb $1 &> /dev/null

printf "0x%x" $(sed -n "s/.*rbp.* //p" $1_$2.txt)

rm -rf "$1_$2.txt"
