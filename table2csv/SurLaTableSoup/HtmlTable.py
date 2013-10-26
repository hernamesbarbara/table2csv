#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import Tag
from .HtmlSrcError import HtmlSrcError, raise_src_err
from utils import *

class HtmlTable(object):
    def __init__(self, soup, discover_links=False):
        self._drop_first_row = False
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
        if self.soup.find('th'):
            headers = [th for th in self.soup.find_all('th')]
        else:
            self._drop_first_row = True
            headers = [td for td in self.soup.find('tr')]

        if not headers or len(headers) == 0:
            return None
        headers = [th.get_text() for th in headers if isinstance(th, Tag)]
        headers = [rm_punct(h) for h in headers]
        if self.headers is None and len(headers) > 0:
            self.headers = headers
            return headers
        else:
            return None

    def find_rows(self):
        rows = []
        for i, tr in enumerate(self.soup.find_all('tr')):
            if i == 0 and self._drop_first_row:
                continue
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
        for i, tr in enumerate(self.soup.find_all('tr')):
            if i == 0 and self._drop_first_row:
                continue
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

    def astype(self, output_type='list', columns=[], link_columns=[]):
        """
        Convert table to a list of dicts

        Arguments:
            columns
                list of col indices you want to return in dict.
            link_columns
                list of col indices w/ hyperlinks you want to return in dict.
        Examples:
            1. return columns 2-5 as dictionary.
                In [158]: table.astype('list', columns=[1,2,3,4])

            2. Include content and links from the third column.
                In [159]: table.astype('list', columns=[2], link_columns=[2])
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
