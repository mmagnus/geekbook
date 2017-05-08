#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""

@todo
 - h3 and h4 are not search??? (i think)
 - dont replace ## because it breaks '## @tag ## text'
 - if md has no # at start you get error! and if you have # and then ### !!!

####################################################################################################
/home/magnus/Dropbox/lb_v2/md/RNApuzzle05.md
Traceback (most recent call last):
  File "make-everything-in-one-line.py", line 157, in <module>
    main()
  File "make-everything-in-one-line.py", line 140, in main
    all_headers.extend(make_headers_objects_for_md(o))
  File "make-everything-in-one-line.py", line 85, in make_headers_objects_for_md
    current_h1.add_child(current_h2)
UnboundLocalError: local variable 'current_h1' referenced before assignment

Marcin Magnus
init: 2012/10/05
huge improv: 2012/11/08
"""
debug = False

import myutils
import sys
import re
import os
import codecs
import pickle

from prettytable import *

import os
import sys
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print PATH
sys.path.append(PATH)
from engine.conf import PATH_TO_HTML, PATH_TO_TEMPLATE_HTML, PATH_TO_MD

class Header:
    """
    Header = # or ## or ### or ####
    """
    def __init__(self, name, level, md):
        """
        input:
         - name = header
         - level: # = 1, ## = 2
         - md = travel
        """
        
        self.name = name
        self.name_dashed = name.replace(' ', '-')
        self.level = level
        self.child = []
        self.note = ''
        self.md = md
    def add_child(self, header_obj):
        self.child.append(header_obj)
    def get_child(self):
        return self.child
    def get_note(self):
        return self.note
    def has_note(self):
        if self.note:
            return True
        else:
            return False
    def add_note(self, note):
        self.note = note
    def get_format(self, term):
        out = ''
        out += '<h1 style="font-size:20px;color:black><a href="/view/' + self.md + '.html#' + self.name_dashed + '">' + self.name + '</a></h1>\n'
        out += '<small style="color: #009933;">' + '<a href="/view/' + self.md + '.html#' + self.name_dashed + '">' + self.md + '</a>' + '</small>\n'
        #        out += '<p>...' + myutilspy.hightlight_text_in_html(term, self.note).replace('\n','<br/>') + '...<p>\n'
        out += '<pre>' + myutils.hightlight_text_in_html(term, self.note).replace('\n','<br/>') + '</pre>\n'
        out += '<div style="width:100%" class="hrDotted"></div>'
        return out

    def __repr__(self):
        return 'h' + str(self.level) + ': ' + self.name

def next_lines_has_header_or_end_of_file(lines, no_lines, c, v=0):
    """
    Return True when the end of the files occurs or a next line starts with '#'
    Return False if a next line starts with anything different than '#'.
    If a next line is empty then just skip the line and get a next next line to analyse.
    """
    if c == no_lines:
        return True
    elif lines[c].startswith('#'):
        return True
    else:
        return False

def replace_space_with_minus(text):
    replace = text.replace(' ', '-')
    return replace

def make_headers_objects_for_md(filename, verbose=False,version2=True):
    """
    filename = '/home/magnus/Dropbox/lb_v2/md/bioinfo::threading.md'
    """
    text = codecs.open(filename, mode="r", encoding="utf8").read()
    md = filename.replace(PATH_TO_MD, '').replace('.md','') ## md = bioinfo::threading
    root = []  ## starting point of the structure
    lines = text.split('\n')
    no_lines = len(lines)
    list_h = ''
    note = ''
    c = 0
    for l in lines:
        c += 1
        if l.startswith('# '):
            l = l.replace('# ', '')
            current_h1 = Header(l, 1, md)
            root.append(current_h1)
            last_h = current_h1
        elif l.startswith('## '):
            l = l.replace('## ', '')
            current_h2 = Header(l, 2, md)
            try:
                current_h1.add_child(current_h2)
            except UnboundLocalError:
                raise Exception(filename)
            last_h = current_h2
        elif l.startswith('### '):
            l = l.replace('### ', '')
            current_h3 = Header(l, 3, md)
            try:
                current_h2.add_child(current_h3) ################ if not current2 then current1
            except UnboundLocalError:
                raise Exception(filename)

            last_h = current_h3
        elif l.startswith('#### '):
            l = l.replace('#### ', '')
            current_h4 = Header(l, 4, md)
            try:
                current_h3.add_child(current_h4)
            except UnboundLocalError:
                raise Exception(filename)
            last_h = current_h4
        else:
            note += ' ' + l + '\n' ## \n = not in one line!
            if next_lines_has_header_or_end_of_file(lines, no_lines, c):
                try:
                    last_h.add_note(note)
                except NameError:
                    pass
                note = ''  ## reset the note variable
    if verbose: print 'root has following headers of # type: '.ljust(40), root
    #tb = PrettyTable(["r.name", "r.note", "r.level", "r.get_child()", "h3"])
    for r in root:
        row = [r.name, r.note[:50], r.level, r.get_child(), [x.get_child() for x in r.get_child()]]
        if verbose: print row
        #tb.add_row(row)
    ## collect all h1
    all_h = []
    for r in root:
        all_h.append(r)
        for c in r.get_child():
            all_h.append(c)
            for a in c.get_child():
                all_h.append(a)
    return all_h

class Db():
    """
    """
    def __init__(self, ):
        """
        """
        self.all_headers = ''

    def collect_data(self, v=0):
        out = myutils.lsdir(PATH_TO_MD)
        ## hack start ##
        out2 = []
        #'/home/magnus/Dropbox/lb_v2/md/.#bash.md'
        for i in out:
            if i.find('#')>-1 or i.find('~')>-1 or i.find('.org')>-1 or i.find('.git')>-1:
                pass
            else:
                if i.endswith('.md'):
                    out2.append(i)
        out = out2
        ## hack end ##

        all_headers = []
        print '<head><meta content="text/html; charset=UTF-8" http-equiv="content-type">'
        print "<link rel='stylesheet' href='/home/magnus/Dropbox/Public/lb/css/style.css' /></head>"
        for o in out:
            if v: print o
            all_headers.extend(make_headers_objects_for_md(o))
        self.all_headers = all_headers

    def search(self, term):
        hits_output = self._search_over_headers_objects(term, self.all_headers)
        return hits_output

    def _search_over_headers_objects(self, term, v=0):
        hits = []
        for h in self.all_headers:
            #print h.level, h.name, ' -->', h.note
            if re.search(term, h.name + h.note, re.I):
                hits.append(h)
        hits_output = ''
        for hit in hits:
            if v:print hit.name
            if v:print hit.note
            h = hit.get_format(term)
            hits_output += h
            if v:print
        return hits_output


def make_db():
    db = Db()
    print 'searcher::making the db'
    db.collect_data()
    pickle.dump(db, open( "searchdb.pickle", "wb" ))

def search(term):
    db = pickle.load(open( "searchdb.pickle", "rb"))
    return db.search(term)

#main
if __name__ == '__main__':
    term = '@test'
    #print make_db()
    search('@test')
