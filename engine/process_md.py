#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This is a set of functions that work on Markdown file, before compiling them to html.

Go to page.py (Page) pre_process to add a new function from here."""

import re
import os

from engine.conf import PATH_TO_IMG, PATH_TO_MD, PATH_TO_ORIG

import logging
logger = logging.getLogger('geekbook')
logger.setLevel(logging.INFO)


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

def remove_image(text, verbose=False):
    """[#rm] will remove the image"""
    changed = False
    ntext = ''
    for l in text.split('\n'):
        if '![#rm]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#rm](', '').replace(')', '')
            cmd = "trash '%s/%s'" % (PATH_TO_MD, fn)
            print(cmd)
            os.system(cmd)
            # skip this line
            changed = True
        elif '![#open]' in l: # ![](imgs/210209-14:02:20.916512_146566355_244096550673487_436531621545580684_n.png)
            fn = l.replace('![#open](', '').replace(')', '')
            cmd = "open '%s/%s'" % (PATH_TO_MD, fn)
            print(cmd)
            os.system(cmd)
            # skip this line
            changed = True
            ntext += l.replace('#open', '') + '\n'
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
            logger.info('youtube video detected: %s', video_id)
            l = '**' + title + '**\n<iframe width="800" height="441" src="https://www.youtube.com/embed/' + \
                video_id + '" frameborder="0" allowfullscreen></iframe>\n' + \
                           '<https://www.youtube.com/watch?v=' + video_id + '>'
            changed = True
        ntext += l + '\n'
    return ntext, changed
