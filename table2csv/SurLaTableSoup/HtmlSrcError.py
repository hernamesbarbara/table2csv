#!/usr/bin/env python
# -*- coding: utf-8 -*-
class HtmlSrcError(Exception): pass

def raise_src_err(markup=""):
    "raises an error if the input markup cant be understood."
    if markup is None or markup == '':
        markup = '`NoneType` or `""` (Empty String)'
    else:
        markup = '`{0}`'.format(markup)
    msg = """
Unable to interpret resource {0} as html.
Please use valid URL, a local html file, or raw html markup.
    """.format(markup[:200])
    raise HtmlSrcError,msg
