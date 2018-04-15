#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
## Sat 180414
Work at home on my Mac.

Evo:
- SimRNA run for diff strategies,
- install Python, pip, and Rosetta on Malibu,
- Mar 28 13:54 a04pk evox.py

## Sat 180414
- SimRNA run for diff strategies,
- install Python, pip, and Rosetta on Malibu,
- Mar 28 13:54 a04pk evox.py

will not work if you do

Evo:

- task1
- task2

"""

from __future__ import print_function
import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("keywords", nargs='+')
    return parser

def parse_note(fn, keywords):
    txt = ''
    collecting = False
    curr_date = ''
    curr_list = ''
    for l in open(fn):
        lstrip = l.strip()
        #print(l)
        #import ipdb
        #ipdb.set_trace()
        if l.startswith('# '):
            curr_week = l
        if l.startswith('## '):
            curr_date = l
        if collecting is True:  # empty line
            if not lstrip.startswith('-'):
                collecting = False
                if curr_week not in txt:
                    txt += curr_week #+ '\n'

                txt += curr_date #+ '\n'
                txt += curr_list
                txt += '\n'
                curr_list = ''

        if collecting:
            curr_list += l.strip() + '\n'

        if not collecting:
            collecting = keywords_in_line(l, keywords)
            if collecting:
                curr_list += l.strip() + '\n'
    return txt


def keywords_in_line(l, keywords):
    for keyword in keywords:
        if l.lower().strip().startswith(keyword.lower()):  # evo:
            return True
    return False


if __name__ == '__main__':
    # parser = get_parser()
    # args = parser.parse_args()

    # fn = "/home/magnus/Dropbox/geekbook/notes/test-project.md" #  workbook.md" # test-project.md" #
    fn = "/home/magnus/Dropbox/geekbook/notes/workbook.md" # test-project.md" #
    keywords = ['evo', 'rna evolution-based modeling']
    txt = parse_note(fn, keywords)
    print(txt)
