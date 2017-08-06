#!/usr/bin/env python2.7

import engine.searcher as sx
import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('phrases')
    parser.add_argument('-v', '--verbose', help='push to the server', action='store_true')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()

    # print(sx.make_db())
    sx.search_term(args.phrases)
