#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is a set of functions that work on HTML file, after compiling them based on Markdown."""

import sys
import re
import datetime
import os

import time
import logging
logger = logging.getLogger('geekbook')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, CssLexer, EmacsLispLexer, BashLexer, HexdumpLexer, DjangoLexer
from pygments.formatters import HtmlFormatter

from engine.conf import PATH_TO_BASE_IMG, PATH_TO_TEMPLATE, PATH_TO_TEMPLATE_HTML, PATH_TO_HTML, PATH_TO_MD


def change_data_tag_into_actual_data(mdfn, text):
    """change [date] OR {{date}} into actual date"""
    date = time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(PATH_TO_MD + mdfn)))
    text = text.replace('[date]', date)
    text = text.replace('{{date}}', date)
    return text


def personal_tags_to_html(text):
    """ insert here your personal tags!"""
    # Change text background depending on text contest.
    # warning text
    text = text.replace('[!warning]', '<p class="bg-warning">')
    text = text.replace('[warning!]', '<br></p>')
    # danger text
    text = text.replace('[!danger]', '<p class="bg-danger">')
    text = text.replace('[danger!]', '<br></p>')
    # succes text
    text = text.replace('[!success]', '<p class="bg-success">')
    text = text.replace('[success!]', '<br></p>')
    # info text
    text = text.replace('[!info]', '<p class="bg-info">')
    text = text.replace('[info!]', '<br></p>')

    return text


def add_head_for_flask(text):
    head = open(PATH_TO_TEMPLATE_HTML).read()
    head = head.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')
    head = head.replace('href="img/', 'href="' + '/img/')
    head = head.replace('="lib/', '="' + '/lib/')
    head = head.replace('="css/', '="' + '/css/')
    head = head.replace('="js/', '="' + '/js/')

    # remove demo content
    head = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->',
                  r'', head, flags=re.M | re.DOTALL)
    return head + text


def add_head(text):
    """Add head html from template  """
    head = open(PATH_TO_TEMPLATE_HTML).read()
    head = head.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')

    head = head.replace('href="img/', 'href="' + PATH_TO_TEMPLATE + '/img/')
    head = head.replace('="lib/', '="' + PATH_TO_TEMPLATE + '/lib/')
    head = head.replace('="css/', '="' + PATH_TO_TEMPLATE + '/css/')
    head = head.replace('="js/', '="' + PATH_TO_TEMPLATE + '/js/')

    # remove demo content
    head = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->',
                  r'', head, flags=re.M | re.DOTALL)
    return head + text

    #head_new = ''
    # for l in head.split('\n'):
    #    if l.find('href="http://') > -1 or l.find('src="http://') > -1 or l.find('href="#') > -1:
    #        head_new += l
    #    else:
    #        l = l.replace('href=', 'href="' + PATH_TO_TEMPLATE + '"')
    #        l = l.replace('src=', 'src="' + PATH_TO_TEMPLATE + '"')
    #        head_new += l
    # return head + text


def use_icons(text):
    """
    https://www.w3schools.com/bootstrap/bootstrap_badges_labels.asp
    """
    text = text.replace('!!!', '<span class="label label-danger">!</span>')
    text = text.replace('!!', '<span class="label label-warning">!</span>')
    return(text)


def change_html_tags_bootstrap(text):
    """ searches for html tags and adds the proper bootstrap class"""
    text = text.replace('<table>', '<table class="table table-hover">')
    #text = text.replace('<img', '<img class="img-thumbnail center-block"')
    # text = text.replace('<a href="','<a target="_blank" href="')
    return(text)


def unhighlight(text):
    hits = re.findall(
        '<div class="highlight"><pre><span></span>(?P<text>.+?)</pre></div>', text, re.M | re.S)
    for h in hits:
        # print 'h',h.strip()
        if h.strip():
            if h.find('<span') == -1:  # it's note
                # print 'no span'
                h_and_context = re.findall(
                    r'<div class="highlight"><pre><span></span>' + re.escape(h) + '</pre></div>', text, re.M | re.S)
                if h_and_context:
                    h_and_context = h_and_context[0]
                    h_and_context_unhigh = h_and_context.replace(
                        '<div class="highlight">', '').replace('</pre></div>', '</pre>')
                    text = text.replace(h_and_context, h_and_context_unhigh)
            else:
                h_and_context = re.findall(
                    r'<div class="highlight"><pre><span></span>' + re.escape(h) + '</pre></div>', text, re.M | re.S)
                # print h_and_context
    return text


def add_title(text, title):
    """title is self.md, remove .md"""
    text = text.replace('<head>', '<head>\n  <title>' + title.replace('.md', '') + '</title>')
    return(text)


