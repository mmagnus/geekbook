#!/usr/bin/env python

"""Search for [ff:..]  with (g)locate make a link.

To remove the db, you can simply run ``rm geekbook/engine/plugins/find_file.json``"""

import sys
import re
import platform
import os
import pandas as pd
import commands

import logging
logger = logging.getLogger('geekbook')

JSON_DB = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'find_file.json'

def file_search(filename, verbose):
    """Search for filename. Returns dirname of the filename's path, and the full path.
    
    170107 add cache. If the db is not found, create an empty pandas df 
    and populate this df with append later. If the filename is not in the db
    run g/locate. Then, save the found path to the db (using pandas, via df, to json)"""

    # cache
    if os.path.isfile(JSON_DB):
        df = pd.read_json(JSON_DB, orient='records')
        #filename = 'x.pse'
        pathdf = df[df['fn'] == filename]['path']
        if not pathdf.empty:
            path = pathdf.to_string(index=False)
            logger.info('find file [from the db]:' + filename)
            return os.path.dirname(path), path
    else:
        df = pd.DataFrame()

    # if filename is not found in the db
    logger.info('find file:' + filename)

    if platform.system() == "Linux":
        out = commands.getoutput('locate ' + filename)
    if platform.system() == "Darwin":
        out = commands.getoutput('glocate ' + filename)
    first_hit = out.split('\n')[0]
    logger.info('# of hits ' + str(len(out.split('\n'))) + " " + out.replace('\n',', '))
    if not first_hit:
        logger.info('not found')
    else:
        logger.info('hit ' + first_hit)

    # update cache
    dffile = pd.DataFrame([[filename, first_hit],], columns=['fn', 'path'])
    df = df.append(dffile, ignore_index=True)
    # save to json
    df.to_json(JSON_DB, orient='records')
    ##
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
            else:
                if verbose: print 'problem: can not find ' + filename
                output += l.replace('[ff:' + filename + ']', '<span style="color:red">' + filename + '</span>')
                msg_listofnotfoundfiles += filename + '\n'
        else:
            output += l + '\n'
    ##
    output = output.replace('[files-not-found]', msg_listofnotfoundfiles)
    return output

if __name__ == '__main__':
    #text = sys.stdin.read()
    text = """
    [ff:XQxIC1CrCP.gif]
    """
    output = find_files(text, verbose=False)
    sys.stdout.write(output)
