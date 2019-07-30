Markdown Tutorial for UberWriter
================================

I will try to give a short impressions on how I use markdown/pandocs capabilities to greatly reduce the time spent on formatting anything -- from websites to PDF Documents.

You can find a much more exhaustive documentation for all features pandoc offers on pandoc's help page: [Link](http://johnmacfarlane.net/pandoc/README.html#pandocs-markdown)

### Headers

There are two styles for headers. One looks like this:

# Header Level One
## Header Level Two
	        ...
###### Header Level Six

And another one, that has only »two« levels:

Header One
==========

Header Two
----------

You can use both styles, whichever you prefer. Additionally, pandoc requires you to have a blank line before a header.

### Paragraphs

A paragraph is one or more lines of text followed by one or more blank line. Newlines are treated as spaces. If you need a hard line break, put two or more spaces at the end of a line, or type a backslash at the end of a line.

### Block quotations

Block quotations in markdown use the same convention as in emails. A generic block quote looks like this: 

> This is a block quote. 
> This paragraph has two lines.
> 
> > And block quotes can be nested, as well.

Note the empty line you need to leave before the second level blockquote.

### Code blocks

There are two ways of creating a code block. You can indent your code four spaces or one tab.

	Code

Or use a fenced code block:

```javascript
a = function() {
	return 0;
}
```

Which works as well. You can identify the language of your code block to add syntax highlighting to the resulting document.

Short code examples can be surrounded by backticks to make them appear verbatim: `this.code() == true`.

### Lists

#### Bullet List:

* one
* two
* three

#### Nested Lists:

* fruits
	+ pears
	+ peaches
* vegetables
	+ broccoli
	+ ubuntu
		- mint
		- lubuntu
		- kubuntu

#### Numbered Lists:

1. Item 1
2. Item 2
3. Item 3

### Title blocks

To give your document some meta-information and a nice title, you can use title blocks at the top of your document: 

	% title
	% author(s) (separated by semicolons)
	% date

### Inline formatting

Emphasizing some text is done by surrounding it with *s:

This is *emphasized with asterisks*, and this will be a **bold text**. And even more ***krass***. And if you want to erase something: ~~completely gone~~ (surrounded by ~)

### Horizontal Rules

Horizontal rules are easily created by putting three or more `***` or `---` on a line:

*****


### Super- and subscripts

Superscripts may be written by surrounding the superscripted text by ^ characters; subscripts may be written by surrounding the subscripted text by ~ characters. Thus, for example,

H~2~O is a liquid.  2^10^ is 1024.

### Math

There are two ways to generate math type setting in pandoc: Inline math looks like this: 

This is inline $1 + 2 = 3$ math.

Note that there are no spaces allowed next to the dollar signs. 

And there is also another format: 

This is a beautiful equation: $$\left|\sum_{i=1}^n x_i \bar{y}_i\right|^2 \leq \sum_{j=1}^n |x_j|^2 \sum_{k=1}^n |y_k|^2$$ And it stands on it's own.

### Links

Enclosing an URL in pointy brackets transforms them into links:

<http://johnmacfarlane.net/pandoc>
<max@mustermann.de>

#### Inline Links: 

This is an [inline link](/url), and here's [one with
a title](http://fsf.org "click here for a good time!").

### Images

![This is the caption](/url/of/image.png)

### Footnotes

An example for footnotes (you can place the referenced footnote wherever you want, e.g. at the bottom of your document):

Here is a footnote reference,[^1] and another.[^longnote]

[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.
	Subsequent paragraphs are indented to show that they belong to the previous footnote.
	The whole paragraph can be indented, or just the first line.  In this way, multi-paragraph footnotes work like multi-paragraph list items.

There is also a different format for inline footnotes, that are easier to write:

Here is an inline note.^[Inlines notes are easier to write, since you don't have to pick an identifier and move down to type the note.]