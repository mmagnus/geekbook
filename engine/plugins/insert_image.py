#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insert_image is executed in md_update.py

"""
import glob
import os
import shutil
import datetime
from PIL import ImageGrab
import random
import string
import time
import platform

from geekbook.engine.conf import INSERT_IMAGE_TAG, INSERT_IMAGE_TAG2, SCREENSHOT_INBOX, SCREENSHOT_INBOX2

import subprocess
def exe(cmd):
    o = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = o.stdout.read().strip().decode()
    err = o.stderr.read().strip().decode()
    return out, err


def get_creation_time_via_pil(fn):
    from PIL import Image
    im = Image.open(fn)
    exif = im.getexif() 
    creation_time = exif.get(36867)
    if creation_time:
        d, t = creation_time.split()
        d = d.replace(':', '')[2:]
        return d + '-' + t
    else:
        return ''


def get_file_size(fn):
    out,err = exe("ls -lh '" + fn + "'")
    return out.split()[4]

    
def get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    try:
        stat = os.stat(path_to_file)
    except OSError:
        return ''
    try:
        d = stat.st_birthtime
        d = datetime.datetime.fromtimestamp(d)
        return d.strftime('%Y%m%d')[2:]
    except AttributeError:
        # We're probably on Linux. No easy way to get creation dates here,
        # so we'll settle for when its content was last modified.
        return stat.st_mtime


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
    text = text.replace('.jpeg/Users/', '.jpeg\n/Users/')

    text = text.replace('.jpegfile:///Users/', '.jpeg\nfile:///Users/')
    text = text.replace('.jpgfile:///Users/', '.jpg\nfile:///Users/')
    text = text.replace('.pngfile:///Users/', '.png\nfile:///Users/')

    ltext = text.split('\n')
    changed = False
    for c in range(0, len(ltext)):
        ### Clipboard ####################
        if ltext[c].strip() == '\ip':
            im = ImageGrab.grabclipboard()
            N = 10
            t = datetime.datetime.today().strftime('%y%m%d') + '_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
            fullpath = td + IMG_PREFIX + t + '.jpeg'
            if verbose:
                print('Create an image from clipboard', fullpath)
            if im:
                im.save(fullpath, 'JPEG', quality=80, optimize=True, progressive=True)
                ltext[c] = '![](' + IMG_PREFIX + t + '.jpeg)'
                changed = True
            else:
                ltext[c] = '\ip error'
                changed = True

        # desktop, but can be configure
        if ltext[c].strip() == INSERT_IMAGE_TAG:
            ltext[c] = insert_image(SCREENSHOT_INBOX, td, IMG_PREFIX)
            changed = True

        # dropbox, but can be configure
        if ltext[c].strip() == INSERT_IMAGE_TAG2:
            ltext[c] = insert_image(SCREENSHOT_INBOX2, td, IMG_PREFIX)
            changed = True

        ############################
        ### Apple Photos [2] ###########
        # file:///Users/magnus/Pictures/Photos%20Library.photoslibrary/resources/derivatives/B/BC0F463E-7D5E-4FC7-A105-7A56A1121DD9_1_105_c.jpeg
        line = ltext[c].strip()

        is_image = False
        if '.jpeg' in line or '.jpg' in line or '.png' in line:
            is_image = True
        if 'file://' in line and is_image and 'Error' not in line:
            f = ltext[c]
            f = f.replace('%20', ' ').replace('file://', '')
            source_path = f
            creation_date = get_creation_time(source_path)
            t = os.path.basename(source_path) # target # is only filename without path
            t = t.replace(' ', '_')
            #creation_date = get_creation_date(source_path)
            size = get_file_size(source_path)
            if creation_date:
                t = creation_date + '_' + size + '_' + t.replace('UNADJUSTEDNONRAW_', '')
            else:
                t = datetime.datetime.today().strftime('%y%m%d') + '_' + size + '_' + t.replace('UNADJUSTEDNONRAW_', '')
            # clean % from the names
            try:
                shutil.copy(source_path, td + IMG_PREFIX + t)
            except IOError:
                ltext[c] = 'Error in ' + source_path
                changed = True
            else:
                if verbose:
                    print('Coping', source_path, td + IMG_PREFIX + t)
                ltext[c] = '![](' + IMG_PREFIX + t + ') '# + creation_date #  + t + ')'
                changed = True
        ############################

        ### Apple Photos ###########
        # /Users/magnus/Pictures/Photos Library.photoslibrary/resources/derivatives/F/FE0782F9-B144-4B2F-889A-3F4961E6E3E0_1_105_c.jpeg
        if '/Pictures/Photos Library.photoslibrary/resources/' in ltext[c].strip() and 'Error' not in ltext[c].strip():
            source_path = ltext[c]
            creation_date = get_creation_date(source_path)
            t = os.path.basename(source_path) # target
            creation_date = get_creation_time(source_path)

            size = get_file_size(source_path)
            if creation_date:
                t = creation_date + '_' + size + '_' + t.replace('UNADJUSTEDNONRAW_', '')
            else:
                t = datetime.datetime.today().strftime('%y%m%d') + '_' + size + '_' + t.replace('UNADJUSTEDNONRAW_', '')
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
                ltext[c] = '![](' + IMG_PREFIX + t + ') '# + creation_date #  + t + ')'
                changed = True
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
    """Check the latest file in d-rectory and copy it to t-arget d-rectory.

    Put a time of creation into a filename."""
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
        size = get_file_size(newest)
        # copy to img
        t = os.path.basename(newest.replace(' ','_'))
        # add date
        # datetime.datetime.today().strftime('%y%m%d')
        creation_time = get_creation_time(newest)
        t = creation_time + '_' + size + '_' + t
        shutil.move(newest, td + IMG_PREFIX + t)
        return '![](' + IMG_PREFIX  + t + ')'
    else:
        return 'error of import, any file not found'

    
def get_creation_time_via_stat(fn):
    import pathlib
    fname = pathlib.Path(fn)
    ctime = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
    # replaces to get to the format:
    # 2021-01-26_09:28:54.834750 to 210126_09:28:54.834750
    return str(ctime).replace('-', '').replace(' ', '-')[2:] # to remove year ;-) lame
    
def get_creation_time(fn):
    dat = get_creation_time_via_pil(fn)
    if not dat:
        dat = get_creation_time_via_stat(fn)
    return dat

if __name__ == '__main__':
    # insert_image()
    fn = '/Users/magnus/Desktop/h5a_5foa/IMG_1888.jpeg'
    #dat = get_creation_time(fn)
    #print(dat)
    #fn = "/Users/magnus/Pictures/Photos Library.photoslibrary/resources/derivatives/E/E412371D-8D5A-408C-845F-BCA826EB4F6A_1_105_c.jpeg"
    #insert_image_file:file:///Users/magnus/Pictures/Photos%20Library.photoslibrary/resources/derivatives/E/E412371D-8D5A-408C-845F-BCA826EB4F6A_1_105_c.jpeg//from_Apple_Photos(text, verbose=True)
    #dat = get_creation_time(fn)
    #print(dat)
    print(get_file_size(fn))
