#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Search for [ff:..]  with (g)locate make a link.

To remove the db, you can simply run ``rm geekbook/engine/plugins/find_file.json``"""

import sys
import re
import logging
import os

logger = logging.getLogger('geekbook')

JSON_DB = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'find_file.json'


def find_files(text, verbose=False):
    """
    The search was completely re-written in a way that now the files
    are search at the level of Flask.

    So go to Flask to see how this is done.

    ``geekbook/engine/webserverflask.py``
    """
    output = ''
    msg_listofnotfoundfiles = ''
    for l in text.split('\n'):
        rx = re.compile('\[ff:(?P<file>.+?)\]').search(l)
        if rx:
            filename = rx.group('file')
            if verbose: print('# filename: ', filename)
            folderpath, filepath = '', filename # file_search(filename, False)

            if verbose: print('# file_finder.search()', output)
            # remove for now folder link, it does not work @todo
            #output += l.replace('[ff:' + filename + ']',' <a href="' + folderpath + '"><code>[+]</code></a> ' + '<a target="_blank" href="/open' + filepath + '"> <span class="mantext">' + os.path.basename(filepath) + '</span></a>')
            output += l.replace('[ff:' + filename + ']', '<a  href="#" address="' + filepath + '" id="openfile"> <span class="mantext">' + os.path.basename(filepath) + '</span></a>\n') # or without '\n
        else:
            output += l + '\n'
    output = output.replace('[files-not-found]', msg_listofnotfoundfiles)
    return output


if __name__ == '__main__':
    #text = sys.stdin.read()
    text = """
    [ff:XQxIC1CrCP.gif]
    """
    output = find_files(text, verbose=False)
    sys.stdout.write(output)
