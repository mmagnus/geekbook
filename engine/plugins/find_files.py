#!/usr/bin/env python

"""Search for [ff:..]  with (g)locate make a link. """

import sys
import re
import platform
import os

import logging
logger = logging.getLogger('geekbook')


def file_search(filename, verbose):
    logger.info('find file:' + filename)
    import commands
    if platform.system() == "Linux":
        out = commands.getoutput('locate ' + filename)
    if platform.system() == "Darwin":
        out = commands.getoutput('glocate ' + filename)
    first_hit = out.split('\n')[0]
    logger.info(out)
    if not first_hit:
        logger.info('not found')
    else:
        logger.info('hit ' + first_hit)
    return os.path.dirname(first_hit), first_hit
    
def find_files(text, verbose=False):
    output = ''
    msg_listofnotfoundfiles = ''
    for l in text.split('\n'):
        rx = re.compile('\[ff:(?P<file>.+?)\]').search(l)
        if rx:
            filename = rx.group('file')
            if verbose: print '# filename: ', filename
            folderpath, filepath = file_search(filename, False)
            if folderpath:
                if verbose: print '# file_finder.search()', output
                output += l.replace('[ff:' + filename + ']',' <a href="' + folderpath + '"><code>[+]</code></a> ' + '<a href="' + filepath + '"> <span class="mantext">' + os.path.basename(filepath) + '</span></a>')

                #output += l.replace('[file:' + filename + ']',' <a href="' + folderpath + '"><img class="manicon" src="' + PATH_TO_BASE_IMG + 'folder.png"></a> ' + '<a href="' + filepath + '"> <span class="mantext"> ' + os.path.basename(filepath) + '</span></a>')
            else:
                if verbose: print 'problem: can not find ' + filename
                output += l.replace('[ff:' + filename + ']', '<span style="color:red">' + filename + '</span>')
                #output += l.replace('[ff:' + filename + ']','<img class="manicon" src="' + PATH_TO_BASE_IMG + 'error.png"> <span style="color:red"><b>' + filename + '</b></span>')
                msg_listofnotfoundfiles += filename + '\n'
        else:
            output += l + '\n'
    ##
    output = output.replace('..MSGNOTFOUNDFILES..', msg_listofnotfoundfiles)
    return output

if __name__ == '__main__':
    #text = sys.stdin.read()
    text = """
    [ff:XQxIC1CrCP.gif]
    """
    output = find_files(text, verbose=False)
    sys.stdout.write(output)
