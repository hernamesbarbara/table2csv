### table2csv

Simple script for downloading html tables as csv.

#### A quick review:

    python table2csv.py \
        http://en.wikipedia.org/wiki/List_of_apocalyptic_and_post-apocalyptic_fiction \
        --save post_apocalyptic_fiction.csv ;

You can optionally specify columns with links to extract. For example, here we indicate that the third column (index 2) contains links that we want
    
    python table2csv.py http://lawandorder.wikia.com/wiki/Law_%26_Order_episodes \
        --columns 1,2,3,4 \
        --links 2 \
        --save lawandorder.csv ;

#### Features
Very limited at this point

* Identifies all the tables on the page as best it can
* Merges tables that share same structure (e.g. same column headers get merged)
* Figures out which table is the biggest
* extracts text
* extracts links (optionally)

#### TODO

* add the ability to specify which table on the page you would like to download (not just the biggest one)
* add support for columns that do not use proper `<th>` tags for headers (i.e. imperfect html tables)
* detect the data types found within each column
* add support for tables with hierarchical indices on the rows and/or columns 

[View on Github](https://github.com/hernamesbarbara/table2csv/)