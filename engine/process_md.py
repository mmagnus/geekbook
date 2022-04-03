#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This is a set of functions that work on Markdown file, before compiling them to html.

Go to page.py (Page) pre_process to add a new function from here."""

import re
import os
import random
import string

from engine.conf import PATH_TO_IMG, PATH_TO_MD, PATH_TO_ORIG

from icecream import ic
import sys
ic.configureOutput(outputFunction=lambda *a: print(*a, file=sys.stderr), includeContext=True)
ic.configureOutput(prefix='> ')

import logging
logger = logging.getLogger('geekbook')
logger.setLevel(logging.INFO)


import subprocess
def exe(cmd):
    o = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = o.stdout.read().strip().decode()
    err = o.stderr.read().strip().decode()
    return out, err


def right_MD_from_webservices(text):
    """ Just paste the url generated by Dropbox to convert it in a markdown img """
    changed = False
    for l in text.split('\n'):
        rx = re.compile('https://www.dropbox.com/(?P<img_id>.+)\?dl=0').search(l)
        rx2 = re.compile('(?<!.)http://g.recordit.co/(?P<rec_id>.+).gif(?!.)').search(l)
        if rx:
            text = re.sub(r'https://www.dropbox.com/(?P<img_id>.+)\?dl=0',
                          '![img](https://www.dropbox.com/' + rx.group('img_id') + '\?raw=1)', text)
            logger.info('dropbox link detected')
            changed = True
        if rx2:
            text = re.sub(r'(?<!.)http://g.recordit.co/(?P<rec_id>.+).gif(?!.)',
                          '![rec](http://g.recordit.co/' + rx2.group('rec_id') + '.gif)',
                          text)
            logger.info('Recordit link detected')
            changed = True
    return text, changed

def simply_interal_links(text):
    """Change http://127.0.0.1:5000/view/cwc15-reporters-h5-r6-210803.html into
    [file:cwc15-reporters-h5-r6-210803.md]

    Fix to deal with this:

    [file:cwc15-introduce-bamHI.md#Run-on-gel-210819]
    http://127.0.0.1:5000/view/cwc15-introduce-bamHI.html#Run-on-gel-210819

    Next: define 127.0.0.1:5000 by option.
    """
    ntext = ''
    changed = False
    for l in text.split('\n'):
        if l.startswith('http://127.0.0.1:5000'):
            l = l.replace('http://127.0.0.1:5000/view/', '[file:')
            l = l.replace('.html', '.md')
            l += ']'
            changed = True
        ntext += l + '\n'
    return ntext, changed

def insert_safari_url(text):
    ntext = ''
    changed = False
    for l in text.split('\n'):
        if l.startswith('\is'):
            with open('/tmp/is.applescript', 'w') as f:
                f.write("""tell application "Safari"
	tell window 1
		tell current tab
			return URL
		end tell
	end tell
end tell""")
            url, err = exe('osascript /tmp/is.applescript')
            ic(url)
            changed = True
            l = url
        ntext += l + '\n'
    return ntext, changed

def insert_file_into_archive(text):
    """Change file:///Users/magnus/Desktop/1VQM-01642-01680_rpr.pdb
    into
    [file:cwc15-reporters-h5-r6-210803.md]

    Fix to deal with this:

    [file:cwc15-introduce-bamHI.md#Run-on-gel-210819]
    http://127.0.0.1:5000/view/cwc15-introduce-bamHI.html#Run-on-gel-210819

    Next: define 127.0.0.1:5000 by option.
    """
    ntext = ''
    changed = False
    GEEKBOOK_ARCHIVE = '/Users/magnus/Library/Mobile\ Documents/27N4MQEA55~pro~writer/Documents/x'
    #'/Users/magnus/Dropbox/geekbook-archive/'
    for l in text.split('\n'):
        if l.startswith('file:///'):
            if l.endswith('.png') or l.endswith('.jpeg') or l.endswith('.jpg'):
                continue
            else:
                fpath = l.replace('file://', '')
                import shutil
                fn = os.path.basename(fpath)
                shutil.move(fpath, '' + fn, GEEKBOOK_ARCHIVE)
                l = '[ff:' + fn + ']'
            changed = True
        ntext += l + '\n'
    return ntext, changed

def remove_image(text, verbose=False):
    """[#rm] will remove the image"""
    changed = False
    ntext = ''
    for l in text.split('\n'):
        if '![#rm]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#rm](', '').replace(')', '')
            cmd = "trash '%s/%s'" % (PATH_TO_MD, fn)
            logger.info('remove image %s', cmd)
            os.system(cmd)
            # skip this line
            changed = True

        elif '![#open]' in l or '![#o]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#open](', '').replace(')', '').strip()
            cmd = "open '%s/%s'" % (PATH_TO_MD, fn)
            logger.info('open image %s', cmd)
            os.system(cmd)
            changed = True
            ntext += l.replace('#open', '') + '\n'

        elif '![#ps]' in l:
            fn = l.replace('![#ps](', '').replace(')', '').strip()
            cmd = " open -a 'Adobe Photoshop 2021.app' '%s/%s'" % (PATH_TO_MD, fn)
            logger.info('open Adobe PS image %s', cmd)
            os.system(cmd)
            changed = True
            ntext += l.replace('#ps', '') + '\n'

        elif '![#fork]' in l or '![#f]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#fork](', '').replace(')', '').strip()
            # # printing letters
            letters = string.ascii_letters
            hash = ''.join(random.choice(letters) for i in range(5)) # hash like ;-)
            nfn = os.path.splitext(fn)[0] + '_fork_' + hash + os.path.splitext(fn)[1]
            cmd = "cp -v '%s/%s' '%s/%s'" % (PATH_TO_MD, fn, PATH_TO_MD, nfn)
            logger.info('%s', cmd)
            os.system(cmd)

            cmd = "open '%s/%s'" % (PATH_TO_MD, nfn)
            logger.info('open image %s', cmd)
            os.system(cmd)

            changed = True
            ntext += l.replace('#fork', '').replace(fn, nfn) + '\n'

        elif '![#dark]' in l or '![#dark]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#dark](', '').replace(')', '').strip()
            #  $f  ${f}.jpeg
            nfn = fn + '.DARK.jpeg'
            # convert $f  /tmp/invtemp
            cmd = "convert '%s/%s' -channel RGB -negate '%s/%s'" % (PATH_TO_MD, fn, PATH_TO_MD, nfn)
            logger.info(cmd)
            os.system(cmd)

            nnfn = fn + '.LIGHT.jpeg'
            cmd = "convert '%s/%s' '%s/%s'" % (PATH_TO_MD, fn, PATH_TO_MD, nnfn)
            logger.info(cmd)
            os.system(cmd)

            changed = True
            ntext += l.replace('#dark', '').replace(fn, nfn) + '\n'

        elif '![#light]' in l or '![#l]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#light](', '').replace(')', '').strip()
            #  $f  ${f}.jpeg
            nfn = fn + '.LIGHT.jpeg'
            cmd = "convert '%s/%s' -channel RGB -negate '%s/%s'" % (PATH_TO_MD, fn, PATH_TO_MD, nfn)
            logger.info(cmd)
            os.system(cmd)

            nnfn = fn + '.DARK.jpeg'
            cmd = "convert '%s/%s' '%s/%s'" % (PATH_TO_MD, fn, PATH_TO_MD, nnfn)
            logger.info(cmd)
            os.system(cmd)

            cmd = "trash '%s/%s'" % (PATH_TO_MD, fn)
            logger.info(cmd)
            os.system(cmd)

            changed = True
            ntext += l.replace('#light', '').replace(fn, nnfn) + '\n' # dark image goes into a note

        elif '![#min]' in l or '![#m]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#min](', '').replace(')', '').strip()
            #  $f  ${f}.jpeg
            nfn = fn + '.MIN.jpeg'
            cmd = "convert '%s/%s' -quality 40 '%s/%s'" % (PATH_TO_MD, fn, PATH_TO_MD, nfn)
            logger.info(cmd)
            os.system(cmd)

            cmd = "trash '%s/%s'" % (PATH_TO_MD, fn)
            logger.info(cmd)
            os.system(cmd)

            changed = True
            ntext += l.replace('#min', '').replace(fn, nfn) + '\n'

        elif '![#smaller]' in l or '![#s]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#s](', '').replace(')', '').strip()
            fn = l.replace('![#smaller](', '').replace(')', '').strip()
            #  $f  ${f}.jpeg
            nfn = fn + '.smaller.jpeg'
            cmd = "convert '%s/%s' -resize 50%% '%s/%s'" % (PATH_TO_MD, fn, PATH_TO_MD, nfn)
            logger.info(cmd)
            os.system(cmd)

            cmd = "trash '%s/%s'" % (PATH_TO_MD, fn)
            logger.info(cmd)
            os.system(cmd)

            changed = True
            ntext += l.replace('#smaller', '').replace(fn, nfn) + '\n'

        else:
            ntext += l + '\n'
    return ntext, changed


def get_youtube_embeds_insert(text):
    from bs4 import BeautifulSoup as bs
    import requests

    ntext = ''
    changed = False
    for l in text.split('\n'):
        if l.startswith('https://www.youtube.com'): #\yti'):
            video_id = l.replace('\yti', '').replace(']', '').replace('https://www.youtube.com/watch?v=', '').strip()
            video_url = "https://www.youtube.com/watch?v=" + video_id
            content = requests.get(video_url)
            soup = bs(content.content, "html.parser")
            title = soup.find("title").text.replace('- YouTube', '').strip()
            # title is wrong right now
            logger.info('youtube video detected: %s', video_id)
            # '**' + title + '**\n
            l = '<iframe width="800" height="441" src="https://www.youtube.com/embed/' + \
                video_id + '" frameborder="0" allowfullscreen></iframe>\n' + \
                           '<https://www.youtube.com/watch?v=' + video_id + '>'
            changed = True
        ntext += l + '\n'
    return ntext, changed


if __name__ == '__main__':
    print(insert_safari_url('\is'))
