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

from icecream import ic
import sys
ic.configureOutput(outputFunction=lambda *a: print(*a, file=sys.stderr))
ic.configureOutput(prefix='> ')

from geekbook.engine.conf import INSERT_IMAGE_TAG, INSERT_IMAGE_TAG2, SCREENSHOT_INBOX, SCREENSHOT_INBOX2,\
     INSERT_IMAGE_TAG2_SUFFIX, INSERT_IMAGE_TAG_SUFFIX, INSERT_IMAGE_HASHTAG, INSERT_IMAGE_HASHTAG2,\
     INSERT_IMAGE_TAG3, SCREENSHOT_INBOX3, INSERT_IMAGE_TAG3_SUFFIX, INSERT_IMAGE_HASHTAG3

import subprocess
def exe(cmd):
    o = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = o.stdout.read().strip().decode()
    err = o.stderr.read().strip().decode()
    return out, err


def get_creation_time_via_pil(fn):
    from PIL import Image, UnidentifiedImageError
    try:
        im = Image.open(fn)
    except UnidentifiedImageError: # for heif files of Apple https://github.com/python-pillow/Pillow/issues/2806
        return None
    except FileNotFoundError:
        return None    
    exif = im.getexif() 
    creation_time = exif.get(36867)
    if creation_time:
        d, t = creation_time.split()
        d = d.replace(':', '')[2:]  # remove : seperator for date
        return d + '-' + t.replace(':', '.')
    else:
        return None


def get_file_size(fn):
    out,err = exe("ls -lh '" + fn + "'")
    if not err:
        return out.split()[4]
    return ''
    
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
        return d.strftime('%Y%m%d')[2:].replace(':', '.')
    except AttributeError:
        # We're probably on Linux. No easy way to get creation dates here,
        # so we'll settle for when its content was last modified.
        return stat.st_mtime.replace(':', '.')


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
            ltext[c] = insert_image(SCREENSHOT_INBOX, td, IMG_PREFIX, INSERT_IMAGE_TAG_SUFFIX, INSERT_IMAGE_HASHTAG)
            changed = True

        # dropbox, but can be configure
        if ltext[c].strip() == INSERT_IMAGE_TAG2:
            ltext[c] = insert_image(SCREENSHOT_INBOX2, td, IMG_PREFIX, INSERT_IMAGE_TAG2_SUFFIX, INSERT_IMAGE_HASHTAG2)
            changed = True

        # ~/Downloads/ but can be configure
        if ltext[c].strip() == INSERT_IMAGE_TAG3:
            ltext[c] = insert_image(SCREENSHOT_INBOX3, td, IMG_PREFIX, INSERT_IMAGE_TAG3_SUFFIX, INSERT_IMAGE_HASHTAG3)
            changed = True

        ############################
        ### Apple Photos [2] ###########
        # file:///Users/magnus/Pictures/Photos%20Library.photoslibrary/resources/derivatives/B/BC0F463E-7D5E-4FC7-A105-7A56A1121DD9_1_105_c.jpeg
        line = ltext[c].strip()

        is_image = False
        if '.jpeg' in line.lower() or '.jpg' in line.lower() or '.png' in line.lower() or '.heic' in line.lower():
            is_image = True
        if ('file://' in line) and is_image and 'Error' not in line:
            # FileNotFoundError: [Errno 2] No such file or directory: file://localhost/localhost/private/var/folders/yc/ssr9692s5fzf7k165grnhpk80000gp/T/Anki-CWARbe/paste-29f8f06a3d79478480a7f2baaffcaab63056e351.png
            f = ltext[c]
            f = f.replace('%2C', ',').replace('%28', '(').replace('%29', ')').replace('%20', ' ').replace('file://localhost/','/').replace('file://', '')
            source_path = f
            creation_date = get_creation_time(source_path)
            t = os.path.basename(source_path) # target # is only filename without path
            t = t.replace(' ', '_')
            #creation_date = get_creation_date(source_path)
            size = get_file_size(source_path)
            if creation_date:
                t = creation_date + '_' + size + '_' + t.replace('UNADJUSTEDNONRAW_', '')[:5]
            else:
                t = datetime.datetime.today().strftime('%y%m%d') + '_' + size + '_' + t.replace('UNADJUSTEDNONRAW_', '')[:5]

            # clean % from the names
            try:
                # if heic
                if line.endswith('.heic'):
                    t = t.replace('.heic', '.jpeg')
                    cmd = "magick mogrify -monitor -format jpg '%s'" % source_path # ok, this is done inplace
                    from icecream import ic
                    import sys
                    print(cmd)
                    os.system(cmd)
                    nt = t + '.MIN.jpeg'
                    nsource_path = source_path.replace('.heic', '.jpg')
                    cmd = "convert '%s' -quality 40 '%s'" % (nsource_path, td + IMG_PREFIX + nt)
                    os.system(cmd)
                    print(cmd)
                    t = nt # for writing in a file                
                else:
                    shutil.copy(source_path, td + IMG_PREFIX + t)
                    os.system("trash '" + source_path + "'")
            except IOError:
                ltext[c] = 'Error in ' + source_path
                changed = True
            else:
                if verbose:
                    print('insert_image.py: coping', source_path, td + IMG_PREFIX + t)
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
                shutil.copy(source_path, td + IMG_PREFIX + t)
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


