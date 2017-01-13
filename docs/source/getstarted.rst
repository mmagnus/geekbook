Get Started
===========================================

**Run geekbookapp.py and edit your notes in ```<path to your geekbook>/notes/```**::

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

open your browser and copy-paste the ```html path``` (in my case is ```file:///private/tmp/geekbook/engine/data/html/index.html```).

To make a new note, create a file in ```<path to your geekbook>/notes/<notes here>```.

Remember to keep geekbookapp.py running all the time, it will detect a new note and compile it for you.

To force your browser to refresh html files whenevery there is a change on you drive (when geekbook compiles something new) please use something like this Auto-load (https://addons.mozilla.org/en-US/firefox/addon/auto-reload/?src=api) (this works for me in Firefox). 
