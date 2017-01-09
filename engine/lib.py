from engine.conf import PATH_TO_IMG
import re


def get_image_path(l):
    """Get image path for l(ine).

    :rtype: string, line
    """
    rx = re.compile('\!\[\]\((?P<filename>.+)\)').search(l)

    if rx:
        path_new = '<a class="lightbox" href="' + PATH_TO_IMG + '/' + rx.group('filename') +'">'+\
                   '<img src="' + PATH_TO_IMG + '/' + rx.group('filename') + \
                   '" alt="" title=""></a> \n'
        return path_new
    else:
        return l
