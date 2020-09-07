#!/bin/sh
[ -d chosen_structures ] && rm -r chosen_structures
structs=$(cat data/chosen_structures.csv | sed '1d' | awk -F"," '{print $1}')
mkdir -p chosen_structures
printf "%s\n" $structs | xargs -I{} cp clusters/cluster-{}.xyz chosen_structures
