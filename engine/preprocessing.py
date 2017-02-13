"""This is a set of functions that work on Markdown file, before compiling them to html."""

from engine.conf import PATH_TO_IMG
import re
import os

import logging
logger = logging.getLogger('geekbook')
logger.setLevel(logging.INFO)

def change_todo_square_chainbox_or_icon(text, verbose=False):
    """Set of rules to replace [i] etc with <img ... >  [ OK ]"""
    ## of list
    text = text.replace('<li>[ ]', '<li><input type="checkbox" />')
    text = text.replace('<li>[X]', '<li><input type="checkbox" checked="checked" />')
    ## every [ ] is change
    text = text.replace('[ ]','<input type="checkbox" />')
    text = text.replace('[X]','<input type="checkbox" checked="checked" />')
    return text


def get_todo(text):
    ntext = ''
    for l in text.split('\n'):
        if not l.startswith('#'):
            l = l.replace('@todo', '<span class="label label-danger">@todo</span>')
        ntext += l + '\n'
    ntext = change_todo_square_chainbox_or_icon(ntext)
    return ntext

def get_abstract(text):
    """``! ``"""
    ntext = ''
    abstract = []

    abstract_flag = False
    for l in text.split('\n'):
        if l.strip() == '[abstract]':
            abstract_flag = True
        if l.startswith('! '):
            if abstract_flag: abstract.append(l[1:])
            l = '<div class="abstract"> ' + l[1:] + '</div>'
        ntext += l + '\n'
    abstract = '<div class="abstract">' + ' '.join(abstract) + '</div><br />\n\n'
    ntext = ntext.replace('[abstract]', abstract)
    return ntext


def get_image_path(text):
    """Get image path for l(ine)."""

    def get_image_path(l):
        """Get image path for l(ine).

        :rtype: string, line
        """
        rx = re.compile('\!\[\]\((?P<filename>.+)\)').search(l)

        if rx:
            path_new = '<a data-lightbox="note" href="' + PATH_TO_IMG + '/' + rx.group('filename') +'"><img src="' + PATH_TO_IMG + '/' + rx.group('filename') +'"></a> \n'
            return path_new
        else:
            return l

    ntext = ''
    for l in text.split('\n'):
        l = get_image_path(l)
        ntext += l + '\n'
    ntext = change_todo_square_chainbox_or_icon(ntext)
    return ntext


def get_youtube_embeds(text):
    ntext = ''

    for l in text.split('\n'):
        if l.strip().startswith('[yt:'):
            video_id = l.replace('[yt:','').replace(']','').strip()
            logger.info('youtube video detected: %s', video_id)
            l = '<iframe width="800" height="441" src="https://www.youtube.com/embed/' + video_id + '" frameborder="0" allowfullscreen></iframe>'
        ntext += l + '\n'
    return ntext


def right_MD_from_webservices(text):
    """ Just paste the url generated by Dropbox to convert it in a markdown img """
    changed = False
    for l in text.split('\n'):
        rx = re.compile('https://www.dropbox.com/(?P<img_id>.+)\?dl=0').search(l)
        rx2 = re.compile('(?<!.)http://g.recordit.co/(?P<rec_id>.+).gif(?!.)').search(l)
        if rx:
            text = re.sub(r'https://www.dropbox.com/(?P<img_id>.+)\?dl=0',
            '![img](https://www.dropbox.com/' + rx.group('img_id') +'\?raw=1)'
            , text)
            logger.info('dropbox link detected')
            changed = True
        if rx2:
            text = re.sub(r'(?<!.)http://g.recordit.co/(?P<rec_id>.+).gif(?!.)',
                          '![rec](http://g.recordit.co/' + rx2.group('rec_id') + '.gif)',
                          text)
            logger.info('Recordit link detected')
            changed = True
    return text, changed
