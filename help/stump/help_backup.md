% UberWriter & Pandoc User Guide
% John MacFarlane, Wolf Vollprecht
% 01.08.2012

## UberWriter's goals

UberWriter aims to make the writing process very easy and beautiful. The editor offers inline highlighting for a specific subset of markdown, which is used to do the formatting of your text.

A short explanation of the core markdown features you'll find below. Pandoc is used to generate PDF, HTML or RTF files from markdown. Please note that Pandoc's syntax offers many, many more features which are well documented on the (pandoc homepage)[http://johnmacfarlane.net/pandoc/README.html].  
However, please note that not all of the advanced features play well with inline highlighting of UberWriter.

But for a quick start, this will be sufficient.

## Pandoc's markdown 

Pandoc understands an extended and slightly revised version of
John Gruber's [markdown] syntax. This document explains the syntax, noting differences from standard markdown. 

### Philosophy 

Markdown is designed to be easy to write, and, even more importantly, easy to read:

> A Markdown-formatted document should be publishable as-is, as plain text, without looking like it's been marked up with tags or formatting instructions. 
> -- [John Gruber](http://daringfireball.net/projects/markdown/syntax#philosophy)

This principle has guided pandoc's decisions in finding syntax for
tables, footnotes, and other extensions.

### Paragraphs

A paragraph is one or more lines of text followed by one or more blank line. Newlines are treated as spaces, so you can reflow your paragraphs as you like. If you need a hard line break, put two or more spaces at the end of a line.

A backslash followed by a newline is also a hard line break.

### Headers

An header consists of one to six `#` signs and a line of text, optionally followed by any number of `#` signs. 
The number of `#` signs at the beginning of the line is the header level:

    ## A level-two header

    ### A level-three header ###

As with setext-style headers, the header text can contain formatting:

    # A level-one header with a [link](/url) and *emphasis*

Standard markdown syntax does not require a blank line before a header. Pandoc does require this (except, of course, at the beginning of the document).

### Inline formatting

To *emphasize* some text, surround it with `*`s or `_`, like this:

    This text is _emphasized with underscores_, and this
    is *emphasized with asterisks*.

Double `*` or `_` produces **strong emphasis**:

    This is **strong emphasis** and __with underscores__.

A `*` or `_` character surrounded by spaces, or backslash-escaped,
will not trigger emphasis:

    This is * not emphasized *, and \*neither is this\*.

Because `_` is sometimes used inside words and identifiers, pandoc does not interpret a `_` surrounded by alphanumeric characters as an emphasis marker.  If you want to emphasize just part of a word, use `*`:

    feas*ible*, not feas*able*.

### Strikethrough

To strikethrough a section of text with a horizontal line, begin and end it with `~~`. Thus, for example,

    This ~~is deleted text.~~

### Block quotations

Markdown uses email conventions for quoting blocks of text.
A block quotation is one or more paragraphs or other block elements (such as lists or headers), with each line preceded by a `>` character and a space. 

> This is a block quote. This paragraph does indeed have more than one line.
> 
> 1. This is a list inside a block quote.
> 2. Second item. 

Among the block elements that can be contained in a block quote are other block quotes. That is, block quotes can be nested:

> This is a block quote.
> 
>> A block quote within a block quote.

**Standard markdown syntax does not require a blank line before a block quote. Pandoc does require this (except, of course, at the beginning of the document).**

The following does not produce a nested block quote in pandoc:

> This is a block quote.
>> Nested.


### Verbatim (code) blocks

### Indented code blocks

A block of text indented one tab is treated as verbatim text: that is, special characters do not trigger special formatting, and all spaces and line breaks are preserved.  For example,

	if (a > 3) {
		moveShip(5 * gravity, DOWN);
	}

The initial (four space or one tab) indentation is not considered part of the verbatim text, and is removed in the output.

Note: blank lines in the verbatim text need not begin with four spaces.

### Lists

### Bullet lists

A bullet list is a list of bulleted list items. A bulleted list
item begins with a bullet (`*`, `+`, or `-`). Here is a simple
example:

* one
* two
* three

### The four-space rule

A list item may contain multiple paragraphs and other block-level
content. However, subsequent paragraphs must be preceded by a blank line and indented four spaces or a tab. The list will look better if the first paragraph is aligned with the rest:

* First paragraph.
        
Continued.

* Second paragraph. With a code block, which must be indented
two tabs:
        
		{ code }

List items may include other lists.  In this case the preceding blank line is optional. The nested list must be indented one tab:

	* fruits
		+ apples
			- macintosh
			- red delicious
		+ pears
		+ peaches
	* vegetables
		+ brocolli
		+ chard

### Ordered lists 

Ordered lists work just like bulleted lists, except that the items begin with enumerators rather than bullets.

In standard markdown, enumerators are decimal numbers followed by a period and a space.  The numbers themselves are ignored, so there is no difference between this list:

	1.  one
	2.  two
	3.  three

and this one:

	5.  one
	7.  two
	1.  three

Unlike standard markdown, Pandoc allows ordered list items to be marked with uppercase and lowercase letters and roman numerals, in addition to arabic numerals. List markers may be enclosed in parentheses or followed by a single right-parentheses or period. They must be separated from the text that follows by at least one space, and, if the list marker is a capital letter with a period, by at least two spaces.

Pandoc also pays attention to the type of list marker used, and to the starting number, and both of these are preserved where possible in the output format. Thus, the following yields a list with numbers followed by a single parenthesis, starting with 9, and a sublist with lowercase roman numerals:

	9)  Ninth
	10)  Tenth
	11)  Eleventh
		i. subone
		ii. subtwo
		iii. subthree

