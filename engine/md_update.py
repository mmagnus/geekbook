#!/usr/bin/python
# -*- coding: utf-8 -*-
"""I'm working on this.Trying to cope with the pre processing of the MD file."""

import codecs
from engine.conf import PATH_TO_MD, SCREENSHOT_INBOX, PATH_TO_IMG, IMG_PREFIX, AI_WRITER, USE_RM_TO_REMOVE_FIGURE
from engine.process_md import right_MD_from_webservices, get_youtube_embeds_insert, remove_image
from engine.plugins.insert_image import insert_image_in_md
from engine.plugins.draw_secondary_structure import get_ss
from engine.plugins.ia_writer import edit_syntax_from_ai_writer_to_geekbook
from os import sep


import logging
logger = logging.getLogger('geekbook')


class Md_update(object):
    """Md_update class

    Attributes:

      fn
      md
    This class is responsible for the changes operated directly on the MD file.
    For example replacing some patterns with MarkDown language.
    """

    def __init__(self, fn):
        """Init a Page and load the content of MD file into self.md"""
        self.fn = fn
        try:
            with codecs.open(PATH_TO_MD + sep + fn, "r", "utf-8") as f:
                self.md = f.read()
        except IOError:
            # logging.error('file removed ' + self.fn)
            pass

    def compile(self):
        """Preprocess, compile, postprocess."""
        # get_ss
        self.md, is_get_ss = get_ss(self.md)

        # insert_image_in_md
        is_ii = False
        if SCREENSHOT_INBOX:
            self.md, is_ii = insert_image_in_md(self.md, PATH_TO_IMG, IMG_PREFIX)
        self.md, is_right_MD = right_MD_from_webservices(self.md)

        self.md, yti = get_youtube_embeds_insert(self.md)

        use_rm = False
        if USE_RM_TO_REMOVE_FIGURE:
            self.md, use_rm = remove_image(self.md)

        # ai writer
        is_edit_synatx_ai = False
        if AI_WRITER:
            self.md, is_edit_synatx_ai = edit_syntax_from_ai_writer_to_geekbook(self.md, IMG_PREFIX)

        # check if anything changed
        if any([is_get_ss, is_ii, is_right_MD, is_edit_synatx_ai, yti, use_rm]):
            return True
        else:
            return False

    def save(self):
        with codecs.open(PATH_TO_MD + sep + self.fn, "w", "utf-8") as outfn:
            outfn.write(self.md)


if __name__ == '__main__':
    fin = 'test.md'

    m = Md_update(fin)
    m.compile()
    m.save()
