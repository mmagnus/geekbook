"""
EXPERIMENTAL

Track ~/geekbook/to-pdf.txt to see new files comming.
Many things hardcoded here, right now this is experimental.

"""

from engine.conf import PATH_TO_MD, PATH_TO_HTML, PATH_TO_ORIG, FIND_FILES_PLUGIN, ADD_EXTRA_SPACE_FOR_NOTES
import os

from icecream import ic
import sys
ic.configureOutput(outputFunction=lambda *a: print(*a, file=sys.stderr), includeContext=True)
ic.configureOutput(prefix='')


PATH_TO_PDF = '~/Dropbox/Apps/boox/geekbook/' # '~/Sync/geekbook/'
PATH_TO_PDF_WORK = '~/Dropbox/Apps/boox/geekbook-work/' # '~/Sync/geekbook/'

import subprocess
def exe(cmd):
    o = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = o.stdout.read().strip().decode()
    err = o.stderr.read().strip().decode()
    return out, err

def topdf(self, negative=True, pdf=True):
        if self.name in ['password', 'address', '_search_']: # 'workflow'
            return

        ic(self.name)

        if self.name.endswith('x'):
            # ok, detect the file with XXXx.md
            # print(self.name + ' xx processing')
            # what is this?
            fn = PATH_TO_MD + os.sep + 'topdf/' + self.fn
            # fn: '/Users/magnus/geekbook/notes//topdf/backup-time-machinex.md'#
            if os.path.exists(fn): # if the files in in topdf/ then its X cross file but it can
                # be a file with dropbox.md 
                with open(fn) as f:
                     md = f.read()
            else: # dropbox should be open here
                with open(PATH_TO_MD + os.sep + self.fn) as f:
                     md = f.read()
        else:    
            with open(PATH_TO_MD + os.sep + self.fn) as f:
                 md = f.read()
                 
        md = md.replace('.DARK.jpeg', '.LIGHT.jpeg')
        # md = md.replace('\n', '\n\n') # \n
        md = md.replace('{{TOC}}', '')

        # add a link for easy edits
        md = "<b>http://127.0.0.1:5000/view/" + self.name + ".html</b></br>\n\n\n\\pagebreak\n" + md  # fix? add space here
        
        # this does not work
        #md = "<a href='http://127.0.0.1:5000/view/" + self.name + ".html'>go to note</a>n" + md
        
        md = md.replace("\n![", "\n\n![") # ?

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
        imgs = re.findall('\!\[.*\]\(imgs/(.+)\)', md)
        # ic(imgs)
        for i in imgs:
            impath = PATH_TO_MD + '/imgs/' + i
            tpath = '/tmp/' + i
            tpath_neg = '/tmp/neg' + i            
                
            if negative:
                # check brightness
                # ic(impath)
                try:
                    image = cv2.imread(impath)
                    if isbright(image, thresh=0.5): # 0.39
                       tmpi = i
                       impath = PATH_TO_MD + '/imgs/' + i
                       cmd = "cp '%s' '/tmp/%s'" % (impath, i)#newpath) # fix for path with spaces
                       ic(cmd)
                       os.system(cmd)

                    else:
                        tmpi = 'neg' + i
                        # or https://note.nkmk.me/en/python-pillow-invert/
                        cmd = '/opt/homebrew/bin/convert %s -channel RGB -negate %s' % (impath, tpath_neg)#newpath)
                        # ic(cmd)
                        out, err = exe(cmd)
                        if err:
                            ic(err)
                        
                except:
                    tmpi = i

            if not negative:
               impath = PATH_TO_MD + '/imgs/' + i
               cmd = 'cp %s /tmp/%s' % (impath, i)#newpath)
               ic(cmd)
               os.system(cmd)
               tmpi = i

            #/tmp/qr.jpg
            #qi = i + ')![](/tmp/qr.jpg)' # here you get qr.jpg)) so you can fix it
            # with replace('qr.jpeg))', 'qr.jpeg)')
            #md = md.replace('(imgs/' + i, '(/tmp/' + qi)
            QR = False
            if QR:
                import qrcode
                from PIL import Image

                # open temp picture
                img_bg = Image.open(tpath)

                qr = qrcode.QRCode(box_size=img_bg.size[0] / 10) # vs 2 1/10?
                qr.add_data('http://18.193.7.215:8080/4j6scj6p82zw400/' + i)
                print('http://18.193.7.215:8080/4j6scj6p82zw400/' + i)
                qr.make()
                # original pictures should be send
                cmd = 'scp ' + PATH_TO_MD + '/imgs/' + i + ' aws:/home/ubuntu/rna-tools/rna_tools/tools/webserver-engine/qr/' + i
                # for test you can keep this off
                # os.system(cmd)
        
                img_qr = qr.make_image()
                #pos = (img_bg.size[0] - img_qr.size[0], img_bg.size[1] - img_qr.size[1])
                pos = (img_bg.size[0] + 100, img_bg.size[1] - img_qr.size[1])
                img_bg.paste(img_qr, pos)
                img_bg.save(tpath) #impath) #'data/dst/qr_lena.png')

            tmpi = '/tmp/' + tmpi
            if os.path.exists(tmpi):
                # fixed size
                full_size = False
                for l in md.split('\n'):
                    if i in l and '[#]' in l:
                        full_size = True

                if full_size:
                    md = md.replace('(imgs/' + i, '(' + tmpi + '')
                else:
                    md = md.replace('(imgs/' + i, '(' + tmpi + '')#{ height=400px }!!!!') # { height=350px }
            else:
                print('missing image %s ' % i)
                #md = md.replace('(imgs/' + i, '(' + tmpi + '){ height=400px }!!!!') # { height=350px }
 
        md = md.replace('!!!!)', '\n') # ugly
            
        md = md.replace('\n#', '\n\n#') # fix merging line with <text>#

        # actually this brings # as a caption and makes a figure smaller in latex
        # with just [] the figure is full size
        md = md.replace('![#](', '![](') 

        # maybe all \n change to more
        # this is a problem with pre !
        # md = md.replace('\n', '\n\n')
        
        #md = md.replace('(imgs/', '(' + PATH_TO_MD + '/imgs/')
        # \n to fix missing \n at the end and then # Notes merges with the last line
        print(md)

        nmd = ''
        for l in md.split('\n'):
            if l.startswith('//'):
                nmd += l.replace('//', '\n\pagebreak\n') + '\n'
            else:
                nmd += l + '\n'
        md = nmd

        md = md.replace('[notes]', '\pagebreak') #'>\n\n' * 15 + '\n XX' ) # add an empty page
        print(md)

        md += '\n\n\n ...\n\n' 
        md += '|\n\n' * 15 + '\n' # add an empty page

        md += '\pagebreak \n \pagebreak ...'

        tmp = '/tmp/' + self.name + '.md' # self name, so you dont have to wait for cmd to end
        #tmp = PATH_TO_MD + sep + '/tmp.md'
        with open(tmp, 'w') as f:
            f.write(md)
        # PATH_TO_MD + sep + self.fn
        # cd ' + PATH_TO_MD + ' &&
        #if not negative:
        #    output = '~/Sync/boox-geekbook-color/' + self.name + '-color.pdf '
        #else:
        if not pdf:
            PATH_TO_EBOOKS = '~/Dropbox/geekbook-ebooks/'
            output = PATH_TO_EBOOKS + self.name + '.epub' # tex#pdf '
        if pdf:
            # if self.name
            output = ''
            for i in ['mail', 'workflow', 'work', 'rnahub', 'openfold', 'rna-tools', 'elena-meeting',
                      'rna-annotation']:  # mail then overwrite by openfold
                if i in self.name:
                    try:
                        os.mkdir(PATH_TO_PDF_WORK + '/' + i )
                    except:
                        output = PATH_TO_PDF_WORK + '/' + i + '/' + self.name + '.pdf' # tex#pdf '
            if not output:
                output = PATH_TO_PDF + self.name + '.pdf' # tex#pdf '

        # no toc for snippets
        toc = ' --toc '
        if self.name == 'snippets':
            toc = ''

# cmd
        if pdf:
            cmd = 'pandoc ' + tmp + ' -o ' + output + toc + ' --metadata=title=' + self.name + '  -V mainfont="Helvetica" -f markdown+implicit_figures --pdf-engine=xelatex -V geometry:"top=3cm, bottom=3cm, left=3cm, right=3cm"'

        else:
            cmd = 'pandoc ' + tmp + ' -o ' + output + toc + ' --metadata=title=' + self.name + '  -V mainfont="Helvetica" -f markdown+implicit_figures --pdf-engine=xelatex -V geometry:"top=3cm, bottom=3cm, left=3cm, right=3cm"'

        # add & so it will not block !
        # -N -f gfm
        print(cmd)
        if True:
            out, err = exe(cmd)
            if err:
                ic(err)
        else:
            os.system(cmd)

if __name__ == '__main__':
    class Page:
        name = ''
    p = Page()
    p.name = 'workflow'
    p.fn = p.name + '.md'
    topdf(p)
    topdf(p, negative=False, pdf=False)    
