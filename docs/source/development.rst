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

Plugins
======================================

Insert Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: engine.plugins.insert_image
   :members:


Flask-based actions
======================================

Run the server::

    [mm] geekbook git:(master) ✗ python engine/webserverflask.py
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

and open in your browser http://127.0.0.1:5000/edit/test.md (you can add this to your notes
``<a href="http://127.0.0.1:5000/edit/test.md">edit</a>``.

To add new function, build on this simple example::

	@app.route('/edit/<note_title>')
	def edit(note_title):
		"""Open a note with your edit"""
		os.system('open ../notes/' + note_title)
		return 'edit note: %s' % note_title

.. automodule:: engine.webserverflask
   :members:

DataTables
======================================

Html code to be inserted dataTables [1] for index can be found in ``engine/make_index.py``.

[1] https://datatables.net/
