#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""geekbookapp - the main program. The magic starts here!"""

import time
import os
import sys
import argparse
import logging
import commands
import gc
import platform

logging.basicConfig(format='%(asctime)s - %(filename)s - %(message)s')
logger = logging.getLogger('geekbook')
logger.setLevel('INFO')

PATH = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))  # __file__)))
sys.path.append(PATH)


from engine.conf import PATH_TO_MD, PATH_TO_HTML, PATH_TO_IMG, PATH_TO_ORIG, AI_WRITER
from engine.page import Page
from engine.md_update import Md_update
from engine.make_index import Index
from engine.colors import bcolors
from engine.searcher import make_db
from engine.plugins import ia_writer
# import yappi


class GeekbookError(Exception):
    pass


class MdFiles(object):
    """MdFiles manages the index of your md files (notes)"""
    path_to_watch = PATH_TO_MD

    def __init__(self):
        self.md_files = []
        self.get_filelist()
        self.sort_by_mtime()

    def get_filelist(self):
        """Get a raw index of all files in your notes folder, clean it and save the list as
        self.md_files"""
        self.md_files = os.listdir(self.path_to_watch)
        nfiles = []
        for f in self.md_files:
            if ' ' in f:
                raise GeekbookError("""We don't handle names of you notes with spaces, please \
use `-`. e.g. geekbook-is-the-best.md Please rename your note and start this app again. Fix: """ % f)
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
        """Get a list of your MD files.
        Update: alwasy get an updated list!"""
        self.get_filelist()
        self.sort_by_mtime()
        return self.md_files


class App(object):
    """App class"""

    def __init__(self, args):
        self.args = args
        # fix #
        try:
            os.mkdir(PATH_TO_ORIG)
        except OSError:
            pass

    def start(self):
        """Start the App.
        """
        if not self.args.debug:
            os.system('clear')
            print (bcolors.OKGREEN + "\n                 ________               __   __________               __    \n                /  _____/  ____   ____ |  | _\______   \ ____   ____ |  | __\n               /   \  ____/ __ \_/ __ \|  |/ /|    |  _//  _ \ /  _ \|  |/ /\n               \    \_\  \  ___/\  ___/|    < |    |   (  <_> |  <_> )    < \n                \______  /\___  >\___  >__|_ \|______  /\____/ \____/|__|_ \ \n                       \/     \/     \/     \/       \/                   \/ \n" + bcolors.ENDC)
        logger.info("G33kB00k is Running... [ok]")

        logger.info("root path: %s" % PATH)
        try:
            os.makedirs(PATH_TO_HTML)
        except OSError:
            pass
        logger.info("html path: <file://" + PATH_TO_HTML + 'index.html>')
        logger.info("imgs path: " + PATH_TO_IMG)

        logger.info('Ready to go! Please edit me: notes/')

        mf = MdFiles()
        logger.info('You have %i notes! Congrats, keep noting!' % len(mf.get_files()))

        index = Index()
        index.update(mf.get_files())

        # yappi.start()
        c = 0

        ipynb_mtime = {}

        while c < 10:  # for debugging
            if AI_WRITER:
                ia_writer.ia_writer_movie_imgs_from_root_folder()

            # check for ipython

            # if not ipynb_mtime:
            # notebook_files = os.listdir(PATH_TO_MD)
            # for n in [n for n in notebook_files if n.endswith('.ipynb') and n.startswith('jupyter')]:
            # cmd = "jupyter nbconvert " + PATH_TO_MD + os.sep + n + " --to markdown"
            # print cmd
            # os.system(cmd)
            # ipynb_mtime[n] = os.path.getmtime(PATH_TO_MD + os.sep + n)
            # else:
            # notebook_files = os.listdir(PATH_TO_MD)
            # for n in [n for n in notebook_files if n.endswith('.ipynb')]:
            # if n in ipynb_mtime.keys():
            # mt = os.path.getmtime(PATH_TO_MD + os.sep + n)
            # if ipynb_mtime[n] < mt:
            # cmd = "jupyter nbconvert " + PATH_TO_MD + os.sep + n + " --to markdown"
            # print cmd
            # os.system(cmd)
            # ipynb_mtime[n] = mt
            # else:
            # mt = os.path.getmtime(PATH_TO_MD + os.sep + n)
            # cmd = "jupyter nbconvert " + PATH_TO_MD + os.sep + n + " --to markdown"
            # print cmd
            # os.system(cmd)
            # ipynb_mtime[n] = mt

            # see what's new - diff between to folders your notes and orig files that keep copy of our notes
            # grep -v removes things from your list, ~, # (and in mmagnus case org mode files)
            cmd = "diff -u -r " + PATH_TO_MD + " " + PATH_TO_ORIG + \
                " | grep -v '.org' | grep -v '~' | grep -v '#' | grep '.md'".strip()
            out = commands.getoutput(cmd)
            # print out
            files_changed = []

            # pick all file names that are changed
            for l in out.split('\n'):
                # new notes
                if l.startswith('Only in ' + PATH_TO_MD):
                    files_changed.append(os.path.basename(l.split()[-1]))
                # changes notes
                if l.startswith('diff -u -r'):
                    files_changed.append(os.path.basename(l.split()[-1]))

            # if there are files change compile them
            for f in files_changed:
                m = Md_update(f)
                p = Page(f)
                if p.is_changed():
                    # if m is changed then (by using any of plugins working on markdown, run this
                    changed = m.compile()
                    if changed:  # only if something is changed in md
                        m.save()

                    p.compile()
                    p.save()

                    index = Index()
                    index.update(mf.get_files())

            if UPDATE:
                for f in mf.get_files():
                    if f == 'imgs':
                        pass
                    else:
                        p = Page(f)
                        p.compile()
                        p.save()

                sys.exit(0)

            # dev -d <file>
            if DEV:
                # update index
                index = Index()
                index.update(mf.get_files())

                # update this one picked note
                m = Md_update(args.debug)
                changed = m.compile()  # if changed MD
                if changed:
                    m.save()

                p = Page(args.debug)
                p.compile()
                p.save()

                sys.exit(0)

            gc.collect()
            time.sleep(1)  # if this is too big you have too wait for ii too long (!)
            # off c += 1

        # yappi.stop()
        # stats = yappi.get_func_stats()
        # stats.save('yappi.callgrind', type="callgrind")


def start_flask(args):
    if not args.noflask and not args.debug and not args.update:
        logger.info("Start off flask!")
        os.system('python ' + PATH + os.sep + 'geekbook/engine/webserverflask.py &')


def start_gitweb():
    """Start git instaweb"""
    os.chdir(PATH_TO_MD)
    os.system('git instaweb')


def start_browser_with_index():
    """Detect the operative system in use and open the html file using the default browser.
    Works with Linux and macOS."""
    if platform.system() == "Linux":
        os.system('xdg-open http://127.0.0.1:5000/view/index.html')
    elif platform.system() == "Darwin":
        os.system('open http://127.0.0.1:5000/view/index.html')
    else:
        logger.info("Sorry, I cannot detect your system, you will have to open the file manually @")


def get_parser():
    """Get parser of arguments"""
    parser = argparse.ArgumentParser('geekbookapp.py')
    parser.add_argument('-d', '--debug', help='debug mode, run only for file,' +
                        'WARNING: use only name of the note, e.g. test.md, NOT notes/test.md')
    parser.add_argument('-u', '--update', help='updates all the pages', action='store_true')
    parser.add_argument(
        '-s', '--silent', help='dont bring up the Internet Browser', action='store_true')
    parser.add_argument('-n', '--notebook',
                        help='updates all jupiter notebooks!', action='store_true')
    parser.add_argument('--noflask', help='dont run flask', action='store_true')
    parser.add_argument('--noupdatedb', help='dont update the db', action='store_true')
    return parser


def convert_jupyter_notebook_to_markdown():
    if args.notebook:
        notebook_files = os.listdir(PATH_TO_MD)
        for n in [n for n in notebook_files if n.endswith('.ipynb')]:
            cmd = "jupyter nbconvert " + PATH_TO_MD + os.sep + n + " --to markdown"
            print cmd
            os.system(cmd)
        sys.exit(1)


# main
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # emacs & python debugging
    # args = parser.parse_args(['--debug', 'test.md', '-s'])
    # args = parser.parse_args(['-u'])

    app = App(args)
    if not args.noupdatedb:
        make_db()
    convert_jupyter_notebook_to_markdown()
    start_flask(args)

    #[mm] notes git:(master) ✗
    #    [NbConvertApp] Converting notebook testA.ipynb to markdown
    #[NbConvertApp] Support files will be in testA_files/
    #[NbConvertApp] Making directory testA_files
    #[NbConvertApp] Writing 2960 bytes to testA.md

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

    app.start()