Pandoc will start a new list each time a different type of list marker is used.  So, the following will create three lists:

	2) Two
	5) Three
	1. Four
	* Five

If default list markers are desired, use `#.`:

	#. one
	#. two
	#. three


### Definition lists 

Pandoc supports definition lists:

	Term 1

	:   Definition 1

	Term 2 with *inline markup*

	:   Definition 2

			{ some code, part of Definition 2 }

			Third paragraph of definition 2.

Each term must fit on one line, which may optionally be followed by a blank line, and must be followed by one or more definitions.
A definition begins with a colon or tilde, which may be indented one or two spaces. The body of the definition (including the first line, aside from the colon or tilde) should be indented four spaces. A term may have multiple definitions, and each definition may consist of one or more block elements (paragraph, code block, list, etc.), each indented four spaces or one tab stop.

If you leave space after the definition (as in the example above),
the blocks of the definitions will be considered paragraphs. In some output formats, this will mean greater spacing between term/definition pairs. For a compact definition list, do not leave space between the definition and the next term:

    Term 1
      ~ Definition 1
    Term 2
      ~ Definition 2a
      ~ Definition 2b

### Numbered example lists
 
The special list marker `@` can be used for sequentially numbered
examples. The first list item with a `@` marker will be numbered '1', the next '2', and so on, throughout the document. The numbered examples need not occur in a single list; each new list using `@` will take up where the last stopped. So, for example:

    (@)  My first example will be numbered (1).
    (@)  My second example will be numbered (2).

    Explanation of examples.

    (@)  My third example will be numbered (3).

Numbered examples can be labeled and referred to elsewhere in the
document:

    (@good)  This is a good example.

    As (@good) illustrates, ...

The label can be any string of alphanumeric characters, underscores, or hyphens.

### Ending a list

What if you want to put an indented code block after a list?

    -   item one
    -   item two

        { my code block }

Trouble! Here pandoc (like other markdown implementations) will treat `{ my code block }` as the second paragraph of item two, and not as a code block.

To "cut off" the list after item two, you can insert some non-indented content, like an HTML comment, which won't produce visible output in any format:

    -   item one
    -   item two

    <!-- end of list -->

        { my code block }

You can use the same trick if you want two consecutive lists instead of one big list:

    1.  one
    2.  two
    3.  three

    <!-- -->

    1.  uno
    2.  dos
    3.  tres

### Horizontal rules

A line containing a row of three or more `*`, `-`, or `_` characters
(optionally separated by spaces) produces a horizontal rule:

* * *

### Title block

If the file begins with a title block

    % title
    % author(s) (separated by semicolons)
    % date

it will be parsed as bibliographic information, not regular text. The block may contain just a title, a title and an author, or all three elements. If you want to include an author but no title, or a title and a date but no author, you need a blank line:

    %
    % Author

or

    % My title
    %
    % June 15, 2006

If a document has multiple authors, the authors may be separated by semicolons. 

    % Author One; Author Two

All three metadata fields may contain standard inline formatting
(italics, links, footnotes, etc.).

### Backslash escapes

Except inside a code block or inline code, any punctuation or space character preceded by a backslash will be treated literally, even if it would normally indicate formatting. 

Thus, for example, if one writes

    *\*hello\**

one will get

    <em>*hello*</em>

instead of

    <strong>hello</strong>

A backslash-escaped space is parsed as a nonbreaking space.

A backslash-escaped newline (i.e. a backslash occurring at the end of a line) is parsed as a hard line break.

Backslash escapes do not work in verbatim contexts.

### Smart punctuation

Pandoc will produce typographically correct output, converting straight quotes to curly quotes, `---` to em-dashes, `--` to en-dashes, and `...` to ellipses. Nonbreaking spaces are inserted after certain abbreviations, such as "Mr."

