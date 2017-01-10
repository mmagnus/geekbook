import os

from flask import Flask
app = Flask(__name__)

@app.route('/edit/<note_title>')
def edit(note_title):
    """Open a note with your edit"""
    os.system('open ../notes/' + note_title)
    return 'edit note: %s' % note_title

if __name__ == "__main__":
    app.run()
