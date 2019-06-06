# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2019, Wolf Vollprecht <w.vollprecht@gmail.com>
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
from gi.overrides import GLib

from uberwriter import helpers, markup_regex

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango


class MarkupHandler:
    # Maximum number of characters for which to markup synchronously.
    max_char_sync = 100000

    def __init__(self, text_view):
        self.text_view = text_view
        self.text_buffer = text_view.get_buffer()

        # Styles
        buffer = self.text_buffer

        self.italic = buffer.create_tag('italic',
                                        weight=Pango.Weight.NORMAL,
                                        style=Pango.Style.ITALIC)

        self.bold = buffer.create_tag('bold',
                                      weight=Pango.Weight.BOLD,
                                      style=Pango.Style.NORMAL)

        self.bolditalic = buffer.create_tag('bolditalic',
                                            weight=Pango.Weight.BOLD,
                                            style=Pango.Style.ITALIC)

        self.strikethrough = buffer.create_tag('strikethrough', strikethrough=True)

        self.horizontalrule = buffer.create_tag('centertext',
                                                justification=Gtk.Justification.CENTER)

        self.plaintext = buffer.create_tag('plaintext',
                                           weight=Pango.Weight.NORMAL,
                                           style=Pango.Style.NORMAL,
                                           strikethrough=False,
                                           justification=Gtk.Justification.LEFT)

        self.table = buffer.create_tag('table',
                                       wrap_mode=Gtk.WrapMode.NONE,
                                       pixels_above_lines=0,
                                       pixels_below_lines=0)

        self.mathtext = buffer.create_tag('mathtext',
                                          weight=Pango.Weight.NORMAL,
                                          style=Pango.Style.NORMAL,
                                          strikethrough=False)

        self.graytext = buffer.create_tag('graytext',
                                          foreground='gray',
                                          weight=Pango.Weight.NORMAL,
                                          style=Pango.Style.NORMAL)

        # Margin and indents
        # A baseline margin is set to allow negative offsets for formatting headers, lists, etc
        self.margins_indents = {}
        self.baseline_margin = 0
        self.char_width = 0
        self.update_margins_indents()

        # Style
        self.on_style_updated()

        self.version = 0

    def on_style_updated(self, *_):
        (found, color) = self.text_view.get_style_context().lookup_color('math_text_color')
        if not found:
            (_, color) = self.text_view.get_style_context().lookup_color('foreground_color')
        self.mathtext.set_property("foreground", color.to_string())

    def apply(self):
        self.version = self.version + 1
        if self.text_buffer.get_char_count() < self.max_char_sync:
            self.do_apply()
        else:
            GLib.idle_add(self.do_apply, self.version)

    def do_apply(self, version=None):
        if version is not None and version != self.version:
            return

        buffer = self.text_buffer
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_slice(start, end, False)

        # Remove tags
        buffer.remove_tag(self.italic, start, end)
        buffer.remove_tag(self.bold, start, end)
        buffer.remove_tag(self.bolditalic, start, end)
        buffer.remove_tag(self.strikethrough, start, end)
        buffer.remove_tag(self.horizontalrule, start, end)
        buffer.remove_tag(self.plaintext, start, end)
        buffer.remove_tag(self.table, start, end)
        buffer.remove_tag(self.mathtext, start, end)
        for tag in self.margins_indents.values():
            buffer.remove_tag(tag, start, end)
        buffer.remove_tag(self.graytext, start, end)

        # Apply "_italic_" tag (italic)
        matches = re.finditer(markup_regex.ITALIC, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.italic, start_iter, end_iter)

        # Apply "**bold**" tag (bold)
        matches = re.finditer(markup_regex.BOLD, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.bold, start_iter, end_iter)

        # Apply "***bolditalic***" tag (bold/italic)
        matches = re.finditer(markup_regex.BOLD_ITALIC, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.bolditalic, start_iter, end_iter)

        # Apply "~~strikethrough~~" tag (strikethrough)
        matches = re.finditer(markup_regex.STRIKETHROUGH, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.strikethrough, start_iter, end_iter)

        # Apply "[description](url)" (gray out)
        matches = re.finditer(markup_regex.LINK, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start("text") - 1)
            end_iter = start_iter.copy()
            end_iter.forward_char()
            buffer.apply_tag(self.graytext, start_iter, end_iter)
            start_iter = buffer.get_iter_at_offset(match.start("url") - 2)
            end_iter = buffer.get_iter_at_offset(match.end("url") + 1)
            buffer.apply_tag(self.graytext, start_iter, end_iter)

        # Apply "---" horizontal rule tag (center)
        matches = re.finditer(markup_regex.HORIZONTAL_RULE, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start("symbols"))
            end_iter = buffer.get_iter_at_offset(match.end("symbols"))
            buffer.apply_tag(self.horizontalrule, start_iter, end_iter)

        # Apply "* list" tag (offset)
        matches = re.finditer(markup_regex.LIST, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            # Lists use character+space (eg. "* ")
            length = 2
            nest = len(match.group("indent").replace("    ", "\t"))
            margin = -length - 2 * nest
            indent = -length - 2 * length * nest
            buffer.apply_tag(self.get_margin_indent_tag(margin, indent), start_iter, end_iter)

        # Apply "1. ordered list" tag (offset)
        matches = re.finditer(markup_regex.ORDERED_LIST, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            # Numeric lists use numbers/letters+dot/parens+space (eg. "123. ")
            length = len(match.group("prefix")) + 1
            nest = len(match.group("indent").replace("    ", "\t"))
            margin = -length - 2 * nest
            indent = -length - 2 * length * nest
            buffer.apply_tag(self.get_margin_indent_tag(margin, indent), start_iter, end_iter)

        # Apply "> blockquote" tag (offset)
        matches = re.finditer(markup_regex.BLOCK_QUOTE, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.get_margin_indent_tag(2, -2), start_iter, end_iter)

        # Apply "#" tag (bold)
        matches = re.finditer(markup_regex.HEADER, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            margin = -len(match.group("level")) - 1
            buffer.apply_tag(self.get_margin_indent_tag(margin, 0), start_iter, end_iter)
            buffer.apply_tag(self.bold, start_iter, end_iter)

        # Apply "======" header underline tag (bold)
        matches = re.finditer(markup_regex.HEADER_UNDER, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.bold, start_iter, end_iter)

        # Apply "```" code tag (offset)
        matches = re.finditer(markup_regex.CODE_BLOCK, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start("block"))
            end_iter = buffer.get_iter_at_offset(match.end("block"))
            buffer.apply_tag(self.get_margin_indent_tag(0, 2), start_iter, end_iter)
            buffer.apply_tag(self.plaintext, start_iter, end_iter)

        # Apply "---" table tag (wrap/pixels)
        matches = re.finditer(markup_regex.TABLE, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.table, start_iter, end_iter)

        # Apply "$math$" tag (colorize)
        matches = re.finditer(markup_regex.MATH, text)
        for match in matches:
            start_iter = buffer.get_iter_at_offset(match.start())
            end_iter = buffer.get_iter_at_offset(match.end())
            buffer.apply_tag(self.mathtext, start_iter, end_iter)

        # Apply focus mode tag (grey out before/after current sentence)
        if self.text_view.focus_mode:
            cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
            start_sentence = cursor_iter.copy()
            start_sentence.backward_sentence_start()
            end_sentence = cursor_iter.copy()
            end_sentence.forward_sentence_end()
            buffer.apply_tag(self.graytext, start, start_sentence)
            buffer.apply_tag(self.graytext, end_sentence, end)

    # Margin and indent are cumulative. They differ in two ways:
    # * Margin is always in the beginning, which means it effectively only affects the first line
    # of multi-line text. Indent is applied to every line.
    # * Margin level can be negative, as a baseline margin exists from which it can be subtracted.
    # Indent is always positive, or 0.
    def get_margin_indent_tag(self, margin_level, indent_level):
        level = (margin_level, indent_level)
        if level not in self.margins_indents:
            margin, indent = self.get_margin_indent(margin_level, indent_level)
            tag = self.text_buffer.create_tag(
                "margin_indent_{}_{}".format(margin_level, indent_level),
                left_margin=margin, indent=indent)
            self.margins_indents[level] = tag
            return tag
        else:
            return self.margins_indents[level]

    def get_margin_indent(self, margin_level, indent_level, baseline_margin=None, char_width=None):
        if baseline_margin is None:
            baseline_margin = self.text_view.props.left_margin
        if char_width is None:
            char_width = helpers.get_char_width(self.text_view)
        margin = max(baseline_margin + char_width * margin_level, 0)
        indent = char_width * indent_level
        return margin, indent

    def update_margins_indents(self):
        baseline_margin = self.text_view.props.left_margin
        char_width = helpers.get_char_width(self.text_view)

        # Bail out if neither the baseline margin nor character width change
        if baseline_margin == self.baseline_margin and char_width == self.char_width:
            return
        self.baseline_margin = baseline_margin
        self.char_width = char_width

        # Adjust tab size
        tab_array = Pango.TabArray.new(1, True)
        tab_array.set_tab(0, Pango.TabAlign.LEFT, 4 * char_width)
        self.text_view.set_tabs(tab_array)

        # Adjust margins and indents
        for level, tag in self.margins_indents.items():
            margin, indent = self.get_margin_indent(*level, baseline_margin, char_width)
            tag.set_properties(left_margin=margin, indent=indent)
