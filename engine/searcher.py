#!/usr/bin/env python3

"""

@todo
 - h3 and h4 are not search??? (i think)
 - dont replace ## because it breaks '## @tag ## text'
 - if md has no # at start you get error! and if you have # and then ### !!!

Error::

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
import re
import os
import codecs
import pickle

import os
import sys
import argparse

import logging
logger = logging.getLogger('geekbook')

debug = False
if not debug:
    PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
else:
    from engine_path import path

sys.path.append(PATH)
from engine.conf import PATH_TO_HTML, PATH_TO_TEMPLATE_HTML, PATH_TO_MD

debug = False


def hightlight_text_in_html(phrase, text, mark_line_only=True):
    """
    Replace <PHRASE> with a highlighted text '<span style="background-color:yellow">PHRASE</span>'

    Normal phrase is used and .upper()
    """
    # ugly hack ;-)
    if mark_line_only:
        ntext = ''
        for l in text.split('\n'):
            if phrase.lower() in l.lower():
                l += '<span style="background-color:red"><<<<<<<<<<<<<<<<<<<<<<<<</span>'
            ntext += l + '\n'
        text = ntext
    else:
        text = text.replace(phrase, '<span style="background-color:yellow">' + phrase + '</span>')
        text = text.replace(phrase.upper(), '<span style="background-color:yellow">' + phrase.upper() + '</span>')
        text = text.replace(phrase.title(), '<span style="background-color:yellow">' + phrase.title() + '</span>')
    return text


def lsdir(directory='/home/magnus/Desktop/', exclude_files_starting_with_dot=True, verbose=False):
    """
    magnus@maximus:~/workspace/myutil$ python test.py
    /home/magnus/Desktop/bookmarks-2010-10-15-present-bookmarks-nice.json
    /home/magnus/Desktop/Untitled 2.odt
    /home/magnus/Desktop/logo.jpg

    GET:
    - directory e.g. /home/magnus/Desktop/

    DO:
    - walk and collect a list of all files -> f
    RETURN:
    - f = list of all files under given directory, [/home/magnus/Desktop/temp/beta.png, ... ,/home/magnus/Desktop/temp/temp~]

    http://snippets.dzone.com/posts/show/644

    """
    def walktree(top=".", depthfirst=True):
        import stat
        names = os.listdir(top)
        if not depthfirst:
            yield top, names
        for name in names:
            try:
                st = os.lstat(os.path.join(top, name))
            except os.error:
                continue
            if stat.S_ISDIR(st.st_mode):
                for (newtop, children) in walktree(os.path.join(top, name), depthfirst):
                    yield newtop, children
        if depthfirst:
            yield top, names

    f = []
    for (basepath, children) in walktree(directory, False):
        for child in children:
            if exclude_files_starting_with_dot:
                if not child.endswith('.md'):
                    continue
                if child.startswith('.'):
                    continue
                else:
                    if verbose:
                        print(os.path.join(basepath, child))
                    f.append(os.path.join(basepath, child))
    return f


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
        self.last_md = ''
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

    def get_format(self, term, prev_md):
        """Get the format for the hit.

        prev_md is to make grouping at the search page:

        # file
        ## hit1
        ## hit2

        """
        out = ''
        if prev_md == self.md:
            pass
        else:
            out += '\n# ' + self.md + '\n'
        out += '\n## ' + self.name + '\n'

        out += '<small style="color: #009933;">' + '<a href="/view/' + self.md + \
            '.html#' + self.name_dashed + '">' + self.md + '</a>' + '</small>\n'
        #        out += '<p>...' + myutilspy.hightlight_text_in_html(term, self.note).replace('\n','<br/>') + '...<p>\n'
        out += '' + hightlight_text_in_html(term, self.note).replace('\n', '<br/>') + '\n'
        out += '<div style="width:100%" class="hrDotted"></div>'
        return out, self.md

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


def make_headers_objects_for_md(filename, verbose=False, version2=True):
    """
    filename = '/home/magnus/Dropbox/lb_v2/md/bioinfo::threading.md'
    """
    # fix for flycheck_*.md
    try:
        text = open(filename, mode="r").read()
    except FileNotFoundError:  # fix for files removed
        return ''
    #all_h = []
    #    return []

    md = filename.replace(PATH_TO_MD, '')
    # replace only .md at the very end    #.replace('.md','') ## md = bioinfo::threading
    md = re.sub('.md$', '', md)
    root = []  # starting point of the structure
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
                current_h1 = Header('', 1, md)
                current_h1.add_child(current_h2)

            last_h = current_h2
        elif l.startswith('### '):
            l = l.replace('### ', '')
            current_h3 = Header(l, 3, md)
            try:
                current_h2.add_child(current_h3)  # if not current2 then current1
            except UnboundLocalError:
                current_h2 = Header('', 2, md)
                current_h2.add_child(current_h3)

            last_h = current_h3
        elif l.startswith('#### '):
            l = l.replace('#### ', '')
            current_h4 = Header(l, 4, md)
            try:
                current_h3.add_child(current_h4)
            except UnboundLocalError:
                current_h3 = Header('', 3, md)
                current_h3.add_child(current_h4)
            last_h = current_h4
        else:
            note += ' ' + l + '\n'  # \n = not in one line!
            if next_lines_has_header_or_end_of_file(lines, no_lines, c):
                try:
                    last_h.add_note(note)
                except NameError:
                    pass
                note = ''  # reset the note variable
    if verbose:
        print('root has following headers of # type: '.ljust(40), root)
    #tb = PrettyTable(["r.name", "r.note", "r.level", "r.get_child()", "h3"])
    for r in root:
        row = [r.name, r.note[:50], r.level, r.get_child(), [x.get_child() for x in r.get_child()]]
        if verbose:
            print(row)
        # tb.add_row(row)
    # collect all h1
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

    def collect_data(self, verbose=False):
        out = lsdir(PATH_TO_MD)
        ## hack start ##
        out2 = []  # list of files to process
        #'/home/magnus/Dropbox/lb_v2/md/.#bash.md'
        for i in out:
            if i.find('#') > -1 or i.endswith('~') or '_search_' in i or \
              i.startswith('flycheck_') or i.find('.org') > -1 or i.find('.git') > -1:
                pass
            else:
                if i.endswith('.md'):
                    out2.append(i)

        files = out2
        ## hack end ##

        all_headers = []
        # print '<head><meta content="text/html; charset=UTF-8" http-equiv="content-type">'
        # print "<link rel='stylesheet' href='/home/magnus/Dropbox/Public/lb/css/style.css' /></head>"
        for f in files:
            all_headers.extend(make_headers_objects_for_md(f))
        self.all_headers = all_headers

    def search(self, term, verbose):
        hits_output = self._search_over_headers_objects(term, self.all_headers)
        if verbose: hits_output
        return hits_output

    def _search_over_headers_objects(self, term, v=0):
        hits = []
        for h in self.all_headers:
            if re.search(term, h.name + h.note, re.I):
                hits.append(h)
        hits_output = ''
        last_md = ''
        for hit in hits:
            if v:
                print(hit.name)
            if v:
                print(hit.note)
            h, last_md = hit.get_format(term, last_md)
            hits_output += h
            if v:
                print
        return hits_output

def make_db(verbose=False):
    db = Db()
    logger.info('searcher.py::making the db')
    db.collect_data(verbose)
    pickle.dump(db, open(PATH + os.sep + "engine/searchdb.pickle", "wb"), protocol=3)


def search_term(term, verbose=False):
    db = pickle.load(open(PATH + os.sep + "engine/searchdb.pickle", "rb"))
    return db.search(term, verbose)



def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument("term", help="", default="")
    return parser


# main
if __name__ == '__main__':
    parser = get_parser()
    if debug:
        args = parser.parse_args(['Elia for Journal', '--verbose'])
    args = parser.parse_args()

    print(make_db(args.verbose))
    print(search_term(args.term, args.verbose))
