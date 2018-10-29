#!/usr/bin/env python

"""search for @future

grep 'date' ~/Dropbox/geekbook/notes/ eng* -n -A 15

"""
import os
import sys
import re
from engine.colors import bcolors
from engine.conf import PATH_TO_MD

if __name__ == '__main__':
    #print (bcolors.OKGREEN + '// geekbook search for <for> in <in> //' +  bcolors.ENDC)
    action = 'search'  # sys.argv[1] # search
    curr = os.getcwd()
    os.chdir(PATH_TO_MD)

    v = True
    # if action == 'search':
    if 1:
        ################################################################################
        # for
        if ' '.join(sys.argv[:]).find('for') == -1:
            raise Exception('Missing for in your query')
        if v:
            print (bcolors.OKGREEN + '> action:' + action + bcolors.ENDC)
        match = re.search('for (?P<for>.*)', ' '.join(sys.argv[:]))
        f = match.group('for').split('in')[0]
        if v:
            print (bcolors.OKGREEN + '\_ for:' + f + bcolors.ENDC)

        ################################################################################
        match = re.search('in (?P<in>.*)', ' '.join(sys.argv[:]))
        if match:
            searchin = match.group('in').strip().split(' n ')[0]
        else:
            searchin = '*'

        # -n forr grep
        match = re.search('n (?P<n>\d+)', ' '.join(sys.argv[:]))
        if match:
            n = match.group('n').strip()
        else:
            n = '0'
        if v:
            print (bcolors.OKGREEN + '\_ n:' + n + bcolors.ENDC)

        if v:
            print (bcolors.OKGREEN + '\_ in: ' + searchin[:200] + bcolors.ENDC)

        cmd = "grep --color=auto -i '" + f + "' " + searchin + " -n "
        if n:
            cmd += "-A " + n
        if v:
            print (bcolors.OKGREEN + '> ' + cmd[:200] + bcolors.ENDC)
        os.system(cmd + ' 2>/dev/null ')
    else:
        print 'action is missing'
    os.chdir(curr)
