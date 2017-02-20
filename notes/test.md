# What is Lorem Ipsum?

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer vehicula velit ut luctus ornare. Donec vel nisi tempor, posuere libero eu, consectetur dolor. Sed hendrerit mi in ex posuere, non venenatis est dignissim. Phasellus at nibh ac mi ullamcorper ultrices ut a velit. Aliquam ullamcorper vitae tortor non commodo. Morbi vitae auctor arcu. Integer in tempor tortor. Fusce fringilla molestie neque sagittis tincidunt. Donec bibendum condimentum egestas. Donec a lorem ultricies, sollicitudin ligula nec, ornare nibh. Nullam pretium ornare enim, nec volutpat nisl aliquet nec. Nullam efficitur semper mauris, eget egestas tortor varius vel. Aliquam et elit maximus, pellentesque ante et, ultrices est. Pellentesque at urna non massa porttitor ornare interdum sed elit. 

[tableofcontent]

[date]

source: https://markdown-it.github.io/

# h1 Heading
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading


# Features
## Horizontal Rules

___

---

***


## Typographic replacements

Enable typographer option to see result.

(c) (C) (r) (R) (tm) (TM) (p) (P) +-

test.. test... test..... test?..... test!....

!!!!!! ???? ,,  -- ---

"Smartypants, double quotes" and 'single quotes'


## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## Code

Inline `code`

Indented code

    python
	// Some comments
    line 1 of code
    line 2 of code
    line 3 of code


Block code "fences"

```
Sample text here...
```

or 

```
gCCCGgAUAgCUCAGuCGgAGAGCAuCAGACUuUUaAuCUGAGGguccAGGGuuCAaGUCCCUGUUCGGGCGCCA
(((((((..((((.....[.))))..(((.........)))......(((((..]....)))))))))))).... # pdbee default
(((((.(...(((.....[.)))...(((.........))).......((((..]....)))).).))))).... # mc-annotate
```

Syntax highlighting

```js
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```

```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```

```python
#!/usr/bin/env python3

import codecs
import sys
import argparse

def get_parser():
    """Get parser of arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    return parser

if __name__ == '__main__':
    parser = get_parser()
	args = parser.parse_args() 

```

## Tables

 Option | Description |
 ------ | ----------- |
 data   | path to data files to supply the data that will be passed into templates. 
 engine | engine to be used for processing templates. Handlebars is the default. 
 ext    | extension to be used for dest files. 

Right aligned columns

 Option | Description |
 ------:| -----------:|
 data   | path to data files to supply the data that will be passed into templates. |
 engine | engine to be used for processing templates. Handlebars is the default. |
 ext    | extension to be used for dest files. |

## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")

Autoconverted link https://github.com/nodeca/pica (enable linkify to see)

## Checklists

- [ ] test test test
- [X] go go go

## Images

Left|Right
----|-----
 ![Minion](https://octodex.github.com/images/minion.png) | ![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat") |

![Minion](https://octodex.github.com/images/minion.png)
![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")

Like links, Images also have a footnote style syntax

![Alt text][id]

With a reference later in the document defining the URL location:

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"

# Geekbook Only
## Locate

[ff:XQxIC1CrCP.gif]

## Youtube

[yt:ICDGkVbSWUo]

## Tags 

- [!danger] [*!danger][*danger!] - The text mean something dangerous to pay attention of [danger!]
- [!warning] [*!warning][*warning!] - The text mean that there is something important to consider [warning!]
- [!success] [*!success][*success!] The text mean something good , something achieved [success!]
- [!info] [*!info][*info!] General information, important piece of text [info!]

## Tags todo, done, progress
### task1 @todo
### task2 @done
### task2 @progress

test @todo small task
## Images - set size
(without the first ``\``)

``!\[Minion](https://octodex.github.com/images/minion.png =100x)``

![Minion](https://octodex.github.com/images/minion.png =100x)

``!\[Minion](https://octodex.github.com/images/minion.png =200x100)``

![Minion](https://octodex.github.com/images/minion.png =200x100)

``!\[Minion](https://octodex.github.com/images/minion.png =x150)``

![Minion](https://octodex.github.com/images/minion.png =x150)

and local images:

``!\[geekbook](imgs/geekbook.png =x50)``

![geekbook](imgs/geekbook.png =x50)

## RNA seq

```
gCCCGgAUAgCUCAGuCGgAGAGCAuCAGACUuUUaAuCUGAGGguccAGGGuuCAaGUCCCUGUUCGGGCGCCA
(((((((..((((.....[.))))..(((.........)))......(((((..]....)))))))))))).... # pdbee default
(((((.(...(((.....[.)))...(((.........))).......((((..]....)))).).))))).... # mc-annotate
```
