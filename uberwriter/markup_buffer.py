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
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango


class MarkupBuffer():
    regex = {
        "ITALIC": re.compile(r"(\*|_)(.*?)\1", re.UNICODE),  # *asdasd* // _asdasd asd asd_
        "STRONG": re.compile(r"(\*\*|__)(.*?)\1", re.UNICODE),  # **as das** // __asdasd asd ad a__
        "STRONGITALIC": re.compile(r"(\*\*\*|___)(.*?)\1"),
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

    def __init__(self, window, text_editor, base_leftmargin):
        self.margin_multiplier = 10
        self.parent = window
        self.text_editor = text_editor
        self.text_buffer = text_editor.get_buffer()

        # Styles
        self.italic = self.text_buffer.create_tag("italic",
                                                  style=Pango.Style.ITALIC)

        self.emph = self.text_buffer.create_tag("emph",
                                                weight=Pango.Weight.BOLD,
                                                style=Pango.Style.NORMAL)

        self.bolditalic = self.text_buffer.create_tag("bolditalic",
                                                      weight=Pango.Weight.BOLD,
                                                      style=Pango.Style.ITALIC)

        self.headline_two = self.text_buffer.create_tag("headline_two",
                                                        weight=Pango.Weight.BOLD,
                                                        style=Pango.Style.NORMAL)

        self.normal_indent = self.text_buffer.create_tag('normal_indent', indent=100)

        self.math_text = self.text_buffer.create_tag('math_text')

        self.unfocused_text = self.text_buffer.create_tag('graytag',
                                                          foreground="gray")

        self.underline = self.text_buffer.create_tag("underline",
                                                     underline=Pango.Underline.SINGLE)

        self.underline.set_property('weight', Pango.Weight.BOLD)

        self.strikethrough = self.text_buffer.create_tag("strikethrough",
                                                         strikethrough=True)

        self.centertext = self.text_buffer.create_tag("centertext",
                                                      justification=Gtk.Justification.CENTER)

        self.text_buffer.apply_tag(
            self.normal_indent,
            self.text_buffer.get_start_iter(),
            self.text_buffer.get_end_iter()
        )

        self.rev_leftmargin = []
        for i in range(0, 6):
            name = "rev_marg_indent_left" + str(i)
            self.rev_leftmargin.append(self.text_buffer.create_tag(name))
            self.rev_leftmargin[i].set_property("left-margin", 90 - 10 * (i + 1))
            self.rev_leftmargin[i].set_property("indent", - 10 * (i + 1) - 10)
            #self.leftmargin[i].set_property("background", "gray")

        self.leftmargin = []

        for i in range(0, 6):
            name = "marg_indent_left" + str(i)
            self.leftmargin.append(self.text_buffer.create_tag(name))
            self.leftmargin[i].set_property("left-margin", base_leftmargin + 10 + 10 * (i + 1))
            self.leftmargin[i].set_property("indent", - 10 * (i + 1) - 10)

        self.leftindent = []

        for i in range(0, 15):
            name = "indent_left" + str(i)
            self.leftindent.append(self.text_buffer.create_tag(name))
            self.leftindent[i].set_property("indent", - 10 * (i + 1) - 20)

        self.table_env = self.text_buffer.create_tag('table_env')
        self.table_env.set_property('wrap-mode', Gtk.WrapMode.NONE)
        self.table_env.set_property('pixels-above-lines', 0)
        self.table_env.set_property('pixels-below-lines', 0)

        # Theme
        self.text_editor.connect('style-updated', self.apply_current_theme)
        self.apply_current_theme()

    def apply_current_theme(self, *_):
        # Math text color
        (found, color) = self.text_editor.get_style_context().lookup_color('math_text_color')
        if not found:
            (_, color) = self.text_editor.get_style_context().lookup_color('foreground_color')
        self.math_text.set_property("foreground", color.to_string())

        # Margin
        mets = self.text_editor.get_pango_context().get_metrics()
        self.set_multiplier(Pango.units_to_double(mets.get_approximate_char_width()) + 1)

    def markup_buffer(self, mode=0):
        buf = self.text_buffer

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

        self.text_buffer.remove_tag(self.italic, context_start, context_end)

        matches = re.finditer(self.regex["ITALIC"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.italic, start_iter, end_iter)

        self.text_buffer.remove_tag(self.emph, context_start, context_end)

        matches = re.finditer(self.regex["STRONG"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.emph, start_iter, end_iter)

        matches = re.finditer(self.regex["STRONGITALIC"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.bolditalic, start_iter, end_iter)

        self.text_buffer.remove_tag(self.strikethrough, context_start, context_end)

        matches = re.finditer(self.regex["STRIKETHROUGH"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.strikethrough, start_iter, end_iter)

        self.text_buffer.remove_tag(self.math_text, context_start, context_end)

        matches = re.finditer(self.regex["MATH"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.math_text, start_iter, end_iter)

        for margin in self.rev_leftmargin:
            self.text_buffer.remove_tag(margin, context_start, context_end)

        matches = re.finditer(self.regex["LIST"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.rev_leftmargin[0], start_iter, end_iter)

        matches = re.finditer(self.regex["NUMERICLIST"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            index = len(match.group(1)) - 1
            if index < len(self.rev_leftmargin):
                margin = self.rev_leftmargin[index]
                self.text_buffer.apply_tag(margin, start_iter, end_iter)

        matches = re.finditer(self.regex["BLOCKQUOTE"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            index = len(match.group(1)) - 2
            if index < len(self.leftmargin):
                self.text_buffer.apply_tag(self.leftmargin[index], start_iter, end_iter)

        for leftindent in self.leftindent:
            self.text_buffer.remove_tag(leftindent, context_start, context_end)

        matches = re.finditer(self.regex["INDENTEDLIST"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            index = (len(match.group(1)) - 1) * 2 + len(match.group(2))
            if index < len(self.leftindent):
                self.text_buffer.apply_tag(self.leftindent[index], start_iter, end_iter)

        matches = re.finditer(self.regex["HEADINDICATOR"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            index = len(match.group(1)) - 1
            if index < len(self.rev_leftmargin):
                margin = self.rev_leftmargin[index]
                self.text_buffer.apply_tag(margin, start_iter, end_iter)

        matches = re.finditer(self.regex["HORIZONTALRULE"], text)
        rulecontext = context_start.copy()
        rulecontext.forward_lines(3)
        self.text_buffer.remove_tag(self.centertext, rulecontext, context_end)

        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            start_iter.forward_chars(2)
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.centertext, start_iter, end_iter)

        matches = re.finditer(self.regex["HEADLINE"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.emph, start_iter, end_iter)

        matches = re.finditer(self.regex["HEADLINE_TWO"], text)
        self.text_buffer.remove_tag(self.headline_two, rulecontext, context_end)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.headline_two, start_iter, end_iter)

        matches = re.finditer(self.regex["TABLE"], text)
        for match in matches:
            start_iter = buf.get_iter_at_offset(context_offset + match.start())
            end_iter = buf.get_iter_at_offset(context_offset + match.end())
            self.text_buffer.apply_tag(self.table_env, start_iter, end_iter)

        if self.parent.focusmode:
            self.focusmode_highlight()

    def focusmode_highlight(self):
        start_document = self.text_buffer.get_start_iter()
        end_document = self.text_buffer.get_end_iter()

        self.text_buffer.remove_tag(
            self.unfocused_text,
            start_document,
            end_document)

        cursor = self.text_buffer.get_mark("insert")
        cursor_iter = self.text_buffer.get_iter_at_mark(cursor)

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

        # grey out everything before
        self.text_buffer.apply_tag(
            self.unfocused_text,
            self.text_buffer.get_start_iter(), start_sentence)

        self.text_buffer.apply_tag(
            self.unfocused_text,
            end_sentence, self.text_buffer.get_end_iter())

    def set_multiplier(self, multiplier):
        self.margin_multiplier = multiplier

    def recalculate(self, lm):
        multiplier = self.margin_multiplier
        for i in range(0, 6):
            new_margin = (lm - multiplier) - multiplier * (i + 1)
            self.rev_leftmargin[i].set_property("left-margin", 0 if new_margin < 0 else new_margin)
            self.rev_leftmargin[i].set_property("indent", - multiplier * (i + 1) - multiplier)

        for i in range(0, 6):
            new_margin = (lm - multiplier) + multiplier + multiplier * (i + 1)
            self.leftmargin[i].set_property("left-margin", 0 if new_margin < 0 else new_margin)
            self.leftmargin[i].set_property("indent", - (multiplier - 1) * (i + 1) - multiplier)
