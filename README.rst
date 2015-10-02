=========
table2csv
=========

Simple script for downloading html tables as csv.

Installation
============

.. code:: bash

    pip install -U table2csv

Usage
=====

.. code:: bash

    table2csv http://en.wikipedia.org/wiki/List_of_Super_Bowl_champions > dump.txt
    python -m table2csv.main http://en.wikipedia.org/wiki/List_of_Super_Bowl_champions > dump.txt

Use --nth=[int] to grab a certain table from the page.

Features
========

-  accepts a URL
-  Identifies all the tables
-  Merges tables that share same structure (e.g. same column headers get
   merged)
-  Figures out which table is the biggest
-  extracts text
-  extracts links

TODO
====

-  detect the data types found within each column
-  add support for tables with hierarchical indices on the rows and/or
   columns

`View on Github <https://github.com/hernamesbarbara/table2csv/>`__
