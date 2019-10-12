#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_image is executed in md_update.py

"""
import glob
import os
import shutil
import sys
import datetime
from PIL import ImageGrab
import random
import string

from geekbook.engine.conf import INSERT_IMAGE_TAG, INSERT_IMAGE_TAG2, SCREENSHOT_INBOX, SCREENSHOT_INBOX2

def insert_image_in_md(text, td, IMG_PREFIX, verbose=False):
    """Go over each line and check if there is `ii`. If yes, then run insert_image function.

    Args:
        text (str): The path of the file to wrap
        d (str): source directory
        td (str): target directory
        IMG_PREFIX

    Returns:
        Text
    """
    verbose = True
    text = text.replace('.jpg/Users/', '.jpg\n/Users/')
    ltext = text.split('\n')
    changed = False
    for c in range(0, len(ltext)):
        ### Clipboard ####################
        if ltext[c].strip() == 'ip':
            im = ImageGrab.grabclipboard()
            N = 10
            t = datetime.datetime.today().strftime('%y%m%d') + '_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
            fullpath = td + IMG_PREFIX + t
            if verbose:
                print('Create an image from clipboard', source_path, td + IMG_PREFIX + t)
            im.save(fullpath, 'PNG')
            ltext[c] = '![](' + IMG_PREFIX + t + ')' #  + t + ')'
            changed = True

        # desktop, but can be configure
        if ltext[c].strip() == INSERT_IMAGE_TAG:
            ltext[c] = insert_image(SCREENSHOT_INBOX, td, IMG_PREFIX)
            changed = True

        # dropbox, but can be configure
        if ltext[c].strip() == INSERT_IMAGE_TAG2:
            ltext[c] = insert_image(SCREENSHOT_INBOX2, td, IMG_PREFIX)
            changed = True

        ### Apple Photos ###########
        if '/Pictures/Photos Library.photoslibrary/resources/proxies/' in ltext[c].strip():
            source_path = ltext[c]
            t = os.path.basename(source_path) # target
            t = datetime.datetime.today().strftime('%y%m%d') + '_' + t.replace('UNADJUSTEDNONRAW_', '')
            # clean % from the names
            t = t.replace('%', '')
            # copy
            try:
                shutil.copy(source_path, td + IMG_PREFIX + t)
            except IOError:
                ltext[c] = 'Error in ' + source_path
                changed = True
            else:
                if verbose:
                    print('Coping', source_path, td + IMG_PREFIX + t)
                ltext[c] = '![](' + IMG_PREFIX + t + ')' #  + t + ')'
                changed = True
        ############################
    return '\n'.join(ltext), changed # trigger compiles


## OK, for efficiency (= I don't have to go over text one again) I merged this function
## into insert_image_in_md. It's not a very clean solution, but it will be faster
## than processing text twice under given implementation.
## def insert_image_from_Apple_Photos(text, td = '/home/magnus/Dropbox/geekbook/notes/', IMG_PREFIX='imgs/', verbose=False):
##     """
##     /Users/magnus/Pictures/Photos Library.photoslibrary/resources/proxies/derivatives/6a/00/6acd/2sekD%FRSC2LkDAT44CGtA_thumb_6acd.jpg
##     """
##     ltext = text.split('\n')
##     changed = False
##     for c in range(0, len(ltext)):
##         if '/Pictures/Photos Library.photoslibrary/resources/proxies/' in ltext[c].strip():
##             source_path = ltext[c]
##             #t = datetime.datetime.today().strftime('%y%m%d') + '_' + t
##             shutil.copy(source_path, td + IMG_PREFIX)# + t)
##             if verbose:
##                 print('Coping', source_path, td + IMG_PREFIX)
##             ltext[c] = '![](' + IMG_PREFIX + ')' #  + t + ')'
##             changed = True
##     return '\n'.join(ltext), changed # trigger compiles


def insert_image(d = '/Users/magnus/Desktop/', td = '/home/magnus/Dropbox/geekbook/notes/imgs/', IMG_PREFIX='imgs/'):
    """Check the latest file in d-rectory and copy it to t-arget d-rectory"""
    # make folder with imgs
    try:
        os.mkdir(td)
    except OSError:
        pass
    files = []
    for ftype in ['*.jpg', '*.png', '*.jpeg']:
        p = glob.glob(d + ftype)
        files.extend(p)
    if files:
        newest = max(files, key=os.path.getctime)
        # copy to img
        t = os.path.basename(newest.replace(' ','_'))
        # add date
        t = datetime.datetime.today().strftime('%y%m%d') + '_' + t
        shutil.move(newest, td + IMG_PREFIX + t)
        return '![](' + IMG_PREFIX  + t + ')'
    else:
        return 'error of import, any file not found'

if __name__ == '__main__':
    # insert_image()
    text = """bleblelbe
/Users/magnus/Pictures/Photos Library.photoslibrary/resources/proxies/derivatives/6a/00/6acd/2sekD%FRSC2LkDAT44CGtA_thumb_6acd.jpg
"""
    insert_image_from_Apple_Photos(text, verbose=True)