### Delimited code blocks

In addition to standard indented code blocks, Pandoc supports
*delimited* code blocks.  These begin with a row of three or more
tildes (`~`) or backticks (`` ` ``) and end with a row of tildes or backticks that must be at least as long as the starting row. Everything between these lines is treated as code. No indentation is necessary:

    ~~~~~~~
    if (a > 3) {
      moveShip(5 * gravity, DOWN);
    }
    ~~~~~~~

Like regular code blocks, delimited code blocks must be separated
from surrounding text by blank lines.

To specify the language of the code block:

    ```haskell
    qsort [] = []
    ```
which yields:

    <pre id="mycode" class="haskell">
      <code>
      ...
      </code>
    </pre>

### Verbatim

To make a short span of text verbatim, put it inside backticks:

    What is the difference between `>>=` and `>>`?

If the verbatim text includes a backtick, use double backticks:

    Here is a literal backtick `` ` ``.

(The spaces after the opening backticks and before the closing backticks will be ignored.)

The general rule is that a verbatim span starts with a string of consecutive backticks (optionally followed by a space) and ends with a string of the same number of backticks (optionally preceded by a space).

Note that backslash-escapes (and other markdown constructs) do not work in verbatim contexts:

    This is a backslash followed by an asterisk: `\*`.

### Superscripts and subscripts

Superscripts may be written by surrounding the superscripted text by `^` characters; subscripts may be written by surrounding the subscripted text by `~` characters. 

Thus, for example,

    H~2~O is a liquid.  2^10^ is 1024.

If the superscripted or subscripted text contains spaces, these spaces must be escaped with backslashes.  (This is to prevent accidental superscripting and subscripting through the ordinary use of `~` and `^`.)

Thus, if you want the letter P with 'a cat' in subscripts, use
`P~a\ cat~`, not `P~a cat~`.


### Math

Anything between two `$` characters will be treated as TeX math.  The opening `$` must have a character immediately to its right, while the closing `$` must have a character immediately to its left.  Thus, `$20,000 and $30,000` won't parse as math.  If for some reason you need to enclose text in literal `$` characters, backslash-escape them and they won't be treated as math delimiters.

TeX math will be printed in all output formats. How it is rendered depends on the output format:

* HTML: with (mathjax)[http://www.mathjax.org/]
* Latex: with Latex

### Raw HTML

Markdown allows you to insert raw HTML anywhere in a document (except verbatim contexts, where `<`, `>`, and `&` are interpreted literally).

Standard markdown allows you to include HTML "blocks": blocks
of HTML between balanced tags that are separated from the surrounding text with blank lines, and start and end at the left margin. 

Within these blocks, everything is interpreted as HTML, not markdown; so (for example), `*` does not signify emphasis.

Pandoc interprets material between HTML block tags as markdown.
Thus, for example, Pandoc will turn

    <table>
    	<tr>
    		<td>*one*</td>
    		<td>[a link](http://google.com)</td>
    	</tr>
    </table>

into

    <table>
    	<tr>
    		<td><em>one</em></td>
    		<td><a href="http://google.com">a link</a></td>
    	</tr>
    </table>

There is one exception to this rule: text between `<script>` and
`<style>` tags is not interpreted as markdown.

### Raw TeX

In addition to raw HTML, pandoc allows raw LaTeX, TeX, and ConTeXt to be included in a document. Inline TeX commands will be preserved and passed unchanged to the LaTeX and ConTeXt writers. Thus, for example, you can use LaTeX to include BibTeX citations:

    This result was proved in \cite{jones.1967}.

Note that in LaTeX environments, like

    \begin{tabular}{|l|l|}\hline
    Age & Frequency \\ \hline
    18--25  & 15 \\
    26--35  & 33 \\
    36--45  & 22 \\ \hline
    \end{tabular}

the material between the begin and end tags will be interpreted as raw LaTeX, not as markdown.

Inline LaTeX is ignored in output formats other than Markdown, LaTeX, and ConTeXt.

### LaTeX macros

For output formats other than LaTeX, pandoc will parse LaTeX `\newcommand` and `\renewcommand` definitions and apply the resulting macros to all LaTeX math.  So, for example, the following will work in all output formats, not just LaTeX:

    \newcommand{\tuple}[1]{\langle #1 \rangle}

    $\tuple{a, b, c}$

In LaTeX output, the `\newcommand` definition will simply be passed unchanged to the output.

### Links

Markdown allows links to be specified in several ways.

#### Automatic links

If you enclose a URL or email address in pointy brackets, it
will become a link:

    <http://google.com>
    <sam@green.eggs.ham>

Pandoc will render autolinked URLs and email addresses as
inline code.

#### Inline links

An inline link consists of the link text in square brackets,
followed by the URL in parentheses. (Optionally, the URL can
be followed by a link title, in quotes.)

    This is an [inline link](/url), and here's [one with
    a title](http://fsf.org "click here for a good time!").

There can be no space between the bracketed part and the parenthesized part. The link text can contain formatting (such as emphasis), but the title cannot.


#### Reference links

An *explicit* reference link has two parts, the link itself and the link definition, which may occur elsewhere in the document (either before or after the link).

The link consists of link text in square brackets, followed by a label in square brackets. (There can be space between the two.) The link definition must begin at the left margin or indented no more than three spaces. It consists of the bracketed label, followed by a colon and a space, followed by the URL, and optionally (after a space) a link title either in quotes or in
parentheses.

Here are some examples:

    [my label 1]: /foo/bar.html  "My title, optional"
    [my label 2]: /foo
    [my label 3]: http://fsf.org (The free software foundation)
    [my label 4]: /bar#special  'A title in single quotes'

The URL may optionally be surrounded by angle brackets:

    [my label 5]: <http://foo.bar.baz>

The title may go on the next line:

    [my label 3]: http://fsf.org
      "The free software foundation"

Note that link labels are not case sensitive.  So, this will work:

    Here is [my link][FOO]

    [Foo]: /bar/baz

In an *implicit* reference link, the second pair of brackets is
empty, or omitted entirely:

    See [my website][], or [my website].

    [my website]: http://foo.bar.baz

#### Internal links

To link to another section of the same document, use the automatically
generated identifier (see [Header identifiers in HTML, LaTeX, and
ConTeXt](#header-identifiers-in-html-latex-and-context), below).
For example:

    See the [Introduction](#introduction).

or

    See the [Introduction].

    [Introduction]: #introduction

Internal links are currently supported for HTML formats (including
HTML slide shows and EPUB), LaTeX, and ConTeXt.

### Images

A link immediately preceded by a `!` will be treated as an image.
The link text will be used as the image's alt text:

    ![la lune](lalune.jpg "Voyage to the moon")

    ![movie reel]

    [movie reel]: movie.gif

### Pictures with captions

An image occurring by itself in a paragraph will be rendered as
a figure with a caption.[^5] (In LaTeX, a figure environment will be used; in HTML, the image will be placed in a `<div>` with class
`.figure`, together with a caption in a `p` with class `caption`.)
The image's alt text will be used as the caption.

    ![This is the caption](/url/of/image.png)

If you just want a regular inline image, just make sure it is not
the only thing in the paragraph. One way to do this is to insert a
nonbreaking space after the image:

    ![This image won't be a figure](/url/of/image.png)\


### Footnotes

Pandoc's markdown allows footnotes, using the following syntax:

    Here is a footnote reference,[^1] and another.[^longnote]

    [^1]: Here is the footnote.

    [^longnote]: Here's one with multiple blocks.

        Subsequent paragraphs are indented to show that they
    belong to the previous footnote.

            { some.code }

		The whole paragraph can be indented, or just the first
        line.  In this way, multi-paragraph footnotes work like
        multi-paragraph list items.

    This paragraph won't be part of the note, because it
    isn't indented.

The identifiers in footnote references may not contain spaces, tabs, or newlines. These identifiers are used only to correlate the footnote reference with the note itself; in the output, footnotes will be numbered sequentially.

The footnotes themselves need not be placed at the end of the
document. They may appear anywhere except inside other block elements (lists, block quotes, tables, etc.).

Inline footnotes are also allowed (though, unlike regular notes,
they cannot contain multiple paragraphs).

The syntax is as follows:

    Here is an inline note.^[Inlines notes are easier to write, since you don't have to pick an identifier and move down to type the note.]

Inline and regular footnotes may be mixed freely.

## Authors of this documentation

© 2006-2012 John MacFarlane (jgm at berkeley dot edu). Released under the [GPL], version 2 or greater.  This software carries no warranty of any kind.  (See COPYRIGHT for full copyright and warranty notices.) Other contributors include Recai Oktaş, Paulo Tanimoto, Peter Wang, Andrea Rossato, Eric Kow, infinity0x, Luke Plant, shreevatsa.public, Puneeth Chaganti, Paul Rivier, rodja.trappe, Bradley Kuhn, thsutton, Nathan Gass, Jonathan Daugherty, Jérémy Bobbio, Justin Bogner, qerub, Christopher Sawicki, Kelsey Hightower, Masayoshi Takahashi, Antoine Latter, Ralf Stephan, Eric Seidel, B. Scott Michel, Gavin Beatty, Sergey Astanin.

© Reworked for UberWriter: Wolf Vollprecht