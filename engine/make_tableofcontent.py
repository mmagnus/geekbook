#!/usr/bin/env python3
"""geekbook - table of content

Get markdown output and make a table of content!

h1 How my lifebook should look?
id_of_div How-my-lifebook-should-look?

changelog:

2012
 - 0831 fix of the previous point
 - 0829 make h1 clickable

"""
import sys
import re


TAG = '[tableofcontent]'
TAG2 = '{{TOC}}'  # iA TOC tag
VERBOSE = False


def tag_heading(heading):
    """Find all tags in a heading and replace it with "my" tags

    Get:
    - heading

    Return:
    - heading with "my" tags
    """
    tags = re.findall('@\w+', heading)
    for t in tags:
        if t == '@done':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-success">' + t + '</span>')
        if t == 'DONE':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-success">' + t + '</span>')
        elif t == '@progress':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-warning">' + t + '</span>')
        elif t == '@inprogress':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-warning">' + t + '</span>')
        elif t == '@todo':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-danger">' + t + '</span>')
        else:
            heading = heading.replace(t, '<span class="label label-info">' + t + '</span>')

    # also work with #<tag> not only @<tag.
    tags = re.findall('\#\w+', heading)
    for t in tags:
        if t == '#done':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-success">' + t + '</span>')
        elif t == 'DONE':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-success">' + t + '</span>')
        elif t == '#progress':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-warning">' + t + '</span>')
        elif t == '#inprogress':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-warning">' + t + '</span>')
        elif t == '#todo':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-danger">' + t + '</span>')
        elif t == '#vip':
            heading = heading.replace(
                t, '<span style="font-family:"  class="label label-danger">' + t + '</span>')
        else:
            heading = heading.replace(t, '<span class="label label-info">' + t + '</span>')
    return heading


def replace_space_with_minus(text):
    replace = text.replace(' ', '-')
    return replace


def make_table_of_content(fn, text, version2=True):
    output = ''

    list_type_start = '<div id="tableofcontent"><ul class="table_of_content" id="tableofcontent_">'
    list_type_end = '</ul></div>'

    collect_headings = list_type_start

    tableofcontent_in_pure_text = ''
    for l in text.split('\n'):
        # h1
        rx = re.compile('<h1>(?P<h1>.+)</h1>').search(l)
        if rx:
            h1 = rx.group('h1')
            if VERBOSE:
                print('h1', h1)
            id_of_div = replace_space_with_minus(h1)
            # '</div>'
            # + '<a class="nondecoration" href="#' + id_of_div + '">' \
            l = '<div id="' + id_of_div + '"><h1>' \
                + '<a class="nondecoration" href="/edit_header/' + fn.replace('.md', '') + '/%23 ' + h1.replace('#', '%23').replace('/', '%2F') + '">' \
                + tag_heading(h1) \
                + '</a></h1>'
            if VERBOSE:
                print("# l", l)
            collect_headings += '<li class="table_of_content_h1">'\
                + '<a href="#' + id_of_div + '">'\
                                + tag_heading(h1) + ' </a></li>\n'
            tableofcontent_in_pure_text += h1 + '\n'

        # h2
        rx = re.compile('<h2>(?P<h2>.+)</h2>').search(l)
        if rx:
            h2 = rx.group('h2')
            id_of_div = replace_space_with_minus(h2)
            # '</div>
            # + '<a class="nondecoration" href="#' + id_of_div + '">' \
            l = '<div id="' + id_of_div + '"><h2>' \
                + '<a class="nondecoration" href="/edit_header/' + fn.replace('.md', '') + '/%23%23 ' + h2.replace('#', '%23').replace('/', '&#47') + '">' \
                + tag_heading(h2) \
                + '</a></h2>'
            if VERBOSE:
                print("# l", l)
            collect_headings += '<li class="table_of_content_h2">'\
                                + '<a href="#' + id_of_div + '">' \
                                + tag_heading(h2) + ' </a></li>\n'
            tableofcontent_in_pure_text += '\t' + h2 + '\n'

        # h3
        rx = re.compile('<h3>(?P<h3>.+)</h3>').search(l)
        if rx:
            h3 = rx.group('h3')
            id_of_div = replace_space_with_minus(h3)
            # '</div>
            l = '<div id="' + id_of_div + '"><h3>' \
                + '<a class="nondecoration" href="/edit_header/' + fn.replace('.md', '') + '/%23%23%23 ' + h3.replace('#', '%23').replace('/', '&#47') + '">' \
                + tag_heading(h3) \
                + '</a></h3>'
            if VERBOSE:
                print("# l", l)
            collect_headings += '<li class="table_of_content_h3">'\
                                + '<a href="#' + id_of_div + '">' \
                                + tag_heading(h3) + ' </a></li>\n'
            tableofcontent_in_pure_text += '\t\t' + h3 + '\n'

        output += l + '\n'

    collect_headings += list_type_end + '\n'

    # not necessary
    # f = open(PATH_TABLE_OF_CONTENT + sep + 'toc.txt', 'w')
    # f = open('/home/magnus/Dropbox/lb_v2/data/toc.txt', 'w') # @todo
    # f.write(tableofcontent_in_pure_text)
    # f.close()

    if version2:
        output = output.replace(TAG, collect_headings)
        output = output.replace(TAG2, collect_headings)
    else:
        # out of order
        sys.stdout.write('<!-- TABLE -->' + '\n')
        sys.stdout.write(collect_headings)
        sys.stdout.write('<!-- END TABLE -->' + '\n')
        ####
    return output


def start(): pass


if __name__ == '__main__':
    text = sys.stdin.read()
    output = make_table_of_content(text)
    sys.stdout.write(output)
    # tag_heading('How to setup priorities? # @priority @test @pla')
