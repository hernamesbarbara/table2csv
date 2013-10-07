#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""table2csv

Usage:
  table2csv <html> [--columns=<c>] [--links=<l>] [--target=<t>] [(--save <f>) | -p]
  table2csv [-h | --help]

Options:
    <html>                     URL, html file, or raw input.
    -c --columns=<c>           Which columns you want.
    -l --links=<l>             Which columns have links that you want.
    -t --target=<t>            Which table you want [default: biggest].
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

import os
from string import punctuation
import re
import lxml
from bs4 import BeautifulSoup
import requests
from collections import defaultdict

def rm_non_ascii(s):
    "remove any non ascii characters"
    if not isinstance(s, basestring):
        return s
    s = s.strip()
    s = "".join(filter(lambda x: ord(x)<128, s))
    return str(s)

def rm_punct(txt):
    txt = rm_non_ascii(txt).strip()
    s = "".join([c for c in txt if c not in punctuation])
    return s

def snakify(txt):
    "downcases and puts text into snake_case"
    s = rm_punct(txt)
    s = "_".join(s.split()).lower()
    return s

def is_html(txt):
    return "doctype" in txt.lower() and "html" in txt.lower()

def is_url(url_or_html):
    "returns True if string is a valid url"
    parsed = requests.utils.urlparse(url_or_html)
    return parsed.scheme == 'http'

def is_local_file(url_or_html):
    return os.path.isfile(url_or_html)

class HtmlTable(object):
    def __init__(self, soup, discover_links=False):
        self.soup = soup
        self.rows = None
        self.headers = None
        self.links = None
        self.find_headers()
        self.find_rows()
        self.discover_links()

    def __len__(self):
        return 0 if not self.rows else len(self.rows)

    def nrow(self):
        return len(self)

    def ncol(self):
        return None if not self.headers else len(self.headers)

    def find_headers(self):
        headers = [th for th in self.soup.find_all('th')]
        if not headers or len(headers) == 0:
            return None
        headers = [th.get_text() for th in headers]
        headers = [rm_punct(h) for h in headers]
        if self.headers is None and len(headers) > 0:
            self.headers = headers
            return headers
        else:
            return None

    def find_rows(self):
        rows = []
        for tr in self.soup.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                row.append(td.get_text())
            if len(row) == self.ncol():
                row = [rm_punct(cell) for cell in row]
                rows.append(row)
        if self.rows is None and len(rows) > 0:
            self.rows = rows
            return rows
        else:
            return None

    def discover_links(self):
        rows = []
        for tr in self.soup.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                links = []
                for a in td.find_all('a'):
                    links.append(a.get('href', ''))

                links = ','.join(links)
                row.append(links)

            if len(row) == self.ncol():
                rows.append(row)

        if self.links is None and len(rows) > 0:
            self.links = rows
            return rows
        else:
            return None

    def astype(self, output_type, columns=[], link_columns=[]):
        "convert table to a list of dicts"
        """
        Arguments:
            columns
                list of col indices you want to return in dict.
            link_columns
                list of col indices w/ hyperlinks you want to return in dict.
        Examples:
            1. return columns 2-5 as dictionary.
                In [158]: table.astype(columns=[1,2,3,4])

            2. Include content and links from the third column.
                In [159]: table.astype(columns=[2], link_columns=[2])
        """
        if len(columns) == 0:             # if columns are not provided
            columns = range(self.ncol())  # defaults to all columns

        if self.headers:
            keys = [self.headers[i] for i in columns]
        else:
            keys = map(str,columns)

        if link_columns:
            link_keys = [self.headers[i] for i in link_columns]
            keys += [snakify(k)+'_href' for k in link_keys]

        res = []
        for i, row in enumerate(self.rows):
            values = row[min(columns):max(columns)+1]

            if link_columns:
                selected = self.links[i]
                links = [selected[j] for j in link_columns]
                values += links

            if len(values) == len(keys):
                if output_type == "dict":
                    res.append(dict(zip(keys,values)))
                else:
                    res.append(values)
        return res

    def __str__(self):
        msg = """HtmlTable
nrow: {0}
ncol: {1}""".format(self.nrow(), self.ncol())
        return msg

    def __repr__(self):
        return str(self)

    def append(self, value):
        if not isinstance(value, HtmlTable):
            raise ValueError("`HtmlTable.append` accepts only `HtmlTable`")
        if not self.headers == value.headers:
            raise ValueError("Unable to merge two tables with different headers")
        self.rows.extend(value.rows)
        self.links.extend(value.links)

class HtmlSrcError(Exception): pass

