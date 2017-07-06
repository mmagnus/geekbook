#!/usr/bin/env python3
"""Push a geekbook note to VM as readme and commit.
TODO:

- sync images

if now change:

    [mm] geekbook$ git:(master) ✗ ./gk-sync.py
    npdock-readme.md.tosync                                                                                            100% 4819     1.4MB/s   00:00
    On branch master
    Your branch is up-to-date with 'origin/master'.
    Changes not staged for commit:
        modified:   db.sqlite3

    Untracked files:
        .tramp_history

    no changes added to commit

#echo 'rpdock-vm:/home/rpdock/web/README.md'
#scp notes/npdock-readme.md rpdock-vm:/home/rpdock/web/README.md

required https://github.com/ekalinin/github-markdown-toc.go
"""


import subprocess
import argparse
import os

def get_toc(f):
        cmd = "gh-md-toc " + f
        o = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = o.stdout.read().strip()
        err = o.stderr.read().strip()
        return out.decode('utf-8')

def get_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file', help='file')
    return parser
    
def get_file():
    fn = 'notes/npdock-readme.md'
    toc = get_toc(fn)

    txt = open(fn).read()
    txt = txt.replace('[tableofcontent]', toc)

    f = open(os.path.basename(fn) + '.tosync','w')
    f.write(txt)
    f.close()
    print(txt)
    
if __name__ == '__main__':
    #parser = get_parser()
    #args = parser.parse_args()
    #fn = args.file

    get_file()
    os.system('scp npdock-readme.md.tosync rpdock-vm:/home/rpdock/web/README.md')
    os.system('ssh rpdock-vm "cd /home/rpdock/web/ && git add README.md && git commit -m \'readme update\' && git push"')
