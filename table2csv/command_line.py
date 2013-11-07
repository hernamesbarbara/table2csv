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
from tf1 import get_soup, find_biggest_group_of_tables, find_nth_from_top, dump_to_stdout

def valid(params):
    url = params.get('<url>', False)
    nth = params.get('--nth', False)
    if not url:
        return False
    else:
        return (nth and nth.isdigit()) or (not nth)

def figure_out_what_to_do(params):
    nth = params.get('--nth')
    func = None
    if nth:
        def func(soup):
            return find_nth_from_top(soup, int(nth))
    else:
        func = find_biggest_group_of_tables
    return func

def main():
    arguments = docopt(__doc__, version='table2csv  0.1')
    err = None
    if not valid(arguments):
        err = 'Unable to interpret cmd.\nPlease try again.\n\n'
        sys.exit(err+__doc__)
    soup = get_soup(arguments['<url>'])
    if soup is None:
        err = "Call to `get_soup` returned `None`.\nYou sure there's a table one that page?\n\n"
        sys.exit(err+__doc__)
    try:
        f = figure_out_what_to_do(arguments)
    except:
        err = 'Unable to interpret cmd.\nPlease try again.\n\n'
        sys.exit(err+__doc__)
    df = f(soup)
    if df is None or len(df) == 0:
        err = 'No tables found.\n\n'
        sys.exit(err+__doc__)
    dump_to_stdout(df)
    sys.exit(0)

if __name__ == '__main__':
    main()
