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


    def do_insert_text(self, position, text, length):
        if self.hemingway_mode and self.get_has_selection():
            return


        Gtk.TextBuffer.do_insert_text(self, position, text, len(text))

    def do_delete_range(self, start, end):
        if self.hemingway_mode:
            self.emit("attempted-hemingway")
        else:
            Gtk.TextBuffer.do_delete_range(self, start, end)