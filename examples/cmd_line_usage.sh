#!/bin/bash

python table2csv.py \
    http://en.wikipedia.org/wiki/List_of_apocalyptic_and_post-apocalyptic_fiction \
    --links 3 \
    --save post_apocalyptic_fiction.csv ;