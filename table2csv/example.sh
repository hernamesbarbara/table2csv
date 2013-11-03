#!/bin/bash
COUNTER=1
for URL in $(cat urls.txt)
    do
        OUTFILE="outfile_${COUNTER}.txt"
        python tf1.py $URL > $OUTFILE
        COUNTER=$((COUNTER + 1)) # bump the counter += 1
    done