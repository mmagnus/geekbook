#!/usr/bin/python
# -*- coding: utf-8 -*-
"""page module
"""

import markdown
import codecs
from mdx_gfm import GithubFlavoredMarkdownExtension


import os
from os import sep
from shutil import copy
from sys import stdout
from time import sleep, gmtime, strftime

from geekbook.engine.src.after_html import add_head, change_data_tag_into_actual_data, change_todo_square_chainbox_or_icon, change_html_tags_bootstrap, add_path_to_img
from geekbook.engine.conf import PATH_TO_MD, PATH_TO_HTML, PATH_TO_ORIG
from geekbook.engine.src.lib import get_image_path
from geekbook.engine.src.tableofcontent import make_table_of_content

from colors import bcolors


class Page(object):
    """Page class

    Attributes:

      fn
      md
      html

    """
    def __init__(self, fn):
        self.fn = fn
        with codecs.open(PATH_TO_MD + sep + fn, "r", "utf-8") as f:
            self.md = f.read()
        self.html = ''

    def get_md(self):
        """
        """
        self.html = markdown.markdown(self.md, extensions=[GithubFlavoredMarkdownExtension()])#(linenums=False)'])
        #html = '<link rel="stylesheet" href="/home/magnus/Dropbox/lb_v2/templates/Pygments/css/pygments.css" type="text/css">' + html

    def compile(self):
        """
        """
        print '['+ strftime("%H:%M:%S", gmtime())+'] -'+' compiling --> %s' % self.fn,
        self.pre_process()
        self.get_md()
        self.post_process()
        print '[ok]'

    def update(self):
        """
        """
        print '['+ strftime("%H:%M:%S", gmtime())+'] -'+' updating --> %s' % self.fn,
        self.pre_process()
        self.get_md()
        self.post_process()
        print '[ok]'

    def pre_process(self):
        """
        """
        ntext = ''
        for l in self.md.split('\n'):
            l = get_image_path(l)
            ntext += l + '\n'
        ntext = change_todo_square_chainbox_or_icon(ntext)
        self.md = ntext

    def post_process(self):
        """
        """
        self.html = add_head(self.html)
        self.html = make_table_of_content(self.html)
        self.html = change_data_tag_into_actual_data(self.html)
        self.html = change_html_tags_bootstrap(self.html)
        self.html = add_path_to_img(self.html)

    def is_changed(self):
        """Check if the file on disc is different than `md`.

        Return:
          boolean
        """
        try:
            with codecs.open(PATH_TO_ORIG + sep + self.fn, "r", "utf-8") as f:
                orig_md = f.read()
        except IOError:
            fail_message = bcolors.FAIL + 'IOError: ' + self.fn + bcolors.ENDC
            pass_message = bcolors.OKGREEN + 'IOError: ' + self.fn + "Ok" + bcolors.ENDC
            for i in range(1,20):
                stdout.write("\r" + fail_message)
                stdout.flush()
                sleep(1)
            print(pass_message)
            orig_md = ''
            pass

        if not os.path.exists(PATH_TO_ORIG):
            os.mkdir(PATH_TO_ORIG)

        if self.md != orig_md:
            copy(PATH_TO_MD + sep + self.fn, PATH_TO_ORIG + sep + self.fn)
            return True
        else:
            return False

    def save(self):
        """
        """
        if not os.path.exists(PATH_TO_HTML):
            os.mkdir(PATH_TO_HTML)

        with codecs.open(PATH_TO_HTML + self.fn.replace('.md', '.html'), "w", "utf-8") as outfn:
            outfn.write(self.html)


if __name__ == '__main__':
    fin = 'test.md'

    p = Page(fin)
    p.compile()
    print p.is_changed()
    p.save()
