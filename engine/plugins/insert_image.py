import glob
import os
import shutil
import sys
import datetime


def insert_image_in_md(text, d, td, IMG_PREFIX):
    """Go over each line and check if there is `ii`. If yes, then run insert_image function."""
    ltext = text.split('\n')
    changed = False
    for c in range(0, len(ltext)):
        if ltext[c].strip() == 'ii':
            ltext[c] = insert_image(d, td, IMG_PREFIX)
            changed = True
    return '\n'.join(ltext), changed # trigger compiles


def insert_image(d = '/home/magnus/Desktop/{*png,*jpg,*jpeg}', td = '/home/magnus/Dropbox/geekbook/notes/imgs/', IMG_PREFIX='imgs/'):
    """Check the latest file in d-rectory and copy it to t-arget d-rectory"""
    # make folder with imgs
    try:
        os.mkdir(td)
    except OSError:
        pass

    newest = max(glob.iglob(d), key=os.path.getctime)
    # copy to img
    t = os.path.basename(newest.replace(' ','_'))
    # add date
    t = datetime.datetime.today().strftime('%y%m%d') + '_' + t
    shutil.move(newest, td + IMG_PREFIX + t)
    return '![](' + IMG_PREFIX  + t + ')'


if __name__ == '__main__':
    insert_image()
