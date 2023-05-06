#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""This is a set of functions that work on Markdown file, before compiling them to html.

Go to page.py (Page) pre_process to add a new function from here."""

from engine.conf import PATH_TO_IMG, PATH_TO_MD, PATH_TO_ORIG
import re
import os
import codecs
import glob

import logging
logger = logging.getLogger('geekbook')
logger.setLevel(logging.INFO)

FLASK_BASED = True

def color_seq_protein(seq):
    seq_txt = ''
    protein = True
    logging.info(seq)
    raw_seq = seq.split('#')[0]
    for s in seq:
        if protein:
            if s.lower() in ["k", "r", "h"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: DodgerBlue;">' + s + '</span>'
            elif s.lower() in ["T", "t"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: green;">' + s + '</span>'
            elif s.lower() in ["d", "e"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: red;">' + s + '</span>'
            elif s.lower() in ["w", "y"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: yellow;">' + s + '</span>'
            elif s.lower() in ["m"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: orange;">^</span>'
            elif s.lower() in ["g", "a", "v", "l", "i", "f"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: LightGreen;">' + s + '</span>'
            elif s.lower() in ["s", "t", "c", "n", "q"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: green;">' + s + '</span>'
            elif s.lower() in ["p"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: pink;">' + s + '</span>'
            elif s.lower() in ["-"]:
                seq_txt += '-'
            elif s.lower() in ["*"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: black;">' + s + '</span>'
            elif s.lower() in ["\\", "/"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: lightgray;">' + s + '</span>'
        if s is '#':
            protein = False
        if not protein:
            seq_txt += s
    return seq_txt


def color_seq_dna(seq, translate=False):
    seq_txt = ''
    dna = True
    raw_seq = seq.split('#')[0]
    for s in seq:
        if dna:
            if s in ["A", "a"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: green;">' + s + '</span>'
            elif s in ["T", "t"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: DodgerBlue;">' + s + '</span>'
            elif s in ["U", "u"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: DodgerBlue;">' + s + '</span>'
            elif s in ["G", "g"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: red;">' + s + '</span>'
            elif s in ["C", "c"]:
                seq_txt += '<span style="font-family: Menlo,Monaco,Consolas,Courier New,monospace; background-color: orange;">' + s + '</span>'
            else:
                seq_txt += s
        if s is '#':
            if translate:
                from Bio.Seq import Seq
                from Bio.Alphabet import generic_dna, generic_protein
                seq = Seq(raw_seq)
                protein = seq.translate()
                protein_txt = ''
                for p in str(protein):
                     protein_txt += '\\' + p + '/'
            dna = False
        if not dna:
            seq_txt += s

    if translate:
        return seq_txt + '\n' + color_seq_protein(protein_txt)
    else:
        return seq_txt


def color_dna(text):
    ntext = ''
    for l in text.split('\n'):
        if '#coldna' in l:
            translate = False
            if '+prot' in l:
                translate = True
            ntext += color_seq_dna(l, translate) + '\n' # + '<b>SUMMARY</b>'
        if '#colprot' in l:
            ntext += color_seq_protein(l) + '\n' # + '<b>SUMMARY</b>'            
        else:
            ntext += l + '\n'
    return ntext

def change_todo_square_chainbox_or_icon(text, verbose=False):
    """Set of rules to replace [i] etc with <img ... >  [ OK ]"""
    # of list
    text = text.replace('<li>[ ]', '<li><input type="checkbox" />')
    text = text.replace('<li>[X]', '<li><input type="checkbox" checked="checked" />')
    # every [ ] is change
    #text = text.replace('[ ]','<input type="checkbox" />')
    #text = text.replace('[X]','<input type="checkbox" checked="checked" />')
    return text


def misc_on_text(text, verbose=False):
    """Set of rules to replace [i] etc with <img ... >  [ OK ]"""
    # of list
    ntext = ''
    for l in text.split('\n'):
        if l == '<summary>':
            ntext += l # + '<b>SUMMARY</b>'
        else:
            ntext += l + '\n'
    return ntext

def format_orgmode_statistcs(text, verbose=False):
    # !!!!!!!!!!!!
    ntext = ''
    for l in text.split('\n'):
        if l.startswith(' |'):
            l = '   ' + l
        ntext += l + '\n'
    #text = text.replace(' | ', '    |')
    return ntext

def get_abstract(text):
    """Collect all lines starting with ``! `` and insert it as in abstract in a place tagged as [abstract].

    Now you can use ** to bold some text.
    You can use \\ to introduce a break (</br>).
    """
    ntext = ''
    abstract = []

    abstract_flag = False
    for l in text.split('\n'):
        if l.strip() == '[abstract]':
            abstract_flag = True
        if l.startswith('! '):
            if abstract_flag:
                # my own converter from **XX** to <b>XX</b>
                rx = re.findall('\*\*(?P<tobold>.+?)\*\*', l)
                for r in rx:
                    print(r)
                    l = l.replace('**' + r + '**', '<b>' + r + '</b>')
                #
                # \\ -> </br>
                abstract.append(l[1:].replace('\\\\', '</br>'))
            l = '<div class="abstract"> ' + l[1:] + '</div>'
        # this is conversion of lines along the note, remove \\ but don't convert into br/
        ntext += l.replace('\\\\', '') + '\n'
    abstract = '<div class="abstract">' + ' '.join(abstract) + '</div><br />\n\n'
    ntext = ntext.replace('[abstract]', abstract)
    return ntext


def make_interna_links(text, verbose=False):
    """
    Convert::
    
    [file:openfold-structure-module-meeting-230428.md]

    into::

      <a href="http://127.0.0.1:5000/view/openfold-structure-module-meeting-230428.html">openfold-structure-module-meeting-230428</a>
    """
    ntext = ''
    for l in text.split('\n'):
        # [file:xxxx.md]
        rx = re.findall('\[file\:(?P<filename>.+?)\]', l)
        for r in rx:
            if '/' in r:  # that means that's a folder /Users/magnus/work/evo-extra
                l = l.replace('[file:' + r + ']', '<a href="http://127.0.0.1:5000/view' + r.replace('.md', '.html') + '">' +
                              r.replace('.md','') + '</a>')
            else:
                #l = l.replace('[file:' + r + ']', '<a href="http://127.0.0.1:5000/view/' + r.replace('.md', '.html') + '">' + r.replace('.md','') + '</a>')
                l = l.replace('[file:' + r + ']', '[' + r.replace('.md','') + '](http://127.0.0.1:5000/view/' + r.replace('.md', '.html') + ')')
            if verbose: print(l)
        ntext += l + '\n'
    return ntext

def make_sport_links(text, verbose=False):
    ntext = ''
    for l in text.split('\n'):
        # [file:xxxx.md]
        rx = re.findall('\[sport\:(?P<date>.+?)\]', l)
        for r in rx:
            # 181203
            y = r[:2]
            m = r[2:4]
            d = r[4:]
            print(rx, y, m, d)
            l = '<a target="_top" href="http://www.myfitnesspal.com/food/diary?date=20%s-%s-%s">MFP</a> ' % (y, m, d)
            l += '<a target="_top" href="https://connect.garmin.com/modern/daily-summary/mmagnus/20%s-%s-%s">Garmin Connect</a>' % (y, m, d)
            if verbose: print(l)
        ntext += l + '\n'
    return ntext


def tablify_images(text):
    """Introduce || between images that are in the same line, hereby making images be presented
    in a table, side by side.

    So this::

          .png) ![](imgs/39387.jpg)

    will be processed into::

          png) || [](imgs/39387.jpg)

    and this will be tablified by Geekbook.

      Args:
         text (str): the whole note in Markdown, easy to be split with .split('\n')

      Returns:
         ntext (str): processed note in Markdown

    """
    ntext = ''
    for l in text.split('\n'):
        l = l.replace(')![', ') || ![')
        l = l.replace(') ![', ') || ![')
        ntext += l + '\n'
    return ntext


def get_image_path_in_line(l):
    """Update: work also with more than one link per line and with tables.
    Update (2): you can also define width and height of your images.

    Only width, e.g.::

      ![](imgs/Screen_Shot_2017-02-12_at_1.17.04_AM.png =500x)

    only height::

      ![](imgs/Screen_Shot_2017-02-12_at_1.17.04_AM.png =x400)

    and both::

      ![](imgs/Screen_Shot_2017-02-12_at_1.17.04_AM.png =400x400)

    You can use internal variable log to switch on and off logging.

    You can also position your images using the following syntax::

       ![#left](imgs/fig1.png)

    where ``#left`` can be replaced with::

       #mini = width:25%;
       #icon = width:5%;
       #half = width:50%
       #full = max-height:100%;
       #scan = max-height:100%;
       #short =  max-height:400px;

    """
    # The details of parsing, i'm using a loop over zipped lists::
    #
    # rall = ['![](imgs/ss_gab.png)', '![](imgs/Screen_Shot_2017-02-12_at_1.17.04_AM.png =500x)']
    # r = ('', 'imgs/ss_gab.png')
    log = True
    rx = re.findall('\!\[(?P<alt>.*?)\]\((?P<filename>.+?)\)', l)
    rall = re.findall('(?P<all>\!\[.*?\]\(.+?\))', l)
    for r, ra in zip(rx, rall):
        alt, name = r  # ('', 'imgs/ss_gab.png')

        # options in []
        style = ''
        if '#left' in alt:
            style = "float: left;  margin: 0 15px 0 0;"

        if '#mini' in alt:
            style += "width:25%;"

        if '#icon' in alt:
            style += "width:5%;"

        if '#center' in alt:
            style += "margin-left: auto; margin-right: auto;"

        if '#half' in alt:
            style += "width:50%;"

        if '#full' in alt:
            style += "max-height:100%;"

        if '#scan' in alt:
            style += "max-height:100%;"

        if '#' in alt:
            style += "max-height:100%;"

        if '#short' in alt:
            style += "max-height:400px;"

        width_html = ''
        height_html = ''
        if name.find(' =') > -1:
            name, dim = name.replace(')', '').split(' =')
            name = name.strip()
            width, height = dim.split('x')  # =500x
            if width:
                width_html = "width:" + width + "px;"
            if height:
                height_html = "height:" + height + "px;"

        # if this is an external link then name is href
        if name.startswith('http'):
            if log:
                logger.info('http image link %s', name)
            path_new = '<a data-lightbox="note" href="' + name + '"><img style="' + \
                width_html + height_html + '" src="' + name + '"></a>'
        else:  # if local then name is a part of full href (PATH_TO_IMG / name)
            if log:
                logger.info('image %s', name)
            if FLASK_BASED:
                path_new = '<a data-lightbox="note" href="/' + name + '"><img style="' + width_html + height_html + style + '" src="/' + name + '"></a>'
            else:
                path_new = '<a data-lightbox="note" href="' + PATH_TO_IMG + '/' + name + '"><img style="' + \
                    width_html + height_html + '" src="' + PATH_TO_IMG + '/' + name + '"></a>'
        l = l.replace(ra, path_new)

        # if || side by side
        if l.find('||') > -1:
            l = '<table class="table table-hover"><tbody><tr><td>' + \
                l.replace('||', '</td><td>') + '</td></tr></tbody></table>'

    return l


def get_image_path(text):
    """Get image path for text. See get_image_path_in_line (to get links per line) to learn more."""
    ntext = ''
    for l in text.split('\n'):
        l = get_image_path_in_line(l)
        ntext += l + '\n'
    ntext = change_todo_square_chainbox_or_icon(ntext)
    return ntext


def get_youtube_embeds(text):
    ntext = ''

    for l in text.split('\n'):
        if l.strip().startswith('[yt:'):
            video_id = l.replace('[yt:', '').replace(']', '').strip()
            logger.info('youtube video detected: %s', video_id)
            l = '<iframe width="800" height="441" src="https://www.youtube.com/embed/' + \
                video_id + '" frameborder="0" allowfullscreen></iframe>\n' + \
                '<https://www.youtube.com/watch?v=' + video_id + '>'
        ntext += l + '\n'
    return ntext


def include_md_files(md, remove_first_line=False):
    """Whenever you see /<file.md> include content of this file in here.

    Args:

       md (str): context of a md file
       remove_first_line (bool): True if you want to skip the first line of included file
                                 usually to remove the file's top header, e.g. `# Noting`
    Returns:

       str: new md (nmd)

    """
    imported_files_list = ''
    nmd = ''
    for l in md.split('\n'):
        # /[file:XXX.md]
        if l.strip().startswith('/[file:'):
            logger.info(l)
            # skip the first line
            loriginal = l
            del1 = False
            if '=del1' in l:
                l = l.replace('=del1', '')
                del1 = True

            shift1 = False
            if '=shift1' in l:
                l = l.replace('=shift1', '')
                shift1 = True

            shift2 = False
            if '=shift2' in l:
                l = l.replace('=shift2', '')
                shift2 = True

            shift3 = False
            if '=shift3' in l:
                l = l.replace('=shift3', '')
                shift3 = True
            # ^ very repetitive code, should be fixed at some point

            file_fn = l.replace('/[file:', '').replace(']', '').strip()
            file_fn_html = file_fn.replace('.md', '.html')
            nmd += '<pre> Imported MD file [%s]: <a href="http://127.0.0.1:5000/view/%s"</a>%s</pre>\n' % (loriginal , file_fn, file_fn_html)
            try:
                with codecs.open(PATH_TO_MD + os.sep + file_fn, "r", "utf-8") as f:
                    if del1:
                        f.readline()
                    f = f.read()
                    # delete toc
                    f = f.replace('{{TOC}}', '')
                    f = f.replace('[tableofcontent]', '')
                    if shift1 or shift2 or shift3:
                        nt = ''
                        for l in f.split('\n'):
                            if l.startswith('#'):
                                if shift1:
                                    l = l.replace('# ', '## ')
                                if shift2:
                                    l = l.replace('# ', '### ')
                                if shift3:
                                    l = l.replace('# ', '#### ')
                            nt += l + '\n'
                        f = nt
                        logger.info('include file: shift by 1')
                    nmd += f
            except IOError:
                logger.info('include file -- file not found -- %s', file_fn)
            else:
                logger.info('include file detected: %s', file_fn)


        if l.startswith('/') and l.endswith('*') and l.count('/') == 1:  # /wet*
            mdname = l.replace('/', '').strip()
            files = glob.glob(PATH_TO_MD + os.sep + mdname)
            for f in files:
                ffullpath = f
                if os.path.isfile(ffullpath):
                    with codecs.open(ffullpath, "r", "utf-8") as f:
                        if remove_first_line:
                            next(f)  # skip first line? hack to get rid of # Title of the note
                        txt = f.read()
                        #
                        shift1 = True
                        if shift1:
                            nt = '# ' + os.path.basename(ffullpath) + '\n' # start with a file name ?
                            for l in txt.split('\n'):
                                if l.startswith('#'):
                                    if shift1:
                                        l = l.replace('# ', '## ')
                                nt += l + '\n'
                            txt = nt
                        # remove table of content for this included note
                        txt = txt.replace('{{TOC}}', '')
                        txt = txt.replace('[tableofcontent]', '')
                        nmd += '<p><div class="alert alert-info">Imported <a href="http://127.0.0.1:5000/view/' + os.path.basename(ffullpath) + \
                               '">' +  os.path.basename(ffullpath) + '</a></div></p>'
                        nmd += '\n' + txt + '\n'
                        imported_files_list += '/' + os.path.basename(f.name) + '\n'

            with open(PATH_TO_MD + os.sep + 'topdf/' + mdname.replace('*', '') + 'x.md', 'w') as f:
                f.write(nmd)
            
        if l.startswith('/') and l.endswith('.md') and l.count('/') == 1:  # /shell.md
            ffullpath = PATH_TO_MD + os.sep + l.replace('/', '').strip()
            mdname = l.replace('/', '').strip()
            # check if exists
            if os.path.isfile(ffullpath):
                with codecs.open(ffullpath, "r", "utf-8") as f:
                    if remove_first_line:
                        next(f)  # skip first line? hack to get rid of # Title of the note
                    txt = f.read()
                    # remove table of content for this included note
                    txt = txt.replace('{{TOC}}', '')
                    txt = txt.replace('[tableofcontent]', '')
                    nmd += '<p><div class="alert alert-info">Imported <a href="http://127.0.0.1:5000/view/' + mdname + '">' + mdname + '</a></div></p>'
                    nmd += '\n' + txt + '\n'
            else:
                nmd = '@error The file can not be found: ' + l + '\n' + nmd  # at this info at the beginning of the file


        else:
            nmd += l + '\n'
    if imported_files_list:
        nmd = '```\n' + imported_files_list + '```\n' + nmd # add list pre
    return nmd


def include_file(text):
    """This is to import any file. If you want to import a note form your Geekbook use

    include_md_files()
    """
    ntext = ''

    for l in text.split('\n'):
        if l.strip().startswith('[if:'):
            file_fn = l.replace('[if:', '').replace(']', '').strip()
            ntext += '<kbd> Imported file: %s </kbd>\n' % file_fn
            try:
                with codecs.open(PATH_TO_MD + os.sep + file_fn, "r", "utf-8") as f:
                    ntext += f.read()
            except IOError:
                logger.info('include file -- file not found -- %s', file_fn)
            else:
                logger.info('include file detected: %s', file_fn)


        ntext += l + '\n'
    return ntext


def update_upper_note(text):
    ntext = ''
    for l in text.split('\n'):
        if l.strip().startswith('^[file:'):
            filename = l.replace('^[file:', '').replace(']', '').strip()
            try:
                os.remove(PATH_TO_ORIG + os.sep + filename)
                logger.info('Remove %s to force updating the page... OK', filename)
            except OSError:
                l = l + ' <span class="label label-danger"> The file not found</span>'
                logger.info('Remove %s to force updating the page... The file not found', filename)
        ntext += l + '\n'
    return ntext

# main
if __name__ == "__main__":
    l = "![](imgs/Screen_Shot_2018-08-14_at_11.29.30_AM.png)"
    print(get_image_path_in_line(l))

    l = "![#left](imgs/Screen_Shot_2018-08-14_at_11.29.30_AM.png)"
    print(get_image_path_in_line(l))
