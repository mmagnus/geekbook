"""geekbook - config file
"""
import os

LOCAL = True

PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

PATH_TO_MD = PATH + '/notes/'
PATH_TO_HTML = PATH + "/engine/data/html/"
PATH_TO_ORIG = PATH + "/engine/data/orig/"
PATH_TO_IMG = PATH + '/notes/'

TEMPLATE = 'default'

# to use it, create conf_local.py with e.g. TEMPLATE='pietro'
try:
    from conf_local import *
except:
    pass

# homepage
PATH_HOMEPAGE = PATH + "/themes/" + TEMPLATE + "/homepage/head_index.html"

# template
PATH_TO_TEMPLATE = PATH + "/themes/" + TEMPLATE + "/notes/" # don't forget about ending /
PATH_TO_TEMPLATE_HTML = PATH_TO_TEMPLATE + 'head.html'

PATH_TO_CSS = PATH_TO_TEMPLATE + "/css/"
PATH_TO_BASE_IMG = PATH_TO_TEMPLATE + "/img/"

try:
    from conf_local import *
except ImportError:
    pass
