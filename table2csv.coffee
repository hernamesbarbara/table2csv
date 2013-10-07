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

if not ('<html>' of params)
    process.exit 1
else
    src = params['<html>']
    target = params['--target']
    save = '--save' of params and params['--save']
    outfile = params['<f>']
    columns = params['--columns']
    links = params['--links']

    console.log 'Reading '.info + src.input + ' as html'.info
    params = ['table2csv.py', src]
    if columns
            params.push '--columns ' + columns
    if links
            params.push '--links ' + links
    if save
        params.push '--save'
        if not outfile
            console.log 'Provide a filename to save results.'.error
            process.exit(1)
        else
            params.push outfile

table2csv = spawn 'python', params

table2csv.stdout.on "data", (data) ->
    if data.toString().trim() == 'DONE'
        console.log 'DONE'.info

    else
        console.log data.toString().trim().data

table2csv.stderr.on "data", (data) ->
    console.log data.toString().trim().error
