#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
COUNTER=1
for URL in $(cat $DIR/urls)
    do
        echo "GET $URL"
        OUTFILE="outfile_${COUNTER}.txt"
        echo "Saving to $OUTFILE"
        `python $DIR/../tf1.py $URL > $DIR/$OUTFILE`
        COUNTER=$((COUNTER + 1)) # bump the counter += 1
    done