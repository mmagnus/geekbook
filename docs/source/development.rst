Development
---------------------------------------------

Configuration
======================================

.. automodule:: engine.conf
   :members:

Geekbookapp
=============================================
.. automodule:: geekbookapp
   :members:

Page
=============================================

.. automodule:: engine.page
   :members:

Make Index
======================================
.. automodule:: engine.make_index
   :members:

Make Table of Contents
=======================================
.. automodule:: engine.make_tableofcontent
   :members:

Preprocessing
======================================
.. automodule:: engine.preprocessing
   :members:

Postprocessing
======================================
.. automodule:: engine.postprocessing      
   :members:


Flask-based action
======================================

**proof of concept**

Run the server::

    [mm] geekbook git:(master) ✗ python engine/webserverflask.py
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

 and open in your browser http://127.0.0.1:5000/edit/test.md

To add new function, build on this simple example::

	@app.route('/edit/<post_id>')
	def edit(post_id):
		# show the post with the given id, the id is an integer
		os.system('open ../notes/' + post_id )
		return 'edit %s' % post_id

