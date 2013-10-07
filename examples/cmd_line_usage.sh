#!/bin/bash
# this should be run from the root folder
# run with this cmd
#    ./examples/./cmd_line_usage.sh

python table2csv.py \
    http://en.wikipedia.org/wiki/List_of_apocalyptic_and_post-apocalyptic_fiction \
    --links 3 \
    --save post_apocalyptic_fiction.csv ;