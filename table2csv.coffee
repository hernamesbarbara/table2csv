doc = """table2csv

Usage:
  table2csv <html> [-c=<colnums>] [-l=<linknums>] [--target=<t>] [(--save <f>) | -p]

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

"""
{docopt} = require 'docopt'
colors   = require 'colors'
{spawn}  = require 'child_process'

colors.setTheme({
  silly: 'rainbow',
  input: 'grey',
  verbose: 'cyan',
  prompt: 'grey',
  info: 'green',
  data: 'grey',
  help: 'cyan',
  warn: 'yellow',
  debug: 'blue',
  error: 'red'
})

params = docopt(doc, version: '1.0.0rc2')

src = params['<html>']
target = params['--target']
save = '--save' of params and params['--save']
outfile = params['<f>']
columns = params['--columns']
links = params['--links']

params = ['table2csv.py', src]

if columns
        params.push '--columns'
        params.push columns
if links
        params.push '--links'
        params.push links
if save
    params.push '--save'
    if not outfile
        params.push ''
    else
        params.push outfile



table2csv = spawn 'python', params

DATA = ''
table2csv.stdout.on "data", (chunk) ->
    DATA += chunk

table2csv.stdout.on "end", () ->
    results = JSON.parse DATA
    for doc in results
        output = switch doc.level
            when 'input' then doc.message.input
            when 'info' then doc.message.info
            when 'data' then doc.message.data
            when 'warn' then doc.message.warn
            when 'error' then doc.message.error
            else doc.message

        console.log output
