#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
import lxml
import requests
from bs4 import BeautifulSoup
from .HtmlSrcError import HtmlSrcError, raise_src_err
from .HtmlTable import HtmlTable
from utils import *

class SurLaTableSoup(BeautifulSoup):

    def __init__(self, html, css={}):
        self.css = css
        try:
            self.html = self.process_input_markup(html)
            super(SurLaTableSoup, self).__init__(self.html)
        except:
            raise TypeError('expected html')
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
            else:
                raise Exception("no html")
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
