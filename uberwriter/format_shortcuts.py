# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
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
# END LICENSE


from gettext import gettext as _

from uberwriter.markup_buffer import MarkupBuffer


class FormatShortcuts():
    """Manage the insertion of formatting for insert them using shortcuts
    """


    def __init__(self, textbuffer, texteditor):
        self.text_buffer = textbuffer
        self.text_editor = texteditor
        self.regex = MarkupBuffer.regex

    def rule(self):
        """insert ruler at cursor
        """

        self.text_buffer.insert_at_cursor("\n\n-------\n")
        self.text_editor.scroll_mark_onscreen(self.text_buffer.get_insert())

    def bold(self):
        """set selected text as bold
        """

        self.apply_format("**")

    def italic(self):
        """set selected text as italic
        """
        self.apply_format("*")

    def strikeout(self):
        """set selected text as stricked out
        """
        self.apply_format("~~")

    def apply_format(self, wrap="*"):
        """apply the given wrap to a selected text, or insert a helper text wraped
           if nothing is selected

        Keyword Arguments:
            wrap {str} -- [the format mark] (default: {"*"})
        """

        if self.text_buffer.get_has_selection():
            # Find current highlighting
            (start, end) = self.text_buffer.get_selection_bounds()
            moved = False
            if (start.get_offset() >= len(wrap) and
                    end.get_offset() <= self.text_buffer.get_char_count() - len(wrap)):
                moved = True
                ext_start = start.copy()
                ext_start.backward_chars(len(wrap))
                ext_end = end.copy()
                ext_end.forward_chars(len(wrap))
                text = self.text_buffer.get_text(ext_start, ext_end, True)
            else:
                text = self.text_buffer.get_text(start, end, True)

            if moved and text.startswith(wrap) and text.endswith(wrap):
                text = text[len(wrap):-len(wrap)]
                new_text = text
                self.text_buffer.delete(ext_start, ext_end)
                move_back = 0
            else:
                if moved:
                    text = text[len(wrap):-len(wrap)]
                new_text = text.lstrip().rstrip()
                text = text.replace(new_text, wrap + new_text + wrap)

                self.text_buffer.delete(start, end)
                move_back = len(wrap)

            self.text_buffer.insert_at_cursor(text)
            text_length = len(new_text)

        else:
            helptext = ""
            if wrap == "*":
                helptext = _("emphasized text")
            elif wrap == "**":
                helptext = _("strong text")
            elif wrap == "~~":
                helptext = _("striked out text")

            self.text_buffer.insert_at_cursor(wrap + helptext + wrap)
            text_length = len(helptext)
            move_back = len(wrap)

        cursor_mark = self.text_buffer.get_insert()
        cursor_iter = self.text_buffer.get_iter_at_mark(cursor_mark)
        cursor_iter.backward_chars(move_back)
        self.text_buffer.move_mark_by_name('selection_bound', cursor_iter)
        cursor_iter.backward_chars(text_length)
        self.text_buffer.move_mark_by_name('insert', cursor_iter)

    def unordered_list_item(self):
        """insert unordered list items or mark a selection as
           an item in an unordered list
        """

        helptext = _("List item")
        text_length = len(helptext)
        move_back = 0
        if self.text_buffer.get_has_selection():
            (start, end) = self.text_buffer.get_selection_bounds()
            if start.starts_line():
                text = self.text_buffer.get_text(start, end, False)
                if text.startswith(("- ", "* ", "+ ")):
                    delete_end = start.forward_chars(2)
                    self.text_buffer.delete(start, delete_end)
                else:
                    self.text_buffer.insert(start, "- ")
        else:
            move_back = 0
            cursor_mark = self.text_buffer.get_insert()
            cursor_iter = self.text_buffer.get_iter_at_mark(cursor_mark)

            start_ext = cursor_iter.copy()
            start_ext.backward_lines(3)
            text = self.text_buffer.get_text(cursor_iter, start_ext, False)
            lines = text.splitlines()

            for line in reversed(lines):
                if line and line.startswith(("- ", "* ", "+ ")):
                    if cursor_iter.starts_line():
                        self.text_buffer.insert_at_cursor(line[:2] + helptext)
                    else:
                        self.text_buffer.insert_at_cursor(
                            "\n" + line[:2] + helptext)
                    break
                else:
                    if not lines[-1] and not lines[-2]:
                        self.text_buffer.insert_at_cursor("- " + helptext)
                    elif not lines[-1]:
                        if cursor_iter.starts_line():
                            self.text_buffer.insert_at_cursor("- " + helptext)
                        else:
                            self.text_buffer.insert_at_cursor("\n- " + helptext)
                    else:
                        self.text_buffer.insert_at_cursor("\n\n- " + helptext)
                    break

            self.select_edit(move_back, text_length)

    def ordered_list_item(self):
        # TODO: implement ordered lists
        pass

    def select_edit(self, move_back, text_length):
        cursor_mark = self.text_buffer.get_insert()
        cursor_iter = self.text_buffer.get_iter_at_mark(cursor_mark)
        cursor_iter.backward_chars(move_back)
        self.text_buffer.move_mark_by_name('selection_bound', cursor_iter)
        cursor_iter.backward_chars(text_length)
        self.text_buffer.move_mark_by_name('insert', cursor_iter)
        self.text_editor.scroll_mark_onscreen(self.text_buffer.get_insert())

    def heading(self):
        """insert heading at cursor position or set selected text as one
        """
        helptext = _("Heading")
        if self.text_buffer.get_has_selection():
            (start, end) = self.text_buffer.get_selection_bounds()
            text = self.text_buffer.get_text(start, end, False)
            self.text_buffer.delete(start, end)
        else:
            text = helptext

        self.text_buffer.insert_at_cursor("#" + " " + text)
        self.select_edit(0, len(text))
