# Copyright (C) 2022, Manuel Genovés <manuel.genoves@gmail.com>
#               2019, Gonçalo Silva
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
# END LICENSE

from gi.repository import Pango
from gi.repository import Gtk, GLib
import re
from multiprocessing import Pipe, Process

import gi

from apostrophe import helpers, markup_regex
from apostrophe.markup_regex import STRIKETHROUGH, BOLD_ITALIC,\
    BOLD, ITALIC_ASTERISK, ITALIC_UNDERSCORE, IMAGE, LINK, LINK_ALT,\
    HORIZONTAL_RULE, LIST, ORDERED_LIST, BLOCK_QUOTE, HEADER, HEADER_UNDER,\
    TABLE, MATH, CODE

gi.require_version('Gtk', '3.0')


class MarkupHandler:
    TAG_NAME_ITALIC = 'italic'
    TAG_NAME_BOLD = 'bold'
    TAG_NAME_BOLD_ITALIC = 'bold_italic'
    TAG_NAME_STRIKETHROUGH = 'strikethrough'
    TAG_NAME_CENTER = 'center'
    TAG_NAME_WRAP_NONE = 'wrap_none'
    TAG_NAME_PLAIN_TEXT = 'plain_text'
    TAG_NAME_GRAY_TEXT = 'gray_text'
    TAG_NAME_CODE_TEXT = 'code_text'
    TAG_NAME_CODE_BLOCK = 'code_block'
    TAG_NAME_UNFOCUSED_TEXT = 'unfocused_text'
    TAG_NAME_MARGIN_INDENT = 'margin_indent'

    def __init__(self, text_view):
        self.text_view = text_view
        self.text_buffer = text_view.get_buffer()
        self.marked_up_text = None

        # Tags.
        buffer = self.text_buffer

        self.tag_italic = buffer.create_tag(self.TAG_NAME_ITALIC,
                                            weight=Pango.Weight.NORMAL,
                                            style=Pango.Style.ITALIC)

        self.tag_bold = buffer.create_tag(self.TAG_NAME_BOLD,
                                          weight=Pango.Weight.BOLD,
                                          style=Pango.Style.NORMAL)

        self.tag_bold_italic = buffer.create_tag(self.TAG_NAME_BOLD_ITALIC,
                                                 weight=Pango.Weight.BOLD,
                                                 style=Pango.Style.ITALIC)

        self.tag_strikethrough = buffer.create_tag(self.TAG_NAME_STRIKETHROUGH,
                                                   strikethrough=True)

        self.tag_center = buffer.create_tag(self.TAG_NAME_CENTER,
                                            justification=Gtk.Justification.CENTER)

        self.tag_wrap_none = buffer.create_tag(self.TAG_NAME_WRAP_NONE,
                                               wrap_mode=Gtk.WrapMode.NONE,
                                               pixels_above_lines=0,
                                               pixels_below_lines=0)

        self.tag_plain_text = buffer.create_tag(self.TAG_NAME_PLAIN_TEXT,
                                                weight=Pango.Weight.NORMAL,
                                                style=Pango.Style.NORMAL,
                                                strikethrough=False,
                                                justification=Gtk.Justification.LEFT)

        self.tag_gray_text = buffer.create_tag(self.TAG_NAME_GRAY_TEXT,
                                               foreground='gray',
                                               weight=Pango.Weight.NORMAL,
                                               style=Pango.Style.NORMAL)

        self.tag_code_text = buffer.create_tag(self.TAG_NAME_CODE_TEXT,
                                               weight=Pango.Weight.NORMAL,
                                               style=Pango.Style.NORMAL,
                                               strikethrough=False)

        self.tag_code_block = buffer.create_tag(self.TAG_NAME_CODE_BLOCK,
                                                weight=Pango.Weight.NORMAL,
                                                style=Pango.Style.NORMAL,
                                                strikethrough=False,
                                                indent=self.get_margin_indent(0, 1)[1])

        self.tags_markup = {
            self.TAG_NAME_ITALIC: lambda args: self.tag_italic,
            self.TAG_NAME_BOLD: lambda args: self.tag_bold,
            self.TAG_NAME_BOLD_ITALIC: lambda args: self.tag_bold_italic,
            self.TAG_NAME_STRIKETHROUGH: lambda args: self.tag_strikethrough,
            self.TAG_NAME_CENTER: lambda args: self.tag_center,
            self.TAG_NAME_WRAP_NONE: lambda args: self.tag_wrap_none,
            self.TAG_NAME_PLAIN_TEXT: lambda args: self.tag_plain_text,
            self.TAG_NAME_GRAY_TEXT: lambda args: self.tag_gray_text,
            self.TAG_NAME_CODE_TEXT: lambda args: self.tag_code_text,
            self.TAG_NAME_CODE_BLOCK: lambda args: self.tag_code_block,
            self.TAG_NAME_MARGIN_INDENT: lambda args: self.get_margin_indent_tag(
                *args)
        }

        # Focus mode.
        self.tag_unfocused_text = buffer.create_tag(self.TAG_NAME_UNFOCUSED_TEXT,
                                                    foreground='gray',
                                                    weight=Pango.Weight.NORMAL,
                                                    style=Pango.Style.NORMAL)

        # Margin and indents.
        # A baseline margin is set to allow negative offsets for formatting
        # headers, lists, etc.
        self.tags_margins_indents = {}
        self.baseline_margin = 0
        self.char_width = 0
        self.update_margins_indents()

        # Style.
        self.on_style_updated()

        # Worker process to handle parsing.
        self.parsing = False
        self.apply_pending = False
        self.parent_conn, child_conn = Pipe()
        Process(target=self.parse, args=(child_conn,), daemon=True).start()
        GLib.io_add_watch(
            self.parent_conn.fileno(),
            GLib.PRIORITY_DEFAULT,
            GLib.IO_IN,
            self.on_parsed)

    def on_style_updated(self, *_):
        style_context = self.text_view.get_style_context()
        (found, color) = style_context.lookup_color('code_bg_color')
        if not found:
            (_, color) = style_context.lookup_color('background_color')
        self.tag_code_text.set_property("background", color.to_string())
        self.tag_code_block.set_property(
            "paragraph-background", color.to_string())

    def apply(self):
        """Applies markup, parsing it in a worker process
        if the text has changed.

        In case parsing is already running, it will re-apply once it finishes.
        This ensure that the pipe doesn't fill (and block) if multiple requests
        are made in quick succession."""

        if not self.parsing:
            self.parsing = True
            self.apply_pending = False

            text = self.text_buffer.get_slice(
                self.text_buffer.get_start_iter(),
                self.text_buffer.get_end_iter(),
                False)
            if text != self.marked_up_text:
                self.parent_conn.send(text)
            else:
                self.do_apply(text)
        else:
            self.apply_pending = True

    def parse(self, child_conn):
        """Parses markup in a worker process."""

        while True:
            while True:
                try:
                    text = child_conn.recv()
                    if not child_conn.poll():
                        break
                except EOFError:
                    child_conn.close()
                    return

            # List of tuples in the form (tag_name, tag_args, tag_start,
            # tag_end).
            result = []

            # Find:
            # - "_italic_" (italic)
            # - "**bold**" (bold)
            # - "***bolditalic***" (bold/italic)
            # - "~~strikethrough~~" (strikethrough)
            # - "`code`" (colorize)
            # - "$math$" (colorize)
            # - "---" table (wrap/pixels)
            regexps = (
                (ITALIC_ASTERISK, self.TAG_NAME_ITALIC),
                (ITALIC_UNDERSCORE, self.TAG_NAME_ITALIC),
                (BOLD, self.TAG_NAME_BOLD),
                (BOLD_ITALIC, self.TAG_NAME_BOLD_ITALIC),
                (STRIKETHROUGH, self.TAG_NAME_STRIKETHROUGH),
                (CODE, self.TAG_NAME_CODE_TEXT),
                (MATH, self.TAG_NAME_CODE_TEXT),
                (TABLE, self.TAG_NAME_WRAP_NONE)
            )
            for regexp, tag_name in regexps:
                matches = re.finditer(regexp, text)
                for match in matches:
                    result.append((tag_name, (), match.start(), match.end()))

            # Find:
            # - "[description](url)" (gray out)
            # - "![description](image_url)" (gray out)
            regexps = (
                (LINK, self.TAG_NAME_GRAY_TEXT),
                (IMAGE, self.TAG_NAME_GRAY_TEXT)
            )
            for regexp, tag_name in regexps:
                matches = re.finditer(regexp, text)
                for match in matches:
                    result.append(
                        (tag_name, (), match.start(), match.start("text")))
                    result.append(
                        (tag_name, (), match.end("text"), match.end()))

            # Find "<url>" links (gray out).
            matches = re.finditer(LINK_ALT, text)
            for match in matches:
                result.append((
                    self.TAG_NAME_GRAY_TEXT,
                    (), match.start("text"),
                    match.end("text")))

            # Find "---" horizontal rule (center).
            matches = re.finditer(HORIZONTAL_RULE, text)
            for match in matches:
                result.append((
                    self.TAG_NAME_CENTER,
                    (), match.start("symbols"),
                    match.end("symbols")))

            # Find "* list" (offset).
            matches = re.finditer(LIST, text)
            for match in matches:
                # Lists use character+space (eg. "* ").
                length = 2
                nest = len(match.group("indent").replace("    ", "\t"))
                margin = -length - 2 * nest
                indent = -length - 2 * length * nest
                result.append((
                    self.TAG_NAME_MARGIN_INDENT,
                    (margin, indent),
                    match.start("content"),
                    match.end("content")
                ))

            # Find "1. ordered list" (offset).
            matches = re.finditer(ORDERED_LIST, text)
            for match in matches:
                # Ordered lists use numbers/letters+dot/parens+space
                # (eg. "123. ").
                length = len(match.group("prefix")) + 1
                nest = len(match.group("indent").replace("    ", "\t"))
                margin = -length - 2 * nest
                indent = -length - 2 * length * nest
                result.append((
                    self.TAG_NAME_MARGIN_INDENT,
                    (margin, indent),
                    match.start("content"),
                    match.end("content")
                ))

            # Find "> blockquote" (offset).
            matches = re.finditer(BLOCK_QUOTE, text)
            for match in matches:
                result.append((self.TAG_NAME_MARGIN_INDENT,
                               (2, -2), match.start(), match.end()))

            # Find "# Header" (offset+bold).
            matches = re.finditer(HEADER, text)
            for match in matches:
                margin = -len(match.group("level")) - 1
                result.append((
                    self.TAG_NAME_MARGIN_INDENT, (margin, 0),
                    match.start(), match.end()))
                result.append(
                    (self.TAG_NAME_BOLD, (), match.start(), match.end()))

            # Find "=======" header underline (bold).
            matches = re.finditer(HEADER_UNDER, text)
            for match in matches:
                result.append(
                    (self.TAG_NAME_BOLD, (), match.start(), match.end()))

            # Find "```" code block tag (offset + colorize paragraph).
            matches = re.finditer(markup_regex.CODE_BLOCK, text)
            for match in matches:
                result.append((
                    self.TAG_NAME_CODE_BLOCK, (),
                    match.start("block"), match.end("block")))

            # Send parsed data back.
            child_conn.send((text, result))

    def on_parsed(self, _source, _condition):
        """Reads the parsing result from the pipe
        and triggers any pending apply."""

        self.parsing = False
        if self.apply_pending:
            self.apply()  # self.apply clears the apply pending flag.

        try:
            if self.parent_conn.poll():
                self.do_apply(*self.parent_conn.recv())
            return True
        except EOFError:
            return False

    def do_apply(self, original_text, result=[]):
        """Applies the result of parsing if the current text
        matches the original text."""

        buffer = self.text_buffer
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = self.text_buffer.get_slice(start, end, False)

        # Apply markup tags.
        if text == original_text and text != self.marked_up_text:
            buffer.remove_tag(self.tag_italic, start, end)
            buffer.remove_tag(self.tag_bold, start, end)
            buffer.remove_tag(self.tag_bold_italic, start, end)
            buffer.remove_tag(self.tag_strikethrough, start, end)
            buffer.remove_tag(self.tag_center, start, end)
            buffer.remove_tag(self.tag_plain_text, start, end)
            buffer.remove_tag(self.tag_gray_text, start, end)
            buffer.remove_tag(self.tag_code_text, start, end)
            buffer.remove_tag(self.tag_code_block, start, end)
            buffer.remove_tag(self.tag_wrap_none, start, end)
            for tag in self.tags_margins_indents.values():
                buffer.remove_tag(tag, start, end)

            for tag_name, tag_args, tag_start, tag_end in result:
                buffer.apply_tag(
                    self.tags_markup[tag_name](tag_args),
                    buffer.get_iter_at_offset(tag_start),
                    buffer.get_iter_at_offset(tag_end))

        # Apply focus mode tag (grey out before/after current sentence).
        buffer.remove_tag(self.tag_unfocused_text, start, end)
        if self.text_view.focus_mode:
            cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
            start_sentence = cursor_iter.copy()
            if not start_sentence.starts_sentence():
                start_sentence.backward_sentence_start()
            end_sentence = cursor_iter.copy()
            if not end_sentence.ends_sentence():
                end_sentence.forward_sentence_end()
            buffer.apply_tag(self.tag_unfocused_text, start, start_sentence)
            buffer.apply_tag(self.tag_unfocused_text, end_sentence, end)

    # Margin and indent are cumulative. They differ in two ways:
    # * Margin is always in the beginning,
    # which means it effectively only affects the first line
    # of multi-line text. Indent is applied to every line.
    # * Margin level can be negative, as a baseline margin exists
    # from which it can be subtracted.
    # Indent is always positive, or 0.
    def get_margin_indent_tag(self, margin_level, indent_level):
        level = (margin_level, indent_level)
        if level not in self.tags_margins_indents:
            margin, indent = self.get_margin_indent(margin_level, indent_level)
            tag = self.text_buffer.create_tag(
                "margin_indent_{}_{}".format(margin_level, indent_level),
                left_margin=margin, indent=indent)
            self.tags_margins_indents[level] = tag
            return tag
        else:
            return self.tags_margins_indents[level]

    def get_margin_indent(self, margin_level, indent_level,
                          baseline_margin=None, char_width=None):
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
        for level, tag in self.tags_margins_indents.items():
            margin, indent = self.get_margin_indent(
                *level, baseline_margin, char_width)
            tag.set_properties(left_margin=margin, indent=indent)

    def stop(self, *_):
        self.parent_conn.close()