def insert_image(d = '/Users/magnus/Desktop/', td = '/home/magnus/Dropbox/geekbook/notes/imgs/', IMG_PREFIX='imgs/', suffix='', hastag=''):
    """Check the latest file in d-rectory and copy it to t-arget d-rectory.
    suffix: add a text to a file name for example "scanned" to get <pic>_scanned.png
    Put a time of creation into a filename."""
    # make folder with imgs
    try:
        os.mkdir(td)
    except OSError:
        pass
    files = []
    for ftype in ['*.jpg', '*.png', '*.jpeg', '*gif']:
        p = glob.glob(d + ftype)
        files.extend(p)
    if files:
        newest = max(files, key=os.path.getctime)
        size = get_file_size(newest)
        # copy to img
        t = os.path.basename(newest.replace(' ','_'))
        ext = os.path.splitext(t)[1] # get ext
        # add date
        # datetime.datetime.today().strftime('%y%m%d')
        # 130818-10.03.32_201K_938BEFCE-D2D3-4B80-9AE1-243408DDBFDA_1_105_c.jpeg
        creation_time = get_creation_time(newest)
        print(t, ext, suffix)
        t = creation_time + '_' + size + '_' + t.replace(ext, suffix + ext)
        shutil.move(newest, td + IMG_PREFIX + t)
        return '![' + hastag + '](' + IMG_PREFIX  + t + ')'
    else:
        return 'error of import, any file not found'

def get_creation_time_via_stat(fn):
    import pathlib
    try:
        fname = pathlib.Path(fn)
        ctime = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
    except FileNotFoundError:
        return None
    # replaces to get to the format:
    # 2021-01-26_09:28:54.834750 to 210126_09:28:54.834750
    return str(ctime).replace('-', '').replace(' ', '-')[2:].replace(':', '.')  # to remove year ;-) lame
    
def get_creation_time(fn):
    """ function to wrap on time"""
    return get_date_exiftool(fn) # for screenshots etc
    # !!!!!!!!!!!! #
    if not dat:
        dat = get_creation_time_via_pil(fn)
    if not dat:
        dat = get_creation_time_via_stat(fn)

    return dat

def get_creation_time_v3(filepath):
    """Gets the date taken for a photo through a shell."""
    cmd = "mdls '%s'" % filepath
    output = subprocess.check_output(cmd, shell = True)
    lines = output.decode("ascii").split("\n")
    for l in lines:
        if "kMDItemContentCreationDate" in l:
            datetime_str = l.split("= ")[1]
            print(datetime_str)
            # ugly fix for time one +1
            d = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S +0000") + datetime.timedelta(hours=2) 
            print(d)
            return str(d.strftime('%y%m%d')),  str(d.strftime('%H%M'))
    raise DateNotFoundException("No EXIF date taken found for file %s" % filepath)


