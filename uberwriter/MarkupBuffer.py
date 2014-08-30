# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012, Wolf Vollprecht <w.vollprecht@gmail.com>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import re
from gi.repository import Gtk  # pylint: disable=E0611
from gi.repository import Pango  # pylint: disable=E0611


class MarkupBuffer():

    def __init__(self, Parent, TextBuffer, base_leftmargin):
        self.multiplier = 10
        self.parent = Parent
        self.TextBuffer = TextBuffer

        # Styles
        self.italic = self.TextBuffer.create_tag("italic",
            style=Pango.Style.ITALIC)

        self.emph = self.TextBuffer.create_tag("emph",
            weight=Pango.Weight.BOLD,
            style=Pango.Style.NORMAL)

        self.bolditalic = self.TextBuffer.create_tag("bolditalic",
            weight=Pango.Weight.BOLD,
            style=Pango.Style.ITALIC)

        self.headline_two = self.TextBuffer.create_tag("headline_two",
            weight=Pango.Weight.BOLD,
            style=Pango.Style.NORMAL)

        self.normal_indent = self.TextBuffer.create_tag('normal_indent', indent=100)

        self.green_text = self.TextBuffer.create_tag(
            "greentext",
            foreground="#00364C"
            )

        self.grayfont = self.TextBuffer.create_tag('graytag',
            foreground="gray")

        self.blackfont = self.TextBuffer.create_tag('blacktag',
            foreground="#222")

        self.underline = self.TextBuffer.create_tag(
            "underline",
            underline=Pango.Underline.SINGLE
            )

        self.underline.set_property('weight', Pango.Weight.BOLD)

        self.strikethrough = self.TextBuffer.create_tag(
            "strikethrough",
            strikethrough=True
            )

        self.centertext = self.TextBuffer.create_tag(
            "centertext",
            justification=Gtk.Justification.CENTER
        )

        self.TextBuffer.apply_tag(
            self.normal_indent,
            self.TextBuffer.get_start_iter(),
            self.TextBuffer.get_end_iter()
        )

        self.rev_leftmargin = []
        for i in range(0, 6):
            name = "rev_marg_indent_left" + str(i)
            self.rev_leftmargin.append(self.TextBuffer.create_tag(name))
            self.rev_leftmargin[i].set_property("left-margin", 90 - 10 * (i + 1))
            self.rev_leftmargin[i].set_property("indent", - 10 * (i + 1) - 10)
            #self.leftmargin[i].set_property("background", "gray")

        self.leftmargin = []

        for i in range(0, 6):
            name = "marg_indent_left" + str(i)
            self.leftmargin.append(self.TextBuffer.create_tag(name))
            self.leftmargin[i].set_property("left-margin", base_leftmargin + 10 + 10 * (i + 1))
            self.leftmargin[i].set_property("indent", - 10 * (i + 1) - 10)

        self.leftindent = []

        for i in range(0, 15):
            name = "indent_left" + str(i)
            self.leftindent.append(self.TextBuffer.create_tag(name))
            self.leftindent[i].set_property("indent", - 10 * (i + 1) - 20)

        self.table_env = self.TextBuffer.create_tag('table_env')
        self.table_env.set_property('wrap-mode', Gtk.WrapMode.NONE)
        # self.table_env.set_property('font', 'Ubuntu Mono 13px')
        self.table_env.set_property('pixels-above-lines', 0)
        self.table_env.set_property('pixels-below-lines', 0)

        # self.ftag = self.TextBuffer.create_tag("pix_front", pixels_above_lines = 100)
    regex = {
        "ITALIC": re.compile(r"\*\w(.+?)\*| _\w(.+?)_ ", re.UNICODE),   # *asdasd* // _asdasd asd asd_
        "STRONG": re.compile(r"\*{2}\w(.+?)\*{2}| [_]{2}\w(.+?)[_]{2} ", re.UNICODE),   # **as das** // __asdasdasd asd ad a__
        "STRONGITALIC": re.compile(r"\*{3}\w(.+?)\*{3}| [_]{3}\w(.+?)[_]{3} "),
        "BLOCKQUOTE": re.compile(r"^([\>]+ )", re.MULTILINE),
        "STRIKETHROUGH": re.compile(r"~~[^ `~\n].+?~~"),
        "LIST": re.compile(r"^[\-\*\+] ", re.MULTILINE),
        "NUMERICLIST": re.compile(r"^((\d|[a-z]|\#)+[\.\)]) ", re.MULTILINE),
        "INDENTEDLIST": re.compile(r"^(\t{1,6})((\d|[a-z]|\#)+[\.\)]|[\-\*\+]) ", re.MULTILINE),
        "HEADINDICATOR": re.compile(r"^(#{1,6}) ", re.MULTILINE),
        "HEADLINE": re.compile(r"^(#{1,6} [^\n]+)", re.MULTILINE),
        "HEADLINE_TWO": re.compile(r"^\w.+\n[\=\-]{3,}", re.MULTILINE),
        "MATH": re.compile(r"[\$]{1,2}([^` ].+?[^`\\ ])[\$]{1,2}"),
        "HORIZONTALRULE": re.compile(r"(\n\n[\*\-]{3,}\n)"),
        "TABLE": re.compile(r"^[\-\+]{5,}\n(.+?)\n[\-\+]{5,}\n", re.DOTALL),
        "LINK": re.compile(r"\(http(.+?)\)")
    }

    def markup_buffer(self, mode=0):
        buf = self.TextBuffer

        # Test for shifting first line
        # bbs = buf.get_start_iter()
        # bbb = buf.get_iter_at_offset(3)

        # buf.apply_tag(self.ftag, bbs, bbb)

        # Modes:
        # 0 -> start to end
        # 1 -> around the cursor
        # 2 -> n.d.

        if mode == 0:
            context_start = buf.get_start_iter()
            context_end = buf.get_end_iter()
            context_offset = 0
        elif mode == 1:
            cursor_mark = buf.get_insert()
            context_start = buf.get_iter_at_mark(cursor_mark)
            context_start.backward_lines(3)
            context_end = buf.get_iter_at_mark(cursor_mark)
            context_end.forward_lines(2)
            context_offset = context_start.get_offset()

        text = buf.get_slice(context_start, context_end, False)

        self.TextBuffer.remove_tag(self.italic, context_start, context_end)

        matches = re.finditer(self.regex["ITALIC"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.italic, startIter, endIter)

        self.TextBuffer.remove_tag(self.emph, context_start, context_end)

        matches = re.finditer(self.regex["STRONG"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.emph, startIter, endIter)

        matches = re.finditer(self.regex["STRONGITALIC"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.bolditalic, startIter, endIter)

        self.TextBuffer.remove_tag(self.strikethrough, context_start, context_end)

        matches = re.finditer(self.regex["STRIKETHROUGH"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.strikethrough, startIter, endIter)

        self.TextBuffer.remove_tag(self.green_text, context_start, context_end)

        matches = re.finditer(self.regex["MATH"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.green_text, startIter, endIter)

        for margin in self.rev_leftmargin:
            self.TextBuffer.remove_tag(margin, context_start, context_end)

        matches = re.finditer(self.regex["LIST"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.rev_leftmargin[0], startIter, endIter)

        matches = re.finditer(self.regex["NUMERICLIST"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            index = len(match.group(1)) - 1
            if index < len(self.rev_leftmargin):
                margin = self.rev_leftmargin[index]
                self.TextBuffer.apply_tag(margin, startIter, endIter)

        matches = re.finditer(self.regex["BLOCKQUOTE"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            index = len(match.group(1)) - 2
            if index < len(self.leftmargin):
                self.TextBuffer.apply_tag(self.leftmargin[index], startIter, endIter)

        for leftindent in self.leftindent:
            self.TextBuffer.remove_tag(leftindent, context_start, context_end)

        matches = re.finditer(self.regex["INDENTEDLIST"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            index = (len(match.group(1)) - 1) * 2 + len(match.group(2))
            if index < len(self.leftindent):
                self.TextBuffer.apply_tag(self.leftindent[index], startIter, endIter)

        matches = re.finditer(self.regex["HEADINDICATOR"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            index = len(match.group(1)) - 1
            if index < len(self.rev_leftmargin):
                margin = self.rev_leftmargin[index]
                self.TextBuffer.apply_tag(margin, startIter, endIter)

        matches = re.finditer(self.regex["HORIZONTALRULE"], text)
        rulecontext = context_start.copy()
        rulecontext.forward_lines(3)
        self.TextBuffer.remove_tag(self.centertext, rulecontext, context_end)

        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            startIter.forward_chars(2)
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.centertext, startIter, endIter)

        matches = re.finditer(self.regex["HEADLINE"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.emph, startIter, endIter)

        matches = re.finditer(self.regex["HEADLINE_TWO"], text)
        self.TextBuffer.remove_tag(self.headline_two, rulecontext, context_end)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.headline_two, startIter, endIter)

        matches = re.finditer(self.regex["TABLE"], text)
        for match in matches:
            startIter = buf.get_iter_at_offset(context_offset + match.start())
            endIter = buf.get_iter_at_offset(context_offset + match.end())
            self.TextBuffer.apply_tag(self.table_env, startIter, endIter)

        if self.parent.focusmode:
            self.focusmode_highlight()

    def focusmode_highlight(self):
        self.TextBuffer.apply_tag(self.grayfont,
            self.TextBuffer.get_start_iter(),
            self.TextBuffer.get_end_iter())

        self.TextBuffer.remove_tag(self.blackfont,
            self.TextBuffer.get_start_iter(),
            self.TextBuffer.get_end_iter())

        cursor = self.TextBuffer.get_mark("insert")
        cursor_iter = self.TextBuffer.get_iter_at_mark(cursor)

        end_sentence = cursor_iter.copy()
        end_sentence.forward_sentence_end()

        end_line = cursor_iter.copy()
        end_line.forward_to_line_end()

        comp = end_line.compare(end_sentence)
        # if comp < 0, end_line is BEFORE end_sentence
        if comp <= 0:
            end_sentence = end_line

        start_sentence = cursor_iter.copy()
        start_sentence.backward_sentence_start()

        self.TextBuffer.apply_tag(self.blackfont,
            start_sentence, end_sentence)

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier

    def recalculate(self, lm):
        multiplier = self.multiplier
        for i in range(0, 6):
            self.rev_leftmargin[i].set_property("left-margin", (lm - multiplier) - multiplier * (i + 1))
            self.rev_leftmargin[i].set_property("indent", - multiplier * (i + 1) - multiplier)

        for i in range(0, 6):
            self.leftmargin[i].set_property("left-margin", (lm - multiplier) + multiplier + multiplier * (i + 1))
            self.leftmargin[i].set_property("indent", - (multiplier - 1) * (i + 1) - multiplier)

    def dark_mode(self, active=False):
        if active:
            self.green_text.set_property("foreground", "#FA5B0F")
            self.grayfont.set_property("foreground", "#666")
            self.blackfont.set_property("foreground", "#CCC")
        else:
            self.green_text.set_property("foreground", "#00364C")
            self.grayfont.set_property("foreground", "gray")
            self.blackfont.set_property("foreground", "#222")
