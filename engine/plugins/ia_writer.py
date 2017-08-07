#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import shutil

from engine.conf import PATH_TO_IMG


def ia_writer_movie_imgs_from_root_folder():
    pngs = glob.glob(PATH_TO_IMG + '/*png')
    for pfile in pngs:
        print(pfile)
        shutil.move(pfile, PATH_TO_IMG)


def edit_syntax_from_ai_writer_to_geekbook(text, IMG_PREFIX):
    """Go over each line and check if there is /foo.png. If yes, then edit it
    from AI Writer syntax to Geekbook.

    Example::

        >>> edit_syntax_from_ai_writer_to_geekbook('/foo.png', 'imgs')
        ('!()(imgs/foo.png]', True)

    """
    textlist = text.split('\n')
    changed = False
    ntextlist = []
    for line in textlist:
        if line.startswith('/') and line.endswith('.png'):
            line = line.replace('/', '![](' + IMG_PREFIX).strip() + ')'
            changed = True
        ntextlist.append(line)
    return '\n'.join(ntextlist), changed


if __name__ == '__main__':
    import doctest
    doctest.testmod()
