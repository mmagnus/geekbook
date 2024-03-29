"""geekbook - config file"""
import os
import logging

LOCAL = True

PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

PATH_TO_MD = PATH + '/notes/'
PATH_TO_HTML = PATH + "/engine/data/html/"
PATH_TO_ORIG = PATH + "/engine/data/orig/"

IMG_PREFIX = 'imgs/'  # keep / at the end  # ![](imgs/<file> this 'imgs' is IMG_PREFIX
PATH_TO_IMG = PATH + '/notes/'
USE_RM_TO_REMOVE_FIGURE = False
ADD_EXTRA_SPACE_FOR_NOTES = False

TEMPLATE = 'default'

AI_WRITER = False

SCREENSHOT_INBOX = None
SCREENSHOT_INBOX2 = None
SCREENSHOT_INBOX3 = None
INSERT_IMAGE_TAG = '' # 'ii'
INSERT_IMAGE_TAG2 = '' # 'id'
INSERT_IMAGE_TAG3 = '' # 'id'
INSERT_IMAGE_TAG_SUFFIX = ''
INSERT_IMAGE_TAG2_SUFFIX = ''
INSERT_IMAGE_TAG3_SUFFIX = ''
INSERT_IMAGE_HASHTAG = ''
INSERT_IMAGE_HASHTAG2 = ''
INSERT_IMAGE_HASHTAG3 = ''
# find files plugin off/on
FIND_FILES_PLUGIN = True

logging.basicConfig(format='%(asctime)s - %(filename)s - %(message)s')
logger = logging.getLogger('geekbook')
logger.setLevel('INFO')

# to use it, create conf_local.py with e.g. TEMPLATE='pietro'
## try:
##     from geekbook.engine.conf_local import *
## except:
##     logger.info('Config local [not found], use default settings [ok]')
user_path = os.path.expanduser("~") + '/.geekbook.py'
try:
    exec(open(user_path).read())  # python3
    logger.info('Config local loaded ' + user_path)    
except FileNotFoundError:# noooot perfect! 
    logger.info('Config local [not found], use default settings [ok] ' + user_path)

# homepage
PATH_HOMEPAGE = PATH + "/themes/" + TEMPLATE + "/homepage/head_index.html"

# template
PATH_TO_TEMPLATE = PATH + "/themes/" + TEMPLATE + "/notes/"  # don't forget about ending /
PATH_TO_TEMPLATE_HTML = PATH_TO_TEMPLATE + 'head.html'

PATH_TO_CSS = PATH_TO_TEMPLATE + "/css/"
PATH_TO_BASE_IMG = PATH_TO_TEMPLATE + "/img/"

