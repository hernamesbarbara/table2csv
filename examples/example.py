#!/usr/bin/env python
# -*- coding: utf-8 -*-
import table2csv

url = 'http://lawandorder.wikia.com/wiki/Law_%26_Order_episodes'

soup = table2csv.get_soup(url)
df = table2csv.find_nth_from_top(soup, 2) # df is a pandas dataframe
table2csv.dump_to_stdout(df)

url = 'http://en.wikipedia.org/wiki/List_of_Law_%26_Order%3A_Special_Victims_Unit_episodes'
soup = table2csv.get_soup(url)
df = table2csv.find_biggest_group_of_tables(soup)
table2csv.dump_to_stdout(df)
