#!/bin/bash
COUNTER=1
for URL in $(cat urls)
    do
        echo GET $URL
        OUTFILE="outfile_${COUNTER}.txt"
        table2csv $URL > $OUTFILE
        echo Saved $OUTFILE
        COUNTER=$((COUNTER + 1)) # bump the counter += 1

    done