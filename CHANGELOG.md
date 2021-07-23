# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.3 dark mode with printing mode

Darkmode [2021-04-19-2021-07-23]

- style: up
- process images macros smaller & light/dark & dark/light for images
- Set light theme for code
- Add printing mode (required after dark mode)
- [prototype] init of darkmode

Add:

- 2021-02-23 Add ADD_EXTRA_SPACE_FOR_NOTES for printed notes for extra space for pdfs for Boox
- 2021-02-22 TOC now handles h4 and h5 level headers
- 2021-02-14 insert_image.py: handle file://localhost/localhost/private
- 2021-02-11/23 Add to engine/process_md.py: ways to do quick actions with  from the editor via `![#rm]()`
             - #rm 
			 - #open
			 - #fork
			 - #min
- 2021-02-08 page: export file (with images) with --add-toc --push --readme

Change:

- 2021-02-11 engine/plugins/insert_image.py: works also on /<path to img.png>

Fix:

- 2021-01-26 insert_image.py: fix pngfiles:///
- 2021-01-26 insert_image.py: fix getting dates, a new function with ifs, add #
- 2021-01-05 fix: dont crash when there is space in name (but files are simply skipped)

## 3.0 Python3 version 
190824

## 2.2 Last Python2 version!
- Introduce ``#short`` to make it shorter 190719
## 2.1
### Added
- Insert files (drag and drop) from Apple Photos
- A draft of slides <https://mmagnus.github.io/geekbook/#/>

### Changed
- Round corners of images
- Fix testing with Travis
- Search file when clicked on a page

### Hacks

- Use html comments to hide some sections
- You can use also inframes
- Dates to headers, otherwise, even with blame, is hard to quickly get info when the entry was entered the system
- Use more [ff:xx]
- Use more short notes, integrate them into meta notes
- Use # for hashtags
- Use [open:xx] in Emacs Markdown to go to a folder or a file
- Use [if:xx] to import a file and it can also used for folders (!)

## 2.0
The system re-written based on Flask.
