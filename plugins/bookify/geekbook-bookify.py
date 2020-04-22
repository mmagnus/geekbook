#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pandoc -s -o doc.pdf part01.md part02.md
"""
from __future__ import print_function
import os
import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    #parser.add_argument('-', "--", help="", default="")

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument("-a", "--author",
                        default="Marcin Magnus")
    parser.add_argument("file", help="", default="") # nargs='+')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    dir = os.path.dirname(args.file)
    file = os.path.basename(args.file)
    full_title = file.replace('.md', '')
    title = file.replace('.md', '') #+ 'aaaaaaaaaaaaaaafasdf'
    if len(title) > 15:
        title = title[:15] + '...'
    outfn = file.replace('.md', '.epub')
    plugin_base = os.path.abspath(os.path.dirname(__file__))
    cover_file =  plugin_base + '/cover.png'
    cover_file_tmp =  plugin_base + '/cover_tmp.png'
    from PIL import Image, ImageDraw, ImageFont
    img = Image.open(cover_file)
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('/Library/Fonts/LetterGothicStd-Bold.otf', 25)
    d.text((60,200), title, font=fnt, fill=(225, 225, 225))
    img.save(cover_file_tmp)

    ##     meta_file = plugin_base + '/meta.txt'
    ##     meta = """<dc:title>%s</dc:title>
    ## <dc:creator>%s</dc:creator>""" % (title, args.author)
    ##     with open(meta_file, 'w') as f:
    ##         f.write(meta)

    cmd = "cd " + dir + " && pandoc " + file + " -o ~/Desktop/" + outfn + \
    " --toc -N --epub-cover-image='" + cover_file_tmp + "'" + \
    " --metadata=title:'" + full_title + "'  --metadata=author:'" +  args.author + "'" #+ \
    #" --data-dir='" + dir + "'"
    #"' --epub-metadata='" + meta_file + "'"
    print(cmd)
    os.system(cmd)
