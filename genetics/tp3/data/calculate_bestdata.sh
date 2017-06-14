#!/bin/bash -xe
PATH=$(dirname $0)
FULLDATA="$PATH/fulldata"
BESTDATA="$PATH/bestdata"
SAMPLE=1000

PATH=$PATH:/bin:/usr/bin
export PATH

for file in armas botas cascos guantes pecheras
do
    FROM="$FULLDATA/$file.tsv"
    TO="$BESTDATA/$file.tsv"
    head -n1 $FROM > $TO #truncate file to headers
    for column in 2 3 4 5 6
    do
        sort -rn -t $'\t' -k$column $FROM | head -n$SAMPLE >> $TO #keep a sample
    done
done
