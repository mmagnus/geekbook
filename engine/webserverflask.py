import os

from flask import Flask
app = Flask(__name__)

@app.route('/edit/<post_id>')
def edit(post_id):
    # show the post with the given id, the id is an integer
    os.system('open ../notes/' + post_id )
    return 'edit %s' % post_id

if __name__ == "__main__":
    app.run()
