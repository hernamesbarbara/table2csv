#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""table2csv

Usage:
  table2csv <url>

"""

from docopt import docopt

def main():
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    df = find_biggest_group_of_tables(soup)
    dump_to_stdout(df)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='table2csv  0.1')
    url = arguments.get('<url>', False)
    if url:
        from tf1 import *
        main()
