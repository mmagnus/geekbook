Get Started
===========================================

Run geekbookapp.py::

  [mm] geekbook git:(master) ./geekbookapp.py
  2017-01-10 09:47:46: (network.c.410) can't bind to port:  1234 Address already in use
  Could not execute http daemon lighttpd -f.
  The file /private/tmp/geekbook/engine/data/html/index.html does not exist.

  ________               __   __________               __
  /  _____/  ____   ____ |  | _\______   \ ____   ____ |  | __
  /   \  ____/ __ \_/ __ \|  |/ /|    |  _//  _ \ /  _ \|  |/ /
  \    \_\  \  ___/\  ___/|    < |    |   (  <_> |  <_> )    <
  \______  /\___  >\___  >__|_ \|______  /\____/ \____/|__|_ \
  \/     \/     \/     \/       \/                   \/

  2017-01-10 09:47:46,585 - geekbookapp.py - G33kB00k is Running... [ok]
  2017-01-10 09:47:46,585 - geekbookapp.py - root path: /private/tmp
  2017-01-10 09:47:46,585 - geekbookapp.py - html path: <file:///private/tmp/geekbook/engine/data/html/index.html>
  2017-01-10 09:47:46,585 - geekbookapp.py - imgs path: /private/tmp/geekbook/notes/

  2017-01-10 09:47:46,586 - page.py - IOError: test.md
  2017-01-10 09:47:46,587 - page.py - compiling --> test.md
  2017-01-10 09:47:46,589 - postprocessing.py - youtube video detected: ICDGkVbSWUo

the web browser of choice should open with the index page. You should see the test note.

You're ready to edit your notes. 

Edit your notes in ```<path to your geekbook>/notes/<note>.md```.

Keep the geekbookapp.py program running in the background. Whenever you edit an old note or add a new one geekbookapp.py will compile it not into a web page. Refresh the web page and you will see your note in the index or the note will be compiled on the note page.

Enjoy!
