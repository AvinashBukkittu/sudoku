#!/bin/bash
count=1
while IFS='' read -r line || [[ -n "$line" ]]; do
    #echo "Text read from file: $line"
    echo "Executing sudoku $count"
    python sudoku.py $line
    count=$((count+1))
done < "$1"