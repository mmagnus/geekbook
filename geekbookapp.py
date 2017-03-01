#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""geekbookapp - the main program. The magic starts here!"""

import time
import os
import sys
import argparse
import filecmp
from os import sep
import logging
import subprocess

logging.basicConfig(format='%(asctime)s - %(filename)s - %(message)s')
logger = logging.getLogger('geekbook')
logger.setLevel('INFO')

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH)

import platform


from engine.conf import PATH_TO_MD, PATH_TO_HTML, PATH_TO_IMG, PATH_TO_ORIG
from engine.page import Page
from engine.md_update import Md_update
from engine.make_index import Index
from engine.colors import bcolors

#import yappi

class MdFiles(object):
    """MdFiles manages the index of your md files (notes)"""
    path_to_watch = PATH_TO_MD

    def __init__(self):
        self.md_files = []
        self.get_filelist()
        self.sort_by_mtime()

    def get_filelist(self):
        """Get a raw index of all files in your notes folder, clean it and save the list as self.md_files"""
        self.md_files = os.listdir(self.path_to_watch)
        nfiles = []
        for f in self.md_files:
            if f.find('#') > -1 or f.find('~') > -1 \
               or f.startswith('.') or f.endswith('.org'):
                continue
            else:
                if f.endswith('.md'):
                    nfiles.append(f)
        self.md_files = nfiles

    def sort_by_mtime(self):
        """Sort by mtime the list of md files"""
        self.md_files.sort(key=lambda x: os.stat(os.path.join(self.path_to_watch, x)).st_mtime)
        self.md_files.reverse()

    def get_files(self):
        """Get a list of your MD files"""
        return self.md_files


class App(object):
    """App class"""
    def __init__(self, args):
        self.args = args

    def start(self):
        """Start the App.
        """
        if not self.args.debug:
            os.system('clear')
            print (bcolors.OKGREEN + "\n                 ________               __   __________               __    \n                /  _____/  ____   ____ |  | _\______   \ ____   ____ |  | __\n               /   \  ____/ __ \_/ __ \|  |/ /|    |  _//  _ \ /  _ \|  |/ /\n               \    \_\  \  ___/\  ___/|    < |    |   (  <_> |  <_> )    < \n                \______  /\___  >\___  >__|_ \|______  /\____/ \____/|__|_ \ \n                       \/     \/     \/     \/       \/                   \/ \n" + bcolors.ENDC)
        logger.info("G33kB00k is Running... [ok]")

        logger.info("root path: %s" % PATH)
        logger.info("html path: <file://" + PATH_TO_HTML + 'index.html>')
        logger.info("imgs path: " + PATH_TO_IMG)

        logger.info('Ready to go! Please edit me: notes/')
        
        mf = MdFiles()
        logger.info('You have %i notes! Congrats, keep noting!' % len(mf.get_files()))

        #yappi.start()
        c = 0
        while c < 10:
            
            mf = MdFiles()

            for f in mf.get_files():
                if f == 'imgs':
                    pass
                else:
                    if UPDATE:
                        p.compile()
                        p.save()
                    else:
                        # if different then do anything
                        # we could use this at some point
                        # http://stackoverflow.com/questions/977491/comparing-two-txt-files-using-difflib-in-python
                        pipe = subprocess.Popen(['diff', PATH_TO_ORIG + sep + f, PATH_TO_MD + sep + f], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        #cmd = "diff -r ~/Dropbox/geekbook/engine/data/orig/ notes/ | grep 'in notes' | grep -v 'org' | grep -v '~' | grep -v '#' | grep '.md'"
                        #pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
                        stdout, stderr = pipe.communicate() # it seems that diff if not equal gives stderr non-zero
                        #stdout = commands.getoutput(cmd).strip()
                        # Only in notes/: rna-SimRNAweb.md
                        #stdout = stdout.replace('Only in notes/: ', '')
                        #for f in stdout.strip().split('\n'):
                        # ^^^ this should be moved from here any way, this is in f
                        if stdout or stderr:
                            m = Md_update(f)
                            p = Page(f)
                            if p.is_changed():
                                changed = m.compile()
                                if changed: # only if something is changed in md
                                    m.save()

                                p.compile()
                                p.save()

                                index = Index()
                                index.update(mf.get_files())

            # update -u option
            if UPDATE:
                index = Index()
                index.update(mf.get_files())

                sys.exit(0)

            # dev -d <file>
            if DEV:
                index = Index()
                index.update(mf.get_files())

                m = Md_update(args.debug)
                changed = m.compile() # if changed MD
                if changed:
                    m.save()

                p = Page(args.debug)
                p.compile()
                p.save()

                sys.exit(0)

            time.sleep(1)
            # off c += 1
            
        #yappi.stop()
        #stats = yappi.get_func_stats()
        #stats.save('yappi.callgrind', type="callgrind")

def start_gitweb():
    """Start git instaweb"""
    os.chdir(PATH_TO_MD)
    os.system('git instaweb')


def start_browser_with_index():
    """Detect the operative system in use and open the html file using the default browser. 
    Works with Linux and macOS."""
    if platform.system() == "Linux":
        os.system('xdg-open file://' + PATH_TO_HTML + 'index.html')
    if platform.system() == "Darwin":
        os.system('open file://' + PATH_TO_HTML + 'index.html')
    else:
        logger.info("Sorry, I cannot detect your system, you will have to open the file manually @")


def get_parser():
    """Get parser of arguments"""
    parser = argparse.ArgumentParser('geekbookapp.py')
    parser.add_argument('-d', '--debug', help='debug mode, run only for file')
    parser.add_argument('-u', '--update', help='updates all the pages', action='store_true')
    parser.add_argument('-s', '--silent', help='dont bring up the Internet Browser', action='store_true')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()

    a = App(args)

    if args.debug:
        DEV = True
        UPDATE = False
    elif args.update:
        UPDATE = True
        DEV = False
    else:
        DEV = False
        UPDATE = False
        if not args.silent:
            start_gitweb()
            start_browser_with_index()
    a.start()
