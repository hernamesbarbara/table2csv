#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""table2csv

Usage:
  table2csv <html> [--columns=<c>] [--links=<l>] [--target=<t>] [(--save <f>) | -p]
  table2csv [-h | --help]

Arguments:
    <html>                     URL, html file, or raw input.
    -c --columns=<colnums>     Which columns you want.
    -l --links=<linknums>      Which columns have links that you want.
    -t --target=<t>            Which table you want [default: biggest].

Options:
    -s --save                  Save.
    -p --print                 Print.
    <f>                        Output filename required for save.
    -h --help                  Show help message.

Examples:
    python table2csv.py http://lawandorder.wikia.com/wiki/Law_%26_Order_episodes \
        --columns 1,2,3,4 \
        --links 2 \
        --save lawandorder.csv ;

    python table2csv.py \
        http://en.wikipedia.org/wiki/List_of_apocalyptic_and_post-apocalyptic_fiction \
        --links 3 \
        --save post_apocalyptic_fiction.csv ;

About:
    Author: @austinogilvie
    Date: 2013
    Name: table2csv
    Version: 0.1
    URL: https://github.com/hernamesbarbara/table2csv/
"""
from SurLaTableSoup import SurLaTableSoup
from utils import *
import sys

SEP = '|'
messages = []

def main():
    from docopt import docopt
    arguments = docopt(__doc__, version='table2csv  0.1')
    source_html = arguments.get('<html>', False)
    messages.append({'level':'info', 'message': "reading html..."})
    messages.append({'level':'info', 'message': source_html})

    if not source_html:
        messages.append({'level':'error', 'message': 'no html provided.'})
        return messages

    save = arguments.get("--save")
    outfile = arguments.get("<f>", False)

    if save and not outfile:
        messages.append({'level':'error', 'message': 'no outfile provided.'})
        return messages
    try:
        soup = SurLaTableSoup(source_html)
    except:
        messages.append({'level':'error', 'message': 'couldnt make the soup.'})
        return messages

    if not len(soup.tables):
        messages.append({'level':'warn', 'message': 'no tables found on this page.'})
        return messages

    target = arguments.get("--target")
    if target != "biggest":
        msg = """
table2csv can only find the biggest table on the page at this time."""
        raise NotImplementedError(msg)
    else:
        columns = arguments.get('--columns', False)
        params = None
        if columns and columns != '':
            columns = map(int,columns.split(','))
            params = {"columns": columns}

        links = arguments.get('--links', False)
        if links and links != '':
            links = map(int,links.split(','))
            if params is not None:
                params.update({"link_columns": links})
            else:
                params = {"link_columns": links}

        table = soup.extract_biggest_table()

        if save and outfile:
            if params is not None:
                records = table.astype('dict',**params)
            else:
                records = table.astype('dict')
            save_csv(records, outfile)
            messages.append({'level':'info', 'message': 'saving...%s' % outfile})
            messages.append({'level':'info', 'message': 'DONE!'})
            return messages

        else:
            if params is not None:
                records = table.astype('list', **params)
            else:
                records = table.astype('list')

            records = [SEP.join(row) for row in records]
            headers = SEP.join(table.headers) + '\n'
            rows = '\n'.join(records)
            res = headers + rows
            messages.append({'level':'data', 'message': res})
            messages.append({'level':'info', 'message': 'DONE!'})
            return messages

if __name__ == '__main__':
    import ujson as json
    try:
        result = main()
    except NotImplementedError, err:
        messages.append({'level':'error', 'message': err.message})
    sys.stdout.write(json.dumps(messages))
    sys.exit()
