from contextlib import contextmanager
from itertools import cycle
import re
import gi

from apostrophe.helpers import user_action
gi.require_version('Gtk', '4.0')

from gi.repository import GObject, Gtk
from apostrophe.markup_regex import LIST, ORDERED_LIST

class ApostropheTextBuffer(Gtk.TextBuffer):
    __gtype_name__ = "ApostropheTextBuffer"

    __gsignals__ = {
        'attempted-hemingway': (GObject.SignalFlags.ACTION, None, ()),
    }

    hemingway_mode = GObject.Property(type=bool, default=False)

    def __init__(self):
        super().__init__()

    @contextmanager
    def _temp_disable_hemingway(self):
        ''' Disables hemingway mode before an action and enables it right away
        '''
        hemingway_cache = self.hemingway_mode
        if hemingway_cache:
            self.hemingway_mode = False
        yield self
        self.hemingway_mode = hemingway_cache

    def get_current_sentence_bounds(self):
        cursor_iter = self.get_iter_at_mark(self.get_insert())
        start_sentence = cursor_iter.copy()
        if not start_sentence.starts_sentence():
            start_sentence.backward_sentence_start()
        end_sentence = cursor_iter.copy()
        if not end_sentence.ends_sentence():
            end_sentence.forward_sentence_end()

        return (start_sentence, end_sentence)

    def get_current_line_bounds(self):
        # backward_line() doesn't seem to work as expected
        # so we just find the end of the line and backward the number of characters
        # that line has
        cursor_iter = self.get_iter_at_mark(self.get_insert())
        end_line = cursor_iter.copy()
        if not end_line.ends_line():
            end_line.forward_line()
        start_line = end_line.copy()
        start_line.backward_chars(end_line.get_line_offset())

        return (start_line, end_line)

    def _indent(self):
        '''Takes over tab insertions.
           If the insertion happens within a list, 
           it nicely handles it, otherwise inserts a plain \t'''
        start_line, end_line = self.get_current_line_bounds()
        current_sentence = self.get_text(start_line, end_line, True)
        text = '\t'

        # Indent unordered lists
        match = re.fullmatch(LIST, current_sentence)
        if match and not match.group("text"):
            symbols = cycle(['-', '*', '+'])
            for i in range(3):
                if next(symbols) == match.group("symbol"):
                    break
            next_symbol = next(symbols)
            indent = "\t" if "\t" in match.group("indent") else "    " + match.group("indent")

            with self._temp_disable_hemingway():
                self.delete(start_line, end_line)
            text = indent + next_symbol + " "

        # Indent ordered lists
        match = re.fullmatch(ORDERED_LIST, current_sentence)
        if match and not match.group("text"):
            indent = "\t" if "\t" in match.group("indent") else "    " + match.group("indent")

            with self._temp_disable_hemingway():
                self.delete(start_line, end_line)
            text = indent + "1" + match.group("delimiter") + " "

        position = self.get_iter_at_mark(self.get_insert())
        Gtk.TextBuffer.do_insert_text(self, position, text, -1)

    def _unindent(self, *args):
        if self.hemingway_mode:
            self.emit("attempted-hemingway")
            return

        start_line, end_line = self.get_current_line_bounds()
        current_sentence = self.get_text(start_line, end_line, True)

        # Unindent unordered lists
        match = re.fullmatch(LIST, current_sentence)
        if match:
            symbols = cycle(['+', '*', '-'])
            for i in range(3):
                if next(symbols) == match.group("symbol"):
                    break
            next_symbol = next(symbols)
            indent = match.group("indent").removesuffix("\t").removesuffix("    ")

            self.delete(start_line, end_line)
            text = indent + next_symbol + " "
            if match.group("text"):
                text += match.group("text")

            position = self.get_iter_at_mark(self.get_insert())
            Gtk.TextBuffer.do_insert_text(self, position, text, -1)

        # Unindent regular tabs
        else:
            pen_iter = self.get_end_iter()
            pen_iter.backward_char()
            end_iter = self.get_end_iter()

            if pen_iter.get_char() == "\t":
                with user_action(self):
                    self.delete(pen_iter, end_iter)

    def _autocomplete_lists(self):
        start_line, end_line = self.get_current_line_bounds()
        current_sentence = self.get_text(start_line, end_line, True)

        text = "\n"

        # ORDERED LISTS
        match = re.match(ORDERED_LIST, current_sentence)
        if match:
            if match.group("text"):
                if match.group("number"):
                    next_prefix = match.group("indent") +\
                                str(int(match.group("number")) + 1) +\
                                match.group("delimiter") +\
                                " "
                    text += next_prefix
            # if there's no text when the user hits enter we exit the list mode
            else:
                with self._temp_disable_hemingway():
                    self.delete(start_line, end_line)
                position = self.get_iter_at_mark(self.get_insert())

        # UNORDERED LISTS
        match = re.match(LIST, current_sentence)
        if match:
            if match.group("text"):
                next_prefix = match.group("indent") + match.group("symbol") + " "
                text += next_prefix
            # if there's no text when the user hits enter we exit the list mode
            else:
                with self._temp_disable_hemingway():
                    self.delete(start_line, end_line)
                position = self.get_iter_at_mark(self.get_insert())

        position = self.get_iter_at_mark(self.get_insert())
        Gtk.TextBuffer.do_insert_text(self, position, text, -1)

    def do_insert_text(self, position, text, length):
        if self.hemingway_mode and self.get_has_selection():
            return

        move_cursor = None
        match text:
            case "\n":
                self._autocomplete_lists()
                return
            case "\t":
                self._indent()
                return
            case ("(" | "[" | "{" | '"' | "'" | "<") as x:
                pairs = {
                    "(" : ")",
                    "[" : "]",
                    "{" : "}",
                    '"' : '"',
                    "'" : "'",
                    "<" : ">"
                }

                #is the next character whitespace?
                if self.get_iter_at_mark(self.get_insert()).get_char().isspace() or\
                   self.get_iter_at_mark(self.get_insert()).is_end():
                    text += pairs[x]
                    move_cursor = -1

        Gtk.TextBuffer.do_insert_text(self, position, text, -1)
        if move_cursor:
            cursor_iter = self.get_iter_at_mark(self.get_insert())
            cursor_iter.forward_cursor_positions(move_cursor)
            self.place_cursor(cursor_iter)

    def do_delete_range(self, start, end):
        if self.hemingway_mode:
            self.emit("attempted-hemingway")
        else:
            Gtk.TextBuffer.do_delete_range(self, start, end)