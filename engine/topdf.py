from engine.conf import PATH_TO_MD, PATH_TO_HTML, PATH_TO_ORIG, FIND_FILES_PLUGIN, ADD_EXTRA_SPACE_FOR_NOTES
import os

from icecream import ic
import sys
ic.configureOutput(outputFunction=lambda *a: print(*a, file=sys.stderr))
ic.configureOutput(prefix='')

def topdf(self, negative=True):
        if self.name == '_search_':
            return
        with open(PATH_TO_MD + os.sep + self.fn) as f:
             md = f.read()
        md = md.replace('.DARK.jpeg', '.LIGHT.jpeg')
        # md = md.replace('\n', '\n\n') # \n
        md = md.replace('{{TOC}}', '')

        # add a link for easy edits
        md = "<b>http://127.0.0.1:5000/view/" + self.name + ".html</b>\n\n" + md
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
        print(imgs)
        for i in imgs:
            impath = PATH_TO_MD + '/imgs/' + i
            tpath = '/tmp/' + i
            # resize
            if 0:
                from PIL import Image
                # open temp picture
                img_bg = Image.open(impath)
                print(img_bg.size[0], img_bg.size[1])
                if img_bg.size[0] > 1000:
                    # cmd = '/opt/homebrew/bin/convert %s -resize 1200x400\> %s' % (impath, tpath)#newpath)
                    cmd = '/opt/homebrew/bin/convert %s -resize 50%% %s' % (impath, tpath)#newpath)
                    print(cmd)
                    os.system(cmd)

                print('(/tmp/' + i)
                #md = md.replace('(imgs/' + i, '(/tmp/' + i)
                impath = tpath # !
                
            if negative:
                # check brightness
                image = cv2.imread(impath)
                if isbright(image, thresh=0.39):
                    pass
                else:
                    newpath = i
                    cmd = '/opt/homebrew/bin/convert %s -channel RGB -negate /tmp/%s' % (impath, i)#newpath)
                    os.system(cmd)
            else:
               impath = PATH_TO_MD + '/imgs/' + i
               cmd = 'cp %s /tmp/%s' % (impath, i)#newpath)
               os.system(cmd)

            print('(/tmp/' + i)
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
                
            md = md.replace('(imgs/' + i, '(/tmp/' + i + '){ height=400px }!!!!') # { height=350px }
        md = md.replace('!!!!)', '\n') # ugly
            
        md = md.replace('(imgs/', '(' + PATH_TO_MD + '/imgs/')

        md += '\n# Notes\n\n'
        md += '|\n\n' * 15 + '\n' # add an empty page
        tmp = '/tmp/print.md'
        #tmp = PATH_TO_MD + sep + '/tmp.md'
        with open(tmp, 'w') as f:
            f.write(md)
        # PATH_TO_MD + sep + self.fn
        # cd ' + PATH_TO_MD + ' &&
        if not negative:
            output = '~/Dropbox/boox-geekbook-color/' + self.name + '-color.pdf '
        else:
            output = '~/Dropbox/boox/geekbook/' + self.name + '.pdf '

        # no toc for snippets
        toc = ' --toc '
        if self.name == 'snippets':
            toc = ''
        cmd = 'pandoc ' + tmp + ' -o ' + output + toc + ' --metadata=title=' + self.name + '  -V mainfont="Helvetica" --pdf-engine=xelatex -V geometry:"top=3cm, bottom=3cm, left=3cm, right=3cm" &' # -N -f gfm 
        print(cmd)
        if 0:  # for testing keep this
            import subprocess
            def exe(cmd):
                o = subprocess.Popen(
                    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out = o.stdout.read().strip().decode()
                err = o.stderr.read().strip().decode()
                return out, err
            exe(cmd)
        os.system(cmd)
