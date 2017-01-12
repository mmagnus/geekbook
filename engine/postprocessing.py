#!/usr/bin/python

"""This is a set of functions that work on HTML file, after compiling them based on Markdown."""

import sys
import re
import datetime
import os

import logging
logger = logging.getLogger('geekbook')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, CssLexer, EmacsLispLexer, BashLexer, HexdumpLexer, DjangoLexer
from pygments.formatters import HtmlFormatter

from engine.conf import PATH_TO_BASE_IMG, PATH_TO_TEMPLATE, PATH_TO_TEMPLATE_HTML, PATH_TO_HTML


def change_data_tag_into_actual_data(text):
    """change [date] into actual date"""
    today = datetime.date.today()
    text = text.replace('[date]', str(today))
    return text


def personal_tags_to_html(text):
    """ insert here your personal tags!"""

# Change text background depending on text contest.
## warning text
    text = text.replace('[!warning]','<p class="bg-warning">')
    text = text.replace('[warning!]','<br></p>')
# danger text
    text = text.replace('[!danger]','<p class="bg-danger">')
    text = text.replace('[danger!]','<br></p>')
# succes text
    text = text.replace('[!success]','<p class="bg-success">')
    text = text.replace('[success!]','<br></p>')
# info text
    text = text.replace('[!info]','<p class="bg-info">')
    text = text.replace('[info!]','<br></p>')

    return text


def add_head(text):
    """Add head html from template  """
    head = open(PATH_TO_TEMPLATE_HTML).read()
    head = head.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')

    head = head.replace('href="img/', 'href="' + PATH_TO_TEMPLATE + '/img/')
    head = head.replace('="lib/', '="' + PATH_TO_TEMPLATE + '/lib/')
    head = head.replace('="css/', '="' + PATH_TO_TEMPLATE + '/css/')

    # remove demo content
    head = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->', r'', head, flags=re.M | re.DOTALL)
    return head + text


    #head_new = ''
    #for l in head.split('\n'):
    #    if l.find('href="http://') > -1 or l.find('src="http://') > -1 or l.find('href="#') > -1:
    #        head_new += l
    #    else:
    #        l = l.replace('href=', 'href="' + PATH_TO_TEMPLATE + '"')
    #        l = l.replace('src=', 'src="' + PATH_TO_TEMPLATE + '"')
    #        head_new += l
    #return head + text


def change_html_tags_bootstrap(text):
    """ searches for html tags and adds the proper bootstrap class"""
    text = text.replace('<table>', '<table class="table table-hover">')
    text = text.replace('<img', '<img class="img-thumbnail center-block"')
    text = text.replace('<a href="','<a target="_blank" href="')
    return(text)


def pigmentize(text):
    """searches for <span></span> and replace with HTML pigmented code
    supported languages: python ; html ; css ; emacs ; bash ; hexdump ;
     DjangoLexer"""
    start_code = text.find('<pre>') + 5
    end_code = text.find('</pre')
    code = text[start_code:end_code]
    if code[0:5] == 'python':
        text.replace('<div class="highlight"><pre>' + highlight(code, PythonLexer(), HtmlFormatter()) + '</pre></div>')
    if code[0:4] == 'html':
        text.replace('<div class="highlight"><pre>' + highlight(code, HtmlLexer(), HtmlFormatter()) + '</pre></div>')
    if code[0:3] == 'css':
        text.replace('<div class="highlight"><pre>' + highlight(code, CssLexer(), HtmlFormatter()) + '</pre></div>')
    if code[0:5] == 'emac':
        text.replace('<div class="highlight"><pre>' + highlight(code, EmacsLispLexer(), HtmlFormatter()) + '</pre></div>')
    if code[0:4] == 'bash':
        text.replace('<div class="highlight"><pre>' + highlight(code, BashLexer(), HtmlFormatter()) + '</pre></div>')
    if code[0:7] == 'hexdump':
        text.replace('<div class="highlight"><pre>' + highlight(code, HexdumpLexer(), HtmlFormatter()) + '</pre></div>')
    if code[0:6] == 'django':
        text.replace('<div class="highlight"><pre>' + highlight(code, DjangoLexer(), HtmlFormatter()) + '</pre></div>')
    return(text)


def add_path_to_img(text):
    text = text.replace('src="img/', 'src="' + PATH_TO_TEMPLATE + '/img/')
    return(text)


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
