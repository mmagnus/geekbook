Features
==========================================

Markdown (Github-Flavored Markdown)
------------------------------------------

Write your notes using Github-Flavored Markdown! Markdown is a way to style text on the web. You control the display of the document; formatting words as bold or italic, adding images, and creating lists are just a few of the things we can do with Markdown. Mostly, Markdown is just regular text with a few non-alphabetic characters thrown in, like # or *. 

GitHub Flavored Markdown is a version of the Markdown syntax that provides an additional set of useful features, many of which make it easier to work with your notes.

- https://guides.github.com/features/mastering-markdown/
- https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

Syntax highlighting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Type::

    ``` js
    var foo = function (bar) {
      return bar++;
    };

    console.log(foo(5));
    ```

.. image:: ../imgs/syntax_hh.png

Geekbook extensions
------------------------------------------
This a set of extensions developed by the Geekbook community.

Table of Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Type ``[tableofcontent]`` to get the table of content of a given note.

Date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Type ``[date]`` to get the current date ```2017-01-13``.

Insert Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Type ``ii`` (and only this in a line) to ask geekbook to copy the last image from the folder when you keep you screenshots to
the folder with your images::

Before in your markdown file::

   ii

save the file, reload the file to get::

   ![](imgs/Screen_Shot_2017-01-14_at_1.25.21_PM.png)

To turn on this plugin in your ``engine.conf_local`` set the path, e.g. ::

   SCREENSHOT_INBOX='/home/magnus/Desktop/*png' 

Abstract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start a line with ``|`` to mark the fragemnt as an abstract.

.. image:: ../imgs/abstract.png

Youtube
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Type ```[yt:video id]```:

.. image:: ../imgs/youtube.png

Task status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Type ```@todo```, ```@done```, ```@progress``` to get:
  
.. image:: ../imgs/todo_done_progress.png
