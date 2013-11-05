#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""table2csv

Usage:
  table2csv <url> [--nth=<i>]

Options:
    --nth=<i>    Nth table from the top of the page.
"""

from docopt import docopt

def main():
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    df = func(soup)
    dump_to_stdout(df)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='table2csv  0.1')
    url = arguments.get('<url>', False)
    nth = arguments.get('--nth', False)
    if url:
        from tf1 import *
        if nth:
            def func(soup):
                return find_nth_from_top(soup, int(nth))
        else:
            func = find_biggest_group_of_tables
        main()