def raise_src_err(markup=""):
    "raises an error if the input markup cant be understood."
    msg = """
    Unable to interpret resource `{0}` as html.
    Please use valid URL, a local html file, or raw html markup.
    """.format(markup[:200])
    raise HtmlSrcError,msg

class SurLaTableSoup(BeautifulSoup):

    def __init__(self, html, css={}):
        self.css = css
        self.html = self.process_input_markup(html)
        super(SurLaTableSoup, self).__init__(self.html)
        self.rawtables = [t for t in self.find_all('table', attrs=self.css)]
        self.tables = None
        self._group_tables()

    def process_input_markup(self,txt):
        "interpret url, local file, or raw html markup"
        markup = txt if is_html(txt) else None
        if markup is not None:
            return markup
        if is_url(txt):
            r = requests.get(txt)
            if r.status_code == 200:
                markup = r.content
        elif is_local_file(txt):
            markup = open(txt,'rb').read()
        if not is_html(markup):
            raise_src_err(markup)
        return markup

    def __len__(self):
        return len(self.rawtables)

    def __iter__(self):
        return iter(self.rawtables)

    def first(self):
        return None if not len(self) else self.rawtables[0]

    def last(self):
        return None if not len(self) else self.rawtables[-1]

    def __str__(self):
        msg = """SurLaTableSoup with ({0}) tables"""
        return msg.format(len(self))

    def _hash_headers(self, strings):
        if strings is None:
            return ""
        return '|'.join(sorted([snakify(s) for s in strings if len(s)]))

    def _group_tables(self):
        if not len(self):
            return "No tables found."
        distinct_tables = defaultdict(list)
        for i, table in enumerate(self):
            table = HtmlTable(table)
            hh = self._hash_headers(table.headers)
            distinct_tables[hh] += [table]
        self.tables = dict(distinct_tables)
        return self.tables

    def _describe_table(self, table_headers):
        if isinstance(table_headers, list):
            hh = self._hash_headers(table_headers)
        else:
            hh = table_headers
        selected = self.tables[hh]
        headers = selected[0].headers
        n_tables = len(selected)
        n_rows = sum([len(t) for t in selected])
        return [headers,n_tables,n_rows]

    def _has_most_rows(self):
        row_cnt = []
        keys = []
        for key in self.tables:
            headers,n_tables,n_rows = self._describe_table(key)
            row_cnt.append(n_rows)
            keys.append(key)
        max_rows = [hh for (hh,n) in zip(keys,row_cnt) if n == max(row_cnt)]
        if len(max_rows) == 1:
            table_with_most_rows = self.tables[max_rows[0]]
            return table_with_most_rows[0].headers
        else:
            raise Exception("More than 1 table having the same number of rows")

    def _describe_page(self):
        msg = """
headers: {0}
n_tables: {1}
n_rows: {2}"""
        summary = []
        for key in self.tables:
            headers,n_tables, n_rows = self._describe_table(key)
            summary.append(msg.format(headers, n_tables, n_rows))
        return summary

    def describe(self):
        summary = "\n".join(self._describe_page())
        return summary + "\n"

    def merge_tables_with(self,headers):
        if isinstance(headers, list):
            hh = self._hash_headers(headers)
        else:
            hh = headers
        selected = self.tables[hh]
        for i , table in enumerate(selected):
            if i == 0:
                merged = table
            else:
                merged.append(table)
        return merged

    def extract_biggest_table(self):
        headers = self._has_most_rows()
        biggest = self.merge_tables_with(headers)
        return biggest


def save_csv(data,outfile):
    import csv
    keys = list(set([ k for doc in data for k in doc.keys()]))
    print "Number of records found: %d" % len(data)
    print "Extracting %d columns" % len(keys)
    print ",".join(keys)
    print "saving...",
    try:
        print outfile
        f = open(outfile, 'wb')
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writer.writerow(keys)
        dict_writer.writerows(data)

    except Exception,err:
        print outfile
        raise

if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__, version='table2csv  0.1')
    source_html = arguments.get('<html>', False)

    if not source_html:
        exit("Please provide URL, html file, or raw html as input")

    save = arguments.get("--save")
    outfile = arguments.get("<f>", False)

    if save and not outfile:
        exit("Provide a filename to save results.")

    soup = SurLaTableSoup(source_html)

    if not soup:
        exit("Trouble interpreting input html. Soup not found.")

    if not len(soup.tables):
        exit("No tables found.")

    print soup.describe()

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
        if params is not None:
            records = table.astype('dict',**params)
        else:
            records = table.astype('dict')

        if save and outfile:
            save_csv(records, outfile)
        else:
            exit(records)



