import glob
import os
import shutil
import sys
import datetime


def insert_image_in_md(text, sd, td, IMG_PREFIX, verbose=False):
    """Go over each line and check if there is `ii`. If yes, then run insert_image function.

    Args:
        text (str): The path of the file to wrap
        d (str): source directory
        td (str): target directory
        IMG_PREFIX

    Returns:
        Text
    """
    text = text.replace('.jpg/Users/', '.jpg\n/Users/')
    ltext = text.split('\n')
    changed = False
    for c in range(0, len(ltext)):
        if ltext[c].strip() == 'ii':
            ltext[c] = insert_image(sd, td, IMG_PREFIX)
            changed = True
        ### Apple Photos ###########
        if '/Pictures/Photos Library.photoslibrary/resources/proxies/' in ltext[c].strip():
            source_path = ltext[c]
            t = os.path.basename(source_path) # target
            t = datetime.datetime.today().strftime('%y%m%d') + '_' + t.replace('UNADJUSTEDNONRAW_', '')
            # clean % from the names
            t = t.replace('%', '')
            # copy
            shutil.copy(source_path, td + IMG_PREFIX + t)
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
    # insert_image()
    text = """bleblelbe
/Users/magnus/Pictures/Photos Library.photoslibrary/resources/proxies/derivatives/6a/00/6acd/2sekD%FRSC2LkDAT44CGtA_thumb_6acd.jpg
"""
    insert_image_from_Apple_Photos(text, verbose=True)
