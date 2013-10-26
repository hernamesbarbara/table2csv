#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import string
import re
import requests

def rm_non_ascii(s):
    "remove any non ascii characters"
    if not isinstance(s, basestring):
        return s
    s = s.strip()
    s = "".join(filter(lambda x: ord(x)<128, s))
    return str(s)

def rm_punct(txt):
    txt = rm_non_ascii(txt).strip()
    s = "".join([c for c in txt if c not in string.punctuation])
    return s

def snakify(txt):
    "downcases and puts text into snake_case"
    s = rm_punct(txt)
    s = "_".join(s.split()).lower()
    return s

def is_html(txt):
    if txt is not None and len(txt):
        return "doctype" in txt.lower() and "html" in txt.lower()
    else:
        return False

def is_url(url_or_html):
    "returns True if string is a valid url"
    parsed = requests.utils.urlparse(url_or_html)
    return parsed.scheme == 'http'

def is_local_file(url_or_html):
    return os.path.isfile(url_or_html)

def save_csv(data, outfile):
    import csv
    keys = list(set([ k for doc in data for k in doc.keys()]))
    try:
        f = open(outfile, 'wb')
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writer.writerow(keys)
        dict_writer.writerows(data)
    except Exception,err:
        raise