def add_path_to_img(text):
    text = text.replace('src="img/', 'src="' + PATH_TO_TEMPLATE + '/img/')
    return(text)


def change_todo_square_chainbox_or_icon(text, verbose=False):
    """Set of rules to replace [i] etc with <img ... >  [ OK ]"""
    # of list
    text = text.replace('<li>[ ]', '<li><input type="checkbox" />')
    text = text.replace('<li>[X]', '<li><input type="checkbox" checked="checked" />')
    text = text.replace('<li>[x]', '<li><input type="checkbox" checked="checked" />')
    # every [ ] is change
    text = text.replace('[ ]', '<input type="checkbox" />')
    text = text.replace('[X]', '<input type="checkbox" checked="checked" />')
    text = text.replace('[x]', '<input type="checkbox" checked="checked" />')
    return text


def get_todo(text):
    """Replace *in text* @todo, @inprogress and @done with `<span class="label label-danger">@todo</span>`
    and so on.

    It's not changed in headers! See `make_tableofcontent.py` to change headers
    """
    ntext = ''
    for l in text.split('\n'):
        if not l.startswith('<div id='):
            if not l.startswith('<li class="table_of_content'):  # header

                l = l.replace('#failure', '<span class="label label-danger">#failure</span>')
                #l = l.replace('#fail', '<span class="label label-danger">#fail</span>')
                #l = l.replace('@fail', '<span class="label label-danger">@fail</span>')

                l = l.replace('@todo', '<span class="label label-danger">@todo</span>')
                l = l.replace('#today', '<span class="label label-danger">#today</span>')
                l = l.replace('#tomorrow', '<span class="label label-danger">#tomorrow</span>')
                l = l.replace('#todo', '<span class="label label-danger">#todo</span>')
                l = l.replace('@inprogress', '<span class="label label-warning">@inprogress</span>')
                l = l.replace('@progress', '<span class="label label-warning">@progress</span> ')
                l = l.replace('#progress', '<span class="label label-warning">#progress</span> ')
                l = l.replace('@done', '<span class="label label-success">@done</span>')
                l = l.replace('#done', '<span class="label label-success">#done</span>')
                l = l.replace('#@k', '<span class="label label-success">@ok</span>')
                l = l.replace('#ok', '<span class="label label-success">#ok</span>')
                l = l.replace('#success', '<span class="label label-success">#success</span>')
                l = l.replace('@fixed', '<span class="label label-info">@fixed</span>')

                l = l.replace('#waiting', '<span class="label label-info">#waiting</span>')

                l = l.replace('@error', '<span class="label label-danger">@error</span>')

                l = l.replace('#True', '<span class="label label-success">True</span>')
                l = l.replace('#False', '<span class="label label-danger">False</span>')

        ntext += l + '\n'
    ntext = change_todo_square_chainbox_or_icon(ntext)
    return ntext


def get_captions(text):
    """Replace *in text* @todo, @inprogress and @done with `<span class="label label-danger">@todo</span>` and so on.
    """
    ntext = ''
    for l in text.split('\n'):
        if l.startswith('Fig.') or l.startswith('Figure.'):
            style = '<small><b style="background-color: white;">Figure.</b>'
            l = l.replace('Figure.', style)
            l = l.replace('Fig.', style)
            l += '</small>'
        ntext += l + '\n'
    return ntext

def get_divhr(text):
    """"""
    ntext = ''
    for l in text.split('\n'):
        if l.startswith('<hr />'):
            l = l.replace('<hr />', '<div style="clear:both"></div><hr>')
        # ok, this is super ugly ;( but works!
        if '<h1' in l:
            l = l.replace('<h1', '<div style="clear:both"></div><h1')
        if '<h2' in l:
            l = l.replace('<h2', '<div style="clear:both"></div><h2')
        if '<h3' in l:
            l = l.replace('<h3', '<div style="clear:both"></div><h3')
        if '<h4' in l:
            l = l.replace('<h4', '<div style="clear:both"></div><h4')
        if '<h5' in l:
            l = l.replace('<h5', '<div style="clear:both"></div><h5')
        ntext += l + '\n'
    return ntext


# main
if __name__ == '__main__':
    content = sys.stdin.read()
    # output = change_infotags_into_icon(content)
    # output = change_todo_square_chainbox_or_icon(output)
    output = change_data_tag_into_actual_data(output)
    output = add_path_to_img(output)
    output = change_html_tags_bootstrap(output)
    output = personal_tags_to_html(output)
    # output = change_tags_into_searchtaglinks(text)
    # output = remove_em(output)
    # output = include_file(output)
    # output = make_inner_link(output)
    output = pigmentize(output)
    sys.stdout.write(output)
    sys.stdout.write
