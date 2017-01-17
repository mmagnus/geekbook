Geekbook

==============================================================
.. argparse::
   :ref: geekbookapp.get_parser
   :prog:  geekbookapp.py

Local configuration of your own Geekbook
---------------------------------------------

To set up your own variables that can be used by Geekbook you can edit the sample in ``engine/`` folder ``conf_local.py_sample``. Copy  	``conf_local.py_sample`` to ``conf_local.py`` and comment (or remove) variables that you don't want to change from default. The default variables are define in ``conf.py``).

For example, to define your own source of screenshots, make a config file like this::

   engine$ cat config_local.py
   SCREENSHOT_INBOX='/home/Thomas/Desktop/*png'

and restart ``geekbookapp.py``.
