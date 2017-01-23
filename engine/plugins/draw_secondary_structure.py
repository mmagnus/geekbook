from engine.conf import PATH_TO_MD, SCREENSHOT_INBOX, PATH_TO_IMG, IMG_PREFIX
import os
import logging
logger = logging.getLogger('geekbook')

def get_ss(text):
    """Draw secondary structure using VARNA.

    .. warning :: to each image `ss_` is added at the beginning of the image file

    1. if the line after </pre> has ![ it means that there is an image already, don't generate new one. 
    And of course, it means if you remove this line, the image will be regenerated.

    2. if [!danger] also skip generation images.

    Should I overwrite a file ? By default no! Use [ss:file:t] # to set overwrite to true """
    try:
        from rna_pdb_tools import SecondaryStructure
    except ImportError:
        logger.info('import error rna_pdb_tools')
        return text, False

    changed = False
    ltext = text.split('\n')
    for c in range(0, len(ltext)):
        if ltext[c].startswith('<pre>[ss'):
            if ltext[c+4].startswith('!['): # ^1
                continue
            if ltext[c+4].startswith('[!danger]'): # ^2
                continue

            args = ltext[c].replace(']','').replace('[','').strip().split(':')
            overwrite = False # default
            if len(args) == 2:
                foo, name = args
            if len(args) == 3:
                foo, name, tf = args
                if tf.lower().strip() == 't':
                    overwrite = True

            title = name
            name = 'ss_' + name + '.png'
            seq = ltext[c+1]
            ss = ltext[c+2]

            # make folder with imgs
            try:
                os.mkdir(PATH_TO_IMG + os.sep + 'imgs')
            except OSError:
                pass

            #print seq, ss, name
            out = PATH_TO_IMG + os.sep + 'imgs' + os.sep + name
            # check not to owerwrite the img file
            isfile = os.path.isfile(out)
            changed = True
            if isfile and not overwrite:
                err = 'imgs is already thare, change a name or force to overwrite [ss:/file/:t]'
                logger.info(err)
                ltext[c+4] = '[!danger]' + err + '[danger!]'
                return '\n'.join(ltext), changed

            # draw & error handling
            stderr = SecondaryStructure.draw_ss(title,seq,ss,out)
            if stderr:
                ltext[c+4] = '[!danger] VARNA Error: ' + stderr.replace('\n',' ') + ' [danger!]'
                logger.info(stderr)
            else:
                ltext[c+4] = '![](imgs/' + name + ')' + '\n'
    return '\n'.join(ltext), changed

