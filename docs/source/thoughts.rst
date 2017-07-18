Food for thoughts
=================================================================

Simple plain text writing
-----------------------------------------------------------------

*It's easy to obsess more about your writing setup than your actual writing, but when inspiration strikes and you actually want to—you know—write something, nothing should stand between you and putting your thoughts on paper, digital or otherwise. Distraction-free writing environments are all the rage, but here's the thing: You can set up a writing environment so free from distractions it's the writing equivalent of a sensory deprivation tank, but if all that fiddling places any barrier between you and your goal—to actually write—it's not worth it.*

http://lifehacker.com/5684804/set-up-a-writing-system-that-stays-out-of-your-way

What Is Markdown, and Why Is It Better for My To-Do Lists and Notes?
-----------------------------------------------------------------

*Markdown uses a very simple formatting syntax to accomplish the same thing that HTML or Rich Text Formatting does. The difference is that it's simpler than HTML and you don't have to worry about opening and closing tags. It also doesn't have all of the menus associated with most text editing programs. To format text, Markdown uses punctuation and characters you're already familiar with.*

http://lifehacker.com/5943320/what-is-markdown-and-why-is-it-better-for-my-to-do-lists-and-notes

Long notes vs short notes
-----------------------------------------------------------------
It seems that if it make sense try to make long notes. One project should be a long note. You have everything in one place, and you can just scroll up or down and use the table of content sidebar to get where you want, it's a really time saver! Not having to click and go to a different note, it's really fun and help you focus on your work. That's why Word doc files don't work for me, it's to hard to find yourself easily and for very big files, Word is just super slow!

However, if you have a note that is clearly self-containing, separate from everything else, use a new note. It will be faster to read or/and edit on mobile devices, easier to print.

Git/Github your notes
-----------------------------------------------------------------
We develop a plugin to automatically git your notes. The script can be added to your crontab. 

``geekbook/plugins/ContentAutoCommit/git-auto-commit.sh``

Magnus: I realized that I prefer to commit changes of my notes by myself. I usually improve some new information, fix some notes etc. So I developed the script but I'm not really using it right now.

.. image:: ../imgs/gitgui-notes.png

Images (external)
-----------------------------------------------------------------
It's also very useful in some applications to have images seperate than your notes. You can have dynamics notes, where your images are in varous places and you provide in Markdown links to them. You can also grab any image to Gimp, edit it and just save. The image in the note will be updated then. You can edit images in batch.

Styles
-----------------------------------------------------------------
Geekbook compared to Word is very easy to stylish however you want :-) It's just HTML. You can do whatevery you want using CSS etc.

Version control of your notes
-----------------------------------------------------------------
If you use git, you can keep all version of your notes, you can track the whole history, in the similar way how you can deal with your code.

Super-flexible
-----------------------------------------------------------------
This system is super flexible. You can use whatever editor you like, you can edit your notes on your phone, one a cluster using Vi/Nano/etc. It's text file so you will be able to open it alwasy in the future.

Cool alternatives
-----------------------------------------------------------------

- Geeknote http://www.geeknote.me/ - Work with Evernote from command line
- KeepNote http://keepnote.org/manual/#philosophy
- Notes https://github.com/pimterry/notes
