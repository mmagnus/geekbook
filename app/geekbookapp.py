#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" geekbookapp
"""

import time
import os
import sys
import argparse

PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print PATH
sys.path.append(PATH)

from geekbook.app.conf import PATH_TO_MD, PATH_TO_HTML
from geekbook.app.src.page import Page
from geekbook.app.src.make_index import Index

class MdFiles(object):
    """MdFiles class"""
    path_to_watch = PATH_TO_MD

    def __init__(self):
        self._get_files()
        self.clean_up()
        self.sort_by_mtime()

    def _get_files(self):
        self.md_files = os.listdir(self.path_to_watch)

    def clean_up(self):
        nfiles = []
        for f in self.md_files:
            if f.find('#') > -1 or f.find('~') > -1 \
               or f.startswith('.') or f.endswith('.org'):
                continue
            else:
                nfiles.append(f)
        self.md_files = nfiles

    def sort_by_mtime(self):
        self.md_files.sort(key=lambda x: os.stat(os.path.join(self.path_to_watch, x)).st_mtime)
        self.md_files.reverse()

    def get_files(self):
        return self.md_files


class App(object):
    """App class"""
    def __init__(self):
        pass

    def start(self):
        """Start the App.
        """
        print 'geekbook is up... [ok]'

        while 1:

            mf = MdFiles()

            for f in mf.get_files():
                if f == 'imgs':
                    pass
                else:
                    p = Page(f)
                    if p.is_changed():
                        p.compile()
                        p.save()

                        index = Index()
                        index.update(mf.get_files())

            if DEV:
                index = Index()
                index.update(mf.get_files())
                p = Page('rna-dca.md')
                p.compile()
                p.save()

                sys.exit(1)

                time.sleep(3)
            else:
                time.sleep(1)


def start_gitweb():
    """Start git instaweb"""
    os.chdir(PATH_TO_MD)
    os.system('git instaweb')

def start_browser_with_index():
    os.system('firefox %s' % PATH_TO_HTML + '/index.html')

def get_parser():
    parser = argparse.ArgumentParser('geekbookapp.py')
    parser.add_argument('-d', '--debug', help='debug mode', action='store_true')
    return parser

if __name__ == '__main__':
    
    args = get_parser().parse_args()

    a = App()

    if args.debug:
        DEV = True
    else:
        DEV = False
        start_gitweb()
        #start_browser_with_index()
    a.start()
