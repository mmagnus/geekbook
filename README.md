# geekbook3 - note taking system for nerds!
Marcin Magnus (mmagnus) & Pietro Boccaletto (akaped)

[![Twitter Follow](http://img.shields.io/twitter/follow/geekbookx.svg?style=social&label=Follow)](https://twitter.com/geekbookx)
[![tag](https://img.shields.io/github/release/mmagnus/geekbook.svg)](https://github.com/mmagnus/geekbook/releases)
[![Build Status](https://travis-ci.org/mmagnus/geekbook.svg?branch=master)](https://travis-ci.org/mmagnus/geekbook)
[![Documentation Status](https://readthedocs.org/projects/geekbook/badge/?version=latest)](http://geekbook.readthedocs.io/en/latest/?badge=latest)
![http://www.gnu.org/licenses/gpl-3.0.html](http://img.shields.io/:license-gpl3-blue.svg)
<span class="badge-paypal"><a href="https://www.paypal.me/MarcinMagnus" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-yellow.svg" alt="PayPal donate button" /></a></span> 
<span class="badge-flattr"><a href="https://flattr.com/profile/mmagnus" title="Donate to this project using Flattr"><img src="https://img.shields.io/badge/flattr-donate-yellow.svg" alt="Flattr donate button" /></a></span>
</p>

<i>Motto: **Notes are like your code**.</i>

(geekbook3 since finally Geekbook uses Python 3)

G33KB00K3 - fun to read & fun to write -- 🤓 eXtreme eXtendable note taking system for nerds/geeks (including scientists!) (= beautiful html generator of your markdown-based notes)  docs: http://geekbook.rtfd.io

**THE LATEST**

[Geekbook Bookify]( https://github.com/mmagnus/geekbook/tree/master/plugins/bookify) - a plugin to process your notes into e-books

**MOTIVATION**

I started using MoinMoin for my personal notes in 2008, but something was missing... I started then playing with simple notes in Markdown written in my Emacs. The next step was to write a system to convert this notes into HTML. The system was drafted in Gdańsk, at the PTBI conference (2012) when I decided to write a tool to process a folder with notes written in Markdown. I wanted to use my CSS style and then more, and more some unique features that I found very useful for myself. I think, at the moment, the project converged pretty much to tools like http://jekyllrb.com and https://www.mkdocs.org.


![](themes/default/qubCXZcWHl.gif)
Figure. From an (old) homepage to a note.

![](docs/imgs/56HcDqXllz.gif)
Figure. A new Homepage.

A neat way how to combine **Emacs/Atom/Sublime/iA Writer editor + Markdown Syntax + Git + Html engine** (bootstrap/python) to get the best notes-talking experience ever. Highly customizable with plugins written in Python. What's the most important, under the hood it's just a set of Markdown files.. you can do with them whatever you want, e.g. you can Pandoc (http://pandoc.org/epub.html) them to epub (that's origin of "book" part of the name).

  * [Features](#features)
    * [Index](#index)
    * [Dashboard](#dashboard)
    * [Extensions](#extensions)
  * [EMACS\-powered](#emacs-powered)
    * [focus\-mode](#focus-mode)
    * [list notes in Emacs (sort by Date/Name)](#list-notes-in-emacs-sort-by-datename)
    * [magit\-based diff of your notes](#magit-based-diff-of-your-notes)
  * [On your OSX](#on-your-osx)
  * [On your phone](#on-your-phone)
  * [Install & Get Started!](#install)
  * [Food for thought](#food-for-thought)

Features | Geekbook | Word Office | Apple Notes
-------- | -------- | ----------- | -----------
**Edits with Emacs** | Oh, boy, yes! | Nope | Nope
**Outline (collapse to headers)** | With Emacs yes. Works great! | Nope | Nope
**Long notes - easier to browse** | Long notes with great speed and table of content | Very slow for long notes. Always problems with formatting long notes with images. | Very good for short notes.
**Syntax highlighting** | Oh, boy, yes! | Hmm.. nope | Hmm.. nope
**Write your own plugins in Python** | Oh, boy, yes! | Nope | Nope
**Export as a pdf** | Yes | Yes | Yes
**Edit with ...** | Any text editor (with Markdown support for better UX) | Word | Apple Notes (Closed)
**Flexible** | Super flexible. You can find your own why how to make your notes | Medium | Medium
**Search** | Super easy to search with built-in search or just grep your files | More difficult to search over a set of files. Slow! | OK
**Version control** | Yes, if you use Git etc | Kind of. Hard to use (compared to Git) | Nope
**Style customizable** | Yes, it's HTML. Do what ever you want | To some extend | Nope
**Edit on your phone** | Yes, use Byword | Not really | Yes, works very well!
**Open & Free** | YES | Nope, closed and pricey | Close, no extra charge if you have an Apple device
**Super easy to use** | Rather for geek/nerds/hackers | Easy but who cares ;-) | Easy but who cares ;-)

@todo Compare to Evernote.

Similar projects: it's kind of like Sphinx for your documentation, or Mkdocs (http://www.mkdocs.org/).

Freatures:

- Index html based
- Sync them with Dropbox/iCloud/github
- Read from console, grep them
- Edit with almost any text editor, I'm using Emacs!
- Keep images separately, edit them in any external tool or edit them in batch
- Customize html templates
- You can sync notes in your system with notes kept at virtual machines (mounted via sshfs) or drives
- Super light!
- Pandoc markdown files to anything you want!
- Use 3rd party editors, if you wish, on your computer or on your phone.

I recommend to use **Emacs** (or VIM or other super-powerful editor) to:

- run git on your notes in your editor,
- grep them in the editor,
- make bookmarks to parts of your notes,
- copy-paste from your notes to your programs you're writing,
- use Google Translate (https://github.com/atykhonov/google-translate)
- ispell,
- outline mode,
- focuse mode.

Sync with **Github** to have your notes (full-text searchable) with you all the time (in a private repository):

![index](docs/imgs/geekbookx.png)

Kinda similar projects:

- www.geeknote.me

# Features
## Index

![index](docs/imgs/index.png)

## Dashboard

![dashboard](docs/imgs/dashboard.png)

## Extensions
Geekbook includes also many plugins that build on top of Markdow to give even more fun.

See for more <http://geekbook.readthedocs.io/en/latest/edit.html#geekbook-only> and <https://geekbook.readthedocs.io/en/latest/quickref.html>

# Emacs powered
## Focus on your notes

![](docs/imgs/emacs_focus_mode.png)

## List your notes in Emacs (sort by Date/Name)

![](docs/imgs/emacs_list.png)

## magit-based diff of your notes

![](docs/imgs/emacs_git.png)

[https://www.emacswiki.org/emacs/Magit](https://www.emacswiki.org/emacs/Magit)

# Python-markdown powered
## Footnotes
- https://python-markdown.github.io/extensions/footnotes/
# On your OSX

Spotlight your notes:

![](docs/imgs/osx_file.png)

# On your phone
On your phone: (in this case using Dropbox & Byword on my iPhone).

![](docs/imgs/notes_at_phone.png)

Or Draft (http://lifehacker.com/draft-is-a-clean-note-taking-app-with-markdown-support-844836670) for Android (not tested by me).

![](docs/imgs/iphone_search_byword.png)

Search on your Iphone to get to the note.

Update: Now I'm using iA Writer for iPhone (https://itunes.apple.com/pl/app/ia-writer/id775737590?l=pl&mt=12). It has sync with iCloud (works with sync also images (!)) and Dropbox. Geekbook has a nice plugin to be able to work with iA Writer seamlessly. 

![](docs/imgs/ia_writer_iphone.PNG)

If you insert an image on your phone, the syntax for it will be iA Writer-like. However if Geekbook detects this syntax it converts it to markdown syntax for images (which works as well in iA Writer). 

![](docs/imgs/screen800x500-0.jpeg)

Moreover, you can use in Geekbook also syntax `/<file.md>` to join chapters into books. 

![](docs/imgs/screen800x500-1.jpeg)

There is also a nice app for Mac (https://ia.net/writer/).

# Install

See http://geekbook.readthedocs.io/en/latest/install.html

# Food for thought
 
 http://geekbook.readthedocs.io/en/latest/thoughts.html
 
 # Markdown Editors

PyCharm - Python IDE and Markdown editor https://www.jetbrains.com/pycharm/

Linux:

- http://www.omgubuntu.co.uk/2017/11/notes-up-markdown-editor-for-linux 
- https://remarkableapp.github.io/

macOS:

- Bear http://www.bear-writer.com/
- iA Writer https://ia.net/writer/

iOS:

- https://ia.net/writer/
