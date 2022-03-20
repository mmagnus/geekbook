#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Page - one note is a page.

Example::

     $ python page.py /Users/magnus/workspace/geekbook-export geekbook-export.md test.md --readme test.md --add-toc --push

"""
import markdown
import codecs
from mdx_gfm import GithubFlavoredMarkdownExtension

import os
from os import sep
from shutil import copy

from engine.postprocessing import (add_title,
                                   add_head_for_flask, change_data_tag_into_actual_data,
                                   add_path_to_img, change_html_tags_bootstrap,
                                   unhighlight, personal_tags_to_html, get_todo, get_captions,
                                   get_divhr, use_icons)

from engine.preprocessing import (include_md_files, get_image_path, get_youtube_embeds, get_abstract,
                                  include_file, make_interna_links, make_sport_links, tablify_images,
                                  update_upper_note,
                                  misc_on_text, color_dna)

from engine.conf import PATH_TO_MD, PATH_TO_HTML, PATH_TO_ORIG, FIND_FILES_PLUGIN, ADD_EXTRA_SPACE_FOR_NOTES
from engine.make_tableofcontent import make_table_of_content
from engine.plugins.find_files import find_files

import logging
logger = logging.getLogger('geekbook')


class Page(object):
    """Page class

    Attributes:

      fn - filename of the note, with .md
      md - md content of the note
      html - html content of the note

    """

    def __init__(self, fn):
        """Init a Page and load the content of MD file into self.md"""
        self.fn = fn
        self.name = fn.replace('.md', '')
        # it catches errors if the file is removed
        try:
            with codecs.open(PATH_TO_MD + sep + fn, "r", "utf-8") as f:
                self.md = f.read()
            self.html = ''
        except IOError:
            # logging.error('file removed ' + self.fn)
            self.md = None

    def to_pdf(self):
        with open(PATH_TO_MD + sep + self.fn) as f:
             md = f.read()
        md = md.replace('.DARK.jpeg', '.LIGHT.jpeg')
        md = md.replace('\n', '\n\n')
        md = md.replace('{{TOC}}', '')
        # revert all images dark
        import cv2
        import numpy as np
        # pip install opencv-python
        # taken from
        # https://github.com/imneonizer/How-to-find-if-an-image-is-bright-or-dark.git
        def isbright(image, dim=10, thresh=0.5):
            # 0.2 smaller more dark will be dark
            # 0.8 almost all is dark!
            # Resize image to 10x10
            image = cv2.resize(image, (dim, dim))
            # Convert color space to LAB format and extract L channel
            L, A, B = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
            # Normalize L channel by dividing all pixel values with maximum pixel value
            L = L/np.max(L)
            # Return True if mean is greater than thresh else False
            return np.mean(L) > thresh

        import re
        print(md)
        imgs = re.findall('\!\[.*\]\(imgs/(.+)\)', md)
        print(imgs)
        for i in imgs:
            impath = PATH_TO_MD + '/imgs/' + i

            # resize
            if 0:
                newpath = i
                print('make smaller')
                cmd = '/opt/homebrew/bin/convert %s -resize 400x400 /tmp/%s' % (impath, i)#newpath)
                os.system(cmd)
                print('(/tmp/' + i)
                md = md.replace('(imgs/' + i, '(/tmp/' + i)

            # check brightness
            image = cv2.imread(impath)
            if isbright(image, thresh=0.39):
                pass
            else:
                newpath = i
                cmd = '/opt/homebrew/bin/convert %s -channel RGB -negate /tmp/%s' % (impath, i)#newpath)
                os.system(cmd)
                print('(/tmp/' + i)
                md = md.replace('(imgs/' + i, '(/tmp/' + i)
                
        #aaaaaaa
        if 0:
            md = md.replace('.jpeg)', '.jpeg.small.jpeg)') #        {width=90%}
            md = md.replace('.jpg)', '.jpg.small.jpg)')
            md = md.replace('.png)', '.png.small.png)')
            # for i in ls *png; do magick $i -resize 50% $i.small.png; done
        
        if 0:
            md = md.replace('.jpeg)', '.jpeg){ height=200px }') #        {width=90%}
            md = md.replace('.jpg)', '.jpg){height=200px}')
            md = md.replace('.png)', '.png){height=200px}')


        md = md.replace('(imgs/', '(' + PATH_TO_MD + '/imgs/')

        md += '# Notes\n\n'
        md += '|\n\n' * 50 + '\n' # add an empty page
        tmp = '/tmp/print.md'
        #tmp = PATH_TO_MD + sep + '/tmp.md'
        with open(tmp, 'w') as f:
            f.write(md)
        # PATH_TO_MD + sep + self.fn
        # cd ' + PATH_TO_MD + ' &&
        cmd = 'pandoc ' + tmp + ' -o ~/Dropbox/boox/geekbook/' + self.name + '.pdf -N --toc  --metadata=title=' + self.name + '  -f gfm -V mainfont="Helvetica" --pdf-engine=xelatex -V geometry:"top=3cm, bottom=3cm, left=3cm, right=3cm" &'
        print(cmd)
        os.system(cmd)
        
    def get_html(self):
        """Compile md to get html"""
        self.html = markdown.markdown(
            self.md, extensions=[GithubFlavoredMarkdownExtension(), 'footnotes'])  # (linenums=False)'])
        # html = '<link rel="stylesheet" href="/home/magnus/Dropbox/lb_v2/templates/Pygments/css/pygments.css" type="text/css">' + html

    def compile(self):
        """Preprocess, compile, postprocess.
        """
        logger.info('compiling --> %s' % self.fn)
        self.pre_process()
        self.get_html()
        self.post_process()
        self.to_pdf()

    def pre_process(self):
        """Do preprocessing.

        E.g.::

           self.md = get_image_path(self.md)"""
        self.md = update_upper_note(self.md)
        self.md = tablify_images(self.md)
        self.md = include_md_files(self.md)
        self.md = include_file(self.md)
        self.md = get_image_path(self.md)
        self.md = get_youtube_embeds(self.md)
        self.md = get_abstract(self.md)
        self.md = get_captions(self.md)
        self.md = make_interna_links(self.md)
        self.md = make_sport_links(self.md)
        self.md = misc_on_text(self.md)
        # self.md = right_link_from_dropbox_screenshot(self.md)

    def post_process(self):
        """Do postprocessing"""
        self.html = make_table_of_content(self.fn, self.html)
        self.html = add_head_for_flask(self.html)
        self.html = change_data_tag_into_actual_data(self.fn, self.html)
        self.html = add_path_to_img(self.html)
        self.html = change_html_tags_bootstrap(self.html)
        self.html = unhighlight(self.html)
        self.html = personal_tags_to_html(self.html)
        if FIND_FILES_PLUGIN:
            self.html = find_files(self.html)
        self.html = color_dna(self.html)
        self.html = get_todo(self.html)
        self.html = add_title(self.html, self.fn)
        self.html = use_icons(self.html)
        self.html = get_divhr(self.html)
        if ADD_EXTRA_SPACE_FOR_NOTES:
            self.html += "<div class='notes'></div>"

    def export(self, path, add_toc, push, readme):
        import re
        import shutil

        content = open(PATH_TO_MD + self.fn).read()
                       
        if self.fn == readme:
             self.fn = 'README.md'
        
        with open(path + os.sep + self.fn, 'w') as f:
            f.write(content)
        try:
            os.mkdir(path + os.sep + 'imgs')
        except:
            pass

        with open(path + os.sep + 'imgs/__place_for_your_imgs__', 'w') as f:
            f.write('__place_for_your_imgs__')

        # \!\[.*?\]\(imgs/.*?\)
        hits = re.findall('\"/imgs/.*?\"', content, re.M|re.DOTALL)
        for h in hits:
            print('Copy ',h.strip())
            shutil.copy(PATH_TO_MD + h.replace('"',''), path + os.sep + 'imgs')

        import subprocess

        def exe(cmd):
            o = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = o.stdout.read().strip().decode()
            err = o.stderr.read().strip().decode()
            return out, err

        if add_toc:
            out, err = exe('gh-md-toc ' + path + os.sep + self.fn)

            with open(path + os.sep + self.fn) as f:
                content = f.read()

            ncontent = content.replace('{{TOC}}',out)

            with open(path + os.sep + self.fn, 'w') as f:
                 f.write(ncontent)

        if push:
            print('Push ...')
            out, err = exe("cd " + path + "&& git add *.md; git add imgs/* && git commit -m 'update' && git push")
            print(err)

    def is_changed(self):
        """Check if the file on disc is different than `md`.

        Make PATH_TO_ORIG if it does not exists.

        Return:
          boolean
        """
        # check if self.md exits, it does not exist if __ini__ failed (and it fails when the
        # file is removed
        if self.md:
            if not os.path.exists(PATH_TO_ORIG):
                os.makedirs(PATH_TO_ORIG)

            try:
                with codecs.open(PATH_TO_ORIG + sep + self.fn, "r", "utf-8") as f:
                    orig_md = f.read()
            except IOError:
                logging.error('file not detected. Create it: ' + self.fn)
                orig_md = ''
                pass

            if self.md != orig_md:
                copy(PATH_TO_MD + sep + self.fn, PATH_TO_ORIG + sep + self.fn)
                return True
            else:
                return False

    def save(self):
        """Save html file to the drive"""
        if not os.path.exists(PATH_TO_HTML):
            os.mkdir(PATH_TO_HTML)

        with codecs.open(PATH_TO_HTML + self.fn.replace('.md', '.html'), "w", "utf-8") as outfn:
            outfn.write(self.html)

import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    #parser.add_argument('-', "--", help="", default="")
    parser.add_argument("--add-toc", help="replace {{TOC}} of your note with TOC generated with https://github.com/ekalinin/github-markdown-toc.go, make sure that this tool is seen in your PATH", action="store_true")
    parser.add_argument("--push", help="run cd <path> && git add README.md; git add imgs/* && git commit -m 'update' && git push", action="store_true")
    parser.add_argument("--readme", help="select this md file as README, .e.g., geekbook-export.md")

    parser.add_argument("exportto", help="a path to repo to export to", default="") # nargs='+')
    parser.add_argument("file", help="", default="a note to be pushed, with .md, e.g., geekbook-export.md", nargs='+')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if list != type(args.file):
        args.file = [args.file]

    for f in args.file:
        p = Page(f)
        p.compile()
        p.is_changed()
        p.save()

        p.export(args.exportto, args.add_toc, args.push, args.readme)
