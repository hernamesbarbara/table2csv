#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""table2csv

Usage:
  table2csv <url> [--nth=<i>]

Options:
    --nth=<i>    Nth table from the top of the page.
"""

from docopt import docopt
import sys
from tf1 import find_biggest_group_of_tables, find_nth_from_top, dump_to_stdout, get_soup

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

def main(params):
    soup = get_soup(params['<url>'])
    err = 'I dont know how to process that command.\nPlease try again.\n\n'
    try:
        f = figure_out_what_to_do(params)
    except:
        f = None
    if soup is None or f is None:
        return (None, err)
    df = f(soup)
    if df is None or len(df) == 0:
        return (None, 'No tables found.\n\n')
    else:
        return (df, None)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='table2csv  0.1')
    if valid(arguments):
        df, err = main(arguments)
        if err:
            sys.exit(err+__doc__)
        dump_to_stdout(df)
        sys.exit()
    else:
        sys.exit('Something went wrong.\n\n'+__doc__)

