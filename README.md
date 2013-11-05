### table2csv

Simple script for downloading html tables as csv.

#### A quick review:

```python

python table2csv.py \
    http://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2011/crime-in-the-u.s.-2011/tables/table-2 >> dump.txt
```

#### Features
* accepts a URL
* Identifies all the tables
* Merges tables that share same structure (e.g. same column headers get merged)
* Figures out which table is the biggest
* extracts text
* extracts links

#### TODO

* add the ability to specify which table on the page you would like to download (not just the biggest one)
* ~~add support for columns that do not use proper `<th>` tags for headers (i.e. imperfect html tables)~~
* detect the data types found within each column
* add support for tables with hierarchical indices on the rows and/or columns 

[View on Github](https://github.com/hernamesbarbara/table2csv/)