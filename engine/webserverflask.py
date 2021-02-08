#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Webserver

# get ip of visitors https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors
"""

import os
import sys
from engine.page import Page
from engine.conf import PATH_TO_HTML, PATH_TO_TEMPLATE_HTML, PATH_TO_TEMPLATE, PATH_TO_MD
from engine.postprocessing import add_head
from flask import Flask, redirect, url_for, send_from_directory, request

import subprocess
import re
import argparse

from flask import request
from flask import jsonify

from engine.searcher import search_term, Db, Header

# Open Access mode
try:
    from engine.open_access import OPEN_ACCESS  # inside this file OPEN_ACCESS = ['work-fenzymes.html']
except ImportError:
    OPEN_ACCESS = []

import platform

app = Flask(__name__, static_url_path='')

@app.route('/edit/<note_title>')
def edit(note_title):
    """Open a note with your edit"""
    if request.remote_addr not in ['127.0.0.1', '0.0.0.0']:
        return 'Hmm...'

    os.system('open ' + PATH_TO_MD + ' ' + note_title)
    return 'edit note: %s' % note_title

@app.route('/open_file/')
def open_file():
    import urllib
    import urllib.parse

    filename  = urllib.parse.unquote(request.args.get('file_path'))

    # for folder paths
    if '/' in filename: # so this is path
        cmd = 'open "' + filename + '" &'
        os.system(cmd)
        return jsonify(result="")

    if platform.system() == "Linux":
        cmd = 'locate ' + filename
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read().decode()

    if platform.system() == "Darwin":
        # out = commands.getoutput('glocate ' + filename)
        cmd = 'mdfind -name "' + filename + '"'
        print('\_ flask search with ', cmd)
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read().decode()

    first_hit = out.split('\n')[0]
    print('# of hits ' + str(len(out.split('\n'))) + " " + out.replace('\n',', '))
    if not first_hit:
        print('not found')
        return jsonify(result='Not found ' + filename)
    else:
        print('hit ' + first_hit)
        #cmd = 'open "/' + first_hit + '" &'
        cmd = 'open "' + first_hit + '" &'
        os.system(cmd)
        return jsonify(result="")


@app.route('/edit_header/<note_title>/<note_header>')
def edit_header(note_title, note_header, verbose=False):
    """
    edit_header::cmd: cd /Users/magnus/Dropbox/geekbook/notes/ && /usr/bin/grep -n '# h1 Heading' test.md
    edit_header::out: 11:# h1 Heading

    Old: grep

    grep -n 'May #2' *.md
    lifebook.md:7:# May #
    Open a note with your edit

    http://stackoverflow.com/questions/3139970/open-a-file-at-line-with-filenameline-syntax

    ..warning: if two headers found there will be a problem ;-)
    """
    #grep -n 'May #2' *.md
    if request.remote_addr not in ['127.0.0.1', '0.0.0.0']:
        return 'Hmm...'

    cmd = "cd '" + PATH_TO_MD + "' && /usr/bin/grep -n '" + note_header + "' '" + note_title + ".md'"
    if verbose: print('edit_header::cmd:', cmd)
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read().decode()
    if verbose: print('edit_header::out:', out)
    note_line = out.split(':')[0]
    cmd = 'emacsclient +' + note_line + ' "' + PATH_TO_MD + '/' + note_title + '.md" &'
    if verbose: print('Emacs cmd', cmd)
    os.system(cmd)
    return redirect('/view/' + note_title + '.md#' + note_header.lstrip('#').strip().replace(' ', '-'))

## @app.route('/open/<filename>')
## def open_file(filename):
##     if platform.system() == "Linux":
##         out = commands.getoutput('locate ' + filename)
##     if platform.system() == "Darwin":
##         # out = commands.getoutput('glocate ' + filename)
##         out = commands.getoutput('mdfind -name ' + filename)

##     first_hit = out.split('\n')[0]
##     print('# of hits ' + str(len(out.split('\n'))) + " " + out.replace('\n',', '))
##     if not first_hit:
##         print('not found')
##         return ('Not found', '~~' + filename + '~~')
##     else:
##         print('hit ' + first_hit)
##     cmd = 'open "/' + first_hit + '" &'
##     os.system(cmd)
##     return cmd

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(PATH_TO_TEMPLATE + os.sep + 'js/' , path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(PATH_TO_TEMPLATE + os.sep + 'css/' , path)

@app.route('/img/<path:path>')
def send_flav(path):
    return send_from_directory(PATH_TO_TEMPLATE + os.sep + 'img/', path)

@app.route('/imgs/<path:path>')
def send_img(path):
    return send_from_directory(PATH_TO_MD + os.sep + 'imgs', path)

@app.route('/view/<path:note_title>')
def view(note_title):
    """Open a note with your edit
    http://flask.pocoo.org/snippets/76/
    """
    if request.remote_addr not in ['127.0.0.1', '0.0.0.0']:
        if note_title not in OPEN_ACCESS:
            return 'Hmm...'

    if 'Users/' in note_title:
        cmd = 'open "/' + note_title + '" &'
        print(cmd)
        os.system(cmd)
        return jsonify(result="")


    head = open(PATH_TO_TEMPLATE_HTML).read()
    head = head.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')
    head = head.replace('href="img/', 'href="' + '/img/')
    head = head.replace('="lib/', '="' + '/lib/')
    head = head.replace('="css/', '="'+ '/css/')
    head = head.replace('="js/', '="' + '/js/')
    head = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->', r'', head, flags=re.M | re.DOTALL)

    html = open(PATH_TO_HTML + os.sep + note_title.replace('.md', '.html')).read()
    #return head + html
    return html

@app.route('/search/<text>')
def search(text):
    if request.remote_addr not in ['127.0.0.1', '0.0.0.0']:
        return 'Hmm...'

    results = search_term(text)
    if not results.strip():
        results = 'NOT FOUND'
    else:
        results = '{{TOC}}\n\n' + results  # this does not work! the output is html h1 etc

    head = open(PATH_TO_TEMPLATE_HTML).read()
    head = head.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')
    head = head.replace('href="img/', 'href="' + '/img/')
    head = head.replace('="lib/', '="' + '/lib/')
    head = head.replace('="css/', '="'+ '/css/')
    head = head.replace('="js/', '="' + '/js/')

    # os.system('open file://' + PATH_TO_HTML + '_search_geekbook_.html')

    # remove demo content
    head = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->', r'', head, flags=re.M | re.DOTALL)

    with open(PATH_TO_MD + '_search_.md', 'w') as f:
        f.write(results)

    p = Page('_search_.md')
    print('compiling...')
    p.compile()
    p.save()
    
    return redirect('/view/_search_.html')
    return
    #return send_from_directory('', 'file:///' + PATH_TO_HTML + '/geekbook-search.html')
    #return redirect(url_for('static', filename='file:///' + PATH_TO_HTML + '/geekbook-search.html'))


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--public', default=False,
                        action="store_true", help="be public")
    parser.add_argument('--debug', default=False,
                        action="store_true", help="debug mode")
    parser.add_argument('--port', default=5000, type=int)
    return parser


#main
if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    if args.public:
        # if you want your geekbook to be seen in the network uncomment this line, and comment the line above
        print('WARNING PUBLIC MODE')
        app.run(debug=args.debug, host= '0.0.0.0', port=args.port)
        # of course be very careful with this. EVERYONE within network can read ALL your notes! (if they know your IP)
    else:
        app.run(debug=args.debug, port=args.port)
