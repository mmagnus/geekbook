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
from colors import bcolors

from engine.postprocessing import *
from engine.preprocessing import get_image_path
from engine.conf import PATH_TO_MD, PATH_TO_HTML, PATH_TO_ORIG
from engine.make_tableofcontent import make_table_of_content

import logging
logger = logging.getLogger('geekbook')


class Page(object):
    """Page class

    Attributes:

      fn
      md
      html

    """
    def __init__(self, fn):
        """Init a Page and load the content of MD file into self.md"""
        self.fn = fn
        with codecs.open(PATH_TO_MD + sep + fn, "r", "utf-8") as f:
            self.md = f.read()
        self.html = ''

    def get_html(self):
        """Compile md to get html"""
        self.html = markdown.markdown(self.md, extensions=[GithubFlavoredMarkdownExtension()])#(linenums=False)'])
        #html = '<link rel="stylesheet" href="/home/magnus/Dropbox/lb_v2/templates/Pygments/css/pygments.css" type="text/css">' + html

    def compile(self):
        """Preprocess, compile, postprocess.
        """
        logger.info('compiling --> %s' % self.fn)
        self.pre_process()
        self.get_html()
        self.post_process()

    def pre_process(self):
        """Do preprocessing.

        E.g.::

           self.md = get_image_path(self.md) """
        self.md = get_image_path(self.md)
        self.md = get_youtube_embeds(self.md)
        self.md = right_link_from_dropbox_screenshot(self.md)

    def post_process(self):
        """Do postprocessing"""
        self.html = add_head(self.html)
        self.html = make_table_of_content(self.html)
        self.html = change_data_tag_into_actual_data(self.html)
        self.html = add_path_to_img(self.html)
        self.html = change_html_tags_bootstrap(self.html)
        self.html = pigmentize(self.html)
        self.html = personal_tags_to_html(self.html)

    def is_changed(self):
        """Check if the file on disc is different than `md`.

        Make PATH_TO_ORIG if it does not exists.

        Return:
          boolean
        """
        if not os.path.exists(PATH_TO_ORIG):
            os.makedirs(PATH_TO_ORIG)

        try:
            with codecs.open(PATH_TO_ORIG + sep + self.fn, "r", "utf-8") as f:
                orig_md = f.read()
        except IOError:
            logging.error('file not detected. Create it: ' + self.fn) 
            orig_md = ''
            pass

        if self.md != orig_md:
            copy(PATH_TO_MD + sep + self.fn, PATH_TO_ORIG + sep + self.fn)
            return True
        else:
            return False

    def save(self):
        """Save html file to the drive"""
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
