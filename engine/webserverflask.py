#!/usr/bin/env python

"""Webserver"""

import os
import sys
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print PATH
sys.path.append(PATH)
from engine.conf import PATH_TO_HTML, PATH_TO_TEMPLATE_HTML, PATH_TO_TEMPLATE, PATH_TO_MD
print PATH_TO_TEMPLATE_HTML
from engine.postprocessing import add_head
from flask import Flask, redirect, url_for, send_from_directory

import subprocess
import re
from engine.searcher import search_term, Db, Header

app = Flask(__name__, static_url_path='')

@app.route('/edit/<note_title>')
def edit(note_title):
    """Open a note with your edit"""
    os.system('open ' + PATH_TO_MD + ' ' + note_title)
    return 'edit note: %s' % note_title

@app.route('/edit_header/<note_title>/<note_header>')
def edit_header(note_title, note_header):
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
    cmd = "cd " + PATH_TO_MD + " && /usr/bin/grep -n '" + note_header + "' " + note_title + ".md"
    print 'edit_header::cmd:', cmd
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).stdout.read()
    print 'edit_header::out:', out
    note_line = out.split(':')[0]
    os.system('emacsclient +' + note_line + ' ' + PATH_TO_MD + '/' + note_title + '.md &')
    
    return redirect('/view/' + note_title + '.md#' + note_header.lstrip('#').strip().replace(' ', '-'))

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(PATH_TO_TEMPLATE + os.sep + 'js/' , path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(PATH_TO_TEMPLATE + os.sep + 'css/' , path)

@app.route('/imgs/<path:path>')
def send_img(path):
    return send_from_directory(PATH_TO_MD + os.sep + 'imgs', path)

@app.route('/view/<note_title>')
def view(note_title):
    """Open a note with your edit"""
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
    results = search_term(text)

    head = open(PATH_TO_TEMPLATE_HTML).read()
    head = head.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')
    head = head.replace('href="img/', 'href="' + '/img/')
    head = head.replace('="lib/', '="' + '/lib/')
    head = head.replace('="css/', '="'+ '/css/')
    head = head.replace('="js/', '="' + '/js/')

    os.system('open file://' + PATH_TO_HTML + '_search_geekbook_.html')
       
    # remove demo content
    head = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->', r'', head, flags=re.M | re.DOTALL)
    return head + results
    #return send_from_directory('', 'file:///' + PATH_TO_HTML + '/geekbook-search.html')
    #return redirect(url_for('static', filename='file:///' + PATH_TO_HTML + '/geekbook-search.html'))

#main
if __name__ == "__main__":
    app.run(debug=True)#
    #host= '0.0.0.0')#debug=True)
