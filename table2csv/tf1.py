#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tf1.py
Module with various faculties for extracting html tables to csv.
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
import string
import sys
import warnings

def rm_non_ascii(s):
    """
    remove any non ascii characters
    """
    if not isinstance(s, basestring):
        return s
    s = s.strip()
    s = ''.join(filter(lambda x: ord(x)<128, s))
    return str(s)

def rm_punct(txt):
    """
    remove all punctuation except for underscore.
    """
    txt = txt.strip().replace('\n', ' ')
    txt = rm_non_ascii(txt).strip()
    exclude = ''.join(ch for ch in string.punctuation if ch != '_')
    s = ''.join([c for c in txt if c not in exclude])
    return s

def rm_quotes(txt):
    if not isinstance(txt, basestring):
        return txt
    return ''.join(ch for ch in txt if ch != '"')

def snakify(txt):
    """
    downcases and swap spaces for underscore.
    """
    if not isinstance(txt, basestring):
        txt = str(txt)
    s = rm_punct(txt)
    s = '_'.join(s.split()).lower()
    return s

def add_column(colname, suffix):
    return colname+'_'+suffix

def get_soup(url):
    try:
        r = requests.get(url)
        return BeautifulSoup(r.text, "html.parser") if r.status_code == 200 else None
    except:
        return None

def count_tables(soup):
    return len(list(soup.find_all('table')))

def has_tables(soup):
    return count_tables(soup) > 0

def find_all_tables(soup):
    return [table for table in soup.find_all('table')]

def find_nth_from_top(soup, nth_table):
    """
    Find all tables on the page. Return the nth from the top.
    """
    all_tables = find_all_tables(soup)
    if not all_tables:
        return None
    table = all_tables[int(nth_table)-1]
    return to_dataframe(table)

def find_biggest_single_table(soup):
    """
    Find all tables on the page. Return the biggest as a DataFrame.
    """
    all_tables = find_all_tables(soup)
    if not all_tables:
        return None
    lengths = [len(table) for table in all_tables]
    max_length = max(lengths)
    biggest_idx = lengths.index(max_length)
    table = all_tables[biggest_idx]
    return to_dataframe(table)

def extract_txt(tag):
    return [el.get_text().strip() for el in tag if isinstance(el, Tag)]

def extract_links(tag, sep=','):
    cells = extract_txt(tag)
    links_lists = [el.find_all('a') for el in tag if isinstance(el, Tag)]
    hrefs = [sep.join([a.attrs.get('href', '') for a in links]) for links in links_lists]
    return hrefs

def extract_all_data(table):
    data = []
    if isinstance(table, Tag):
        table = [tr for tr in table.find_all('tr')]
    for i, row in enumerate(table):
        if i == 0:
            colnames = extract_txt(row)
            colnames += map(lambda x: add_column(x, suffix='link'), colnames)
            data.append(colnames)
        else:
            row_values = extract_txt(row)
            row_values += extract_links(row)
            if len(row_values) == len(colnames):
                data.append(row_values)
    return data

def to_dataframe(table):
    """
    Takes a list of lists. Returns a DataFrame. Assumes columns are in table[0].
    """
    data = extract_all_data(table)
    if len(data) < 2:
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(data[1:], columns=data[0])
    # drop columns which are entirely null
    # mostly this will be link columns we've added which never have links
    df = df.replace({'': None})
    df.columns = map(snakify, df.columns)
    df = df.apply(lambda x: x.apply(rm_quotes)) # rm double quoted strings
    df = df.apply(lambda x: x.str.replace('\n', ' '), axis=1) # rm new lines
    return df

def hash_column_names(columns):
    """
    Returns a pipe delimited ('hashed') representation of a list.
    """
    columns = sorted(columns)
    columns = map(snakify, columns)
    return ','.join([str(col) for col in columns])

def consolidate(tables):
    """
    Takes a list of DataFrames. Returns a dictionary.

    Returns:
        {'col_a|col_b': df}
    """
    if not all([isinstance(table, pd.DataFrame) for table in tables]):
        tables = [to_dataframe(table) for table in tables]
    grouped = {}
    for table in tables:
        hashcols = hash_column_names(table.columns)
        if hashcols not in grouped:
            grouped[hashcols] = table
        else:
            grouped[hashcols] = grouped[hashcols].append(table)
    return grouped

def find_biggest_group_of_tables(soup):
    """
    Takes a soup. Returns a DataFrame.
    Args:
        soup => BeautifulSoup
    Returns:
        The biggest DataFrame resulting in a consolidation of all like tables
        found on the page.
    """
    tables = find_all_tables(soup)
    if not tables:
        return None
    grouped = consolidate(tables)
    groups = grouped.values()
    lengths = [len(group) for group in groups]
    max_length = max(lengths)
    biggest_idx = lengths.index(max_length)
    if lengths.count(max_length) > 1:
        msg = """The biggest table on this page has {nrow} rows.
                        {n_tables} tables have the same # of rows. Extracting the 1st one."""
        warnings.warn(msg.format(nrow=max_length, n_tables=lengths.count(max_length)))
    return groups[biggest_idx].reset_index(drop=1)

def dump_to_stdout(frame, drop_missing=True, sep=','):
    if drop_missing:
        frame = frame.dropna(how='all', axis=1)
    try:
        frame.to_csv(sys.stdout, sep=sep, index=False, encoding='utf-8')
    except:
        sys.stdout.write("couldn't save the file")