def get_creation_time_v2(fn):

        from PIL import Image
        try:
            im = Image.open(fn)
            exif = im.getexif() 
            creation_time = exif.get(36867)
            if creation_time:
                d, t = creation_time.split()
                d = d.replace(':', '')[2:]
                t = t.replace(':', '-')
                return (d, t)
        except:
            print(fn)
            return ('error', '')

def get_date_exiftool(fn):
    """pyexiftool https://pypi.org/project/PyExifTool/"""
    import exiftool
    files = [fn]
    ic(fn)
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(files)

    d = ''
    for d in metadata:
        try:
            d = d["EXIF:DateTimeOriginal"].replace(' ', '-').replace(':', '').replace(':', '.')[2:] + '_v2' # remove the year [2:]
            #print("{:20.20} {:20.20}".format(d["SourceFile"], d["EXIF:DateTimeOriginal"])) # example
        except KeyError: # if not date then this
            d = d["File:FileAccessDate"].replace(' ', '-').replace(':', '').replace(':', '.')[2:] + '_v2'
    return d

def get_date_file(fn):
    cmd = "file '" + fn + "'"
    output = subprocess.check_output(cmd, shell = True)
    #os.system()
    # datetime=
    import re
    #x = str(output).split('datetime=')[1].split('image')[0].replace(':', '').strip().replace(' ', '-')
    #return x
    print(output)
    print(str(output).split(','))
    for i in str(output).split(','):
        print('dupa', i)
        #if 'datetime':
        #    d = i.strip().replace('datetime=','') #2021:09:16 19:39:41
        #    ic(d)
        #    return d
    #r = re.findall(r'datetime=(?P<dt>.*?)', str(output), re.M) # [\d: ]+
    #print(r)
    #if r:
    #    dt = r.group('dt')
    #    ic(dt)
    #aaaaaaaa    
        
#main
if __name__ == '__main__':
    # insert_image()
    fn = '/Users/magnus/Desktop/h5a_5foa/IMG_1888.jpeg'
    fn = "/Users/magnus/Pictures/Photos Library.photoslibrary/resources/derivatives/9/977FC017-D725-42EC-8C81-7B5B35E1CE7C_1_102_a.jpeg"
    fn = "/Users/magnus/Pictures/Photos Library.photoslibrary/resources/renders/9/977FC017-D725-42EC-8C81-7B5B35E1CE7C_1_201_a.heic"
    fn = "/Users/magnus/Pictures/Photos Library.photoslibrary/resources/derivatives/D/D943BC4D-BFA2-476A-A7E3-D51C5837B45F_1_105_c.jpeg"
    fn = "/Users/magnus/Library/Mobile Documents/27N4MQEA55~pro~writer/Documents/imgs/221003-17.17.44.534412_3.4M_IMG_6615.jpeg"
    #dat = get_creation_time(fn)
    #print(dat)
    #fn = "/Users/magnus/Pictures/Photos Library.photoslibrary/resources/derivatives/E/E412371D-8D5A-408C-845F-BCA826EB4F6A_1_105_c.jpeg"
    #insert_image_file:file:///Users/magnus/Pictures/Photos%20Library.photoslibrary/resources/derivatives/E/E412371D-8D5A-408C-845F-BCA826EB4F6A_1_105_c.jpeg//from_Apple_Photos(text, verbose=True)
    #dat = get_creation_time(fn)
    #print(dat)
    # date format
    # 220927-11.09.24.364393_467K_sc_2022-09-27_at_11.09.18.jpg)

    if 0:
        ic(get_file_size(fn))
        ic(get_creation_time(fn))
        ic(get_creation_time_v2(fn))
        ic(get_creation_time_via_pil(fn))
        ic(get_creation_time_v3(fn))
        ic(get_creation_time_via_stat(fn))
        # 2022-03-09T08:21:10Z
        print('stats')
        os.system("stat '" + fn + "'")
        print('file')
        os.system("file '" + fn + "'")
        get_date_file(fn)
    get_date_exiftool(fn)
