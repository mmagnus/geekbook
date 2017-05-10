import os

def hightlight_text_in_html(phrase, text):
    """
    Replace NO_PUBKEY with a highlighted text '<span style="background-color:yellow">NO_PUBKEY</span>'

    Normal phrase is used and .upper()
    """
    text = text.replace(phrase, '<span style="background-color:yellow">' + phrase + '</span>')
    text = text.replace(phrase.upper(), '<span style="background-color:yellow">' + phrase.upper() + '</span>')
    text = text.replace(phrase.title(), '<span style="background-color:yellow">' + phrase.title() + '</span>')
    return text

def lsdir(directory = '/home/magnus/Desktop/', exclude_files_starting_with_dot=True, verbose=False):
    """
    magnus@maximus:~/workspace/myutil$ python test.py
    /home/magnus/Desktop/bookmarks-2010-10-15-present-bookmarks-nice.json
    /home/magnus/Desktop/Untitled 2.odt
    /home/magnus/Desktop/logo.jpg

    GET:
    - directory e.g. /home/magnus/Desktop/

    DO:
    - walk and collect a list of all files -> f
    RETURN:
    - f = list of all files under given directory, [/home/magnus/Desktop/temp/beta.png, ... ,/home/magnus/Desktop/temp/temp~]

    http://snippets.dzone.com/posts/show/644

    """
    def walktree (top = ".", depthfirst = True):
        import stat
        names = os.listdir(top)
        if not depthfirst:
            yield top, names
        for name in names:
            try:
                st = os.lstat(os.path.join(top, name))
            except os.error:
                continue
            if stat.S_ISDIR(st.st_mode):
                for (newtop, children) in walktree (os.path.join(top, name), depthfirst):
                    yield newtop, children
        if depthfirst:
            yield top, names

    f = []
    for (basepath, children) in walktree(directory,False):
        for child in children:
            if exclude_files_starting_with_dot:
                if child.startswith('.'):
                    continue
                else:
                    if verbose:
                        print os.path.join(basepath, child)
                    f.append( os.path.join(basepath, child))
    return f

