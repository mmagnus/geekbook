#!/usr/bin/python

"""
"""

import sys
import re
import datetime
import os

from geekbook.engine.conf import PATH_TO_BASE_IMG, PATH_TO_TEMPLATE, PATH_TO_TEMPLATE_HTML, PATH_TO_HTML




def change_data_tag_into_actual_data(text):
    """change [date] into actual date"""
    today = datetime.date.today()
    text = text.replace('[date]', str(today))
    return text

def change_todo_square_chainbox_or_icon(text, verbose=False):
    """
    Set of rules to replace [i] etc with <img ... >

    [ OK ]
    """
    ## of list
    text = text.replace('<li>[ ]', '<li><input type="checkbox" />')
    text = text.replace('<li>[X]', '<li><input type="checkbox" checked="checked" />')
    ## every [ ] is change
    text = text.replace('[ ]','<input type="checkbox" />')
    text = text.replace('[X]','<input type="checkbox" checked="checked" />')
    return text

def add_head(text):
    """Add head html from template
    """
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
    #tables
    text = text.replace('<table>', '<table class="table table-hover">')
    text = text.replace('<h2>', '<br><hr><br><h2>') #add contest separator


    return(text)


def add_path_to_img(text):
    text = text.replace('src="img/', 'src="' + PATH_TO_TEMPLATE + '/img/')
    return(text)

if __name__ == '__main__':
    content = sys.stdin.read()
    output = change_infotags_into_icon(content)
    output = change_todo_square_chainbox_or_icon(output)
    output = change_data_tag_into_actual_data(output)
    output = change_html_tags_bootstrap(output)
    #output = change_tags_into_searchtaglinks(text)
    #output = remove_em(output)
    output = include_file(output)
    #output = make_inner_link(output)
    output = add_path_to_img(output)
    sys.stdout.write(output)
    sys.stdout.write
