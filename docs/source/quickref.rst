Quick Reference
=================================================================

::

     find a full path to your file and insert it in the given place in a generated html
     [ff:<file>]
     [ff:uniq-name.pse]

     insert an external file
     [if:<file>]
     [if:/Users/magnus/work-src/fenzymes/examples/readme.txt]

     insert the table of content in here
     [tableofcontent] or {{TOC}}

     to get the current date 2017-01-13
     [date]

     define only width for a image:
     ![](imgs/Screen_Shot_2017-02-12_at_1.17.04_AM.png =500x)

     only height:
     ![](imgs/Screen_Shot_2017-02-12_at_1.17.04_AM.png =x400)

     and both:
     ![](imgs/Screen_Shot_2017-02-12_at_1.17.04_AM.png =400x400)

     you can put to images next to each other and sqeeze them to the left
     <div style="width:300px">
     ![](imgs/190409_L4yjm119T5aONVO9BVeCTQ_thumb_7a17.jpg)![](imgs/190409_thumb_7a18.jpg)
     </div>

     #short - set for image (``max-height:400px``) to make it shorter

     [tableofcontent] or {{TOC}}
        insert the table of content in here


     add description of a note in the Index page
     [desc:info on TN]

     insert a file and remove the first line and shift all headers by one to fit the structure of the file where you import to
     /[file:hacking-convert-pdf-to-images.md =del1 =shift1]
     
     recompile master note with a give note when the note is changed
     ^[file:master-notes-for-this-one.md]

     \ii - copy an image file from Desktop to Geekbook and insert a link in a Markdown file
     \ip - copy a clipboard an image file and insert a link in a Markdown file
     \id - copy an image file from Dropbox to Geekbook and insert a link in a Markdown file
