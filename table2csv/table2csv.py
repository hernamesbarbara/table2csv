#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""table2csv

Usage:
  table2csv <url> [--nth=<i>]

Options:
    --nth=<i>    Nth table from the top of the page.
"""

from docopt import docopt

def valid(params):
    url = params.get('<url>', False)
    nth = params.get('--nth', False)
    if not url:
        return False
    else:
        return (nth and nth.isdigit()) or (not nth)

def figure_out_what_to_do(params):
    nth = params.get('--nth')
    if nth:
        def func(soup):
            return find_nth_from_top(soup, int(nth))
    else:
        func = find_biggest_group_of_tables
    return func

if __name__ == '__main__':
    arguments = docopt(__doc__, version='table2csv  0.1')
    err = 'I dont know how to process that command.\nPlease try again.\n\n'
    if not valid(arguments):
        exit(err+__doc__)
    import requests
    from bs4 import BeautifulSoup
    from tf1 import find_biggest_group_of_tables, find_nth_from_top, dump_to_stdout, get_soup
    soup = get_soup(arguments['<url>'])
    try:
        f = figure_out_what_to_do(arguments)
    except:
        f = None
    if soup is None or f is None:
        exit(err+__doc__)
    df = f(soup)
    if df is None or len(df) == 0:
        exit('No tables found.\n\n'+__doc__)
    else:
        dump_to_stdout(df)
        exit()


