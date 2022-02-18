#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""iA writer plugin.

Detect an image inserted vie iA writer and convert to Geekbook syntax,
and move the image to
proper Geekbook images storage folder.

Example::

       /emacs.jpeg -> ![](imgs/emacs.jpeg)

"""
import datetime
import logging
import os
import shutil

from geekbook.engine.conf import IMG_PREFIX, PATH_TO_IMG, PATH_TO_MD


logger = logging.getLogger('geekbook')
logger.setLevel('INFO')


def add_timestamp_to_image(file):
    """This function is used if there is already a file with the same name in your
    images storage folder."""
    filename, ext = os.path.splitext(file)
    return filename + '-' + (str(datetime.datetime.now()).replace(' ',
                                                                  '')) + ext


def edit_syntax_from_ai_writer_to_geekbook(text, img_prefix):
    """Go over each line and check if there is /foo.png (or /foo.jpeg). If yes, then edit it
    from iA Writer syntax to Geekbook.

    Example::

        >>> edit_syntax_from_ai_writer_to_geekbook('/foo x.png', 'imgs')
        ('![](imgs/foo_x.png)', True)

    Returns:

        (str, bool): text, changed is True if any of iA syntax detected

    .. warning:: works with .png and .jpeg
    """
    textlist = text.split('\n')
    changed = False
    ntextlist = []

    if not img_prefix.endswith('/'):
        img_prefix += '/'

    for line in textlist:
        if line.startswith('/') and (line.lower().endswith('.png') or line.lower().endswith('.jpg') or line.lower().endswith('.jpeg') or line.lower().endswith('.gif')):
            pfile = line.replace('/', '')
            pfile_fullpath = PATH_TO_IMG + os.sep + IMG_PREFIX + os.sep + pfile

            if os.path.exists(pfile_fullpath):
                targetfn = add_timestamp_to_image(pfile.replace(' ', '_'))
            else:
                targetfn = pfile.replace(' ', '_')

            logger.info("mv %s %s" % (PATH_TO_MD + os.sep + pfile,
                                      os.sep + IMG_PREFIX + os.sep + targetfn))

            try:
                shutil.move(PATH_TO_MD + pfile,
                            PATH_TO_IMG + IMG_PREFIX + os.sep + targetfn)
                pass
            except:
                logger.info("error: moving the file")

            line = '![](' + IMG_PREFIX + targetfn + ')'
            changed = True

        ntextlist.append(line)
    return '\n'.join(ntextlist), changed


if __name__ == '__main__':
    import doctest
    doctest.testmod()
