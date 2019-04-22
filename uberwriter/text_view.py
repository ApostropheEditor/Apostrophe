import gi

from uberwriter.inline_preview import InlinePreview
from uberwriter.text_view_format_inserter import FormatInserter
from uberwriter.text_view_markup_handler import MarkupHandler
from uberwriter.text_view_scroller import TextViewScroller
from uberwriter.text_view_undo_redo_handler import UndoRedoHandler
from uberwriter.text_view_drag_drop_handler import DragDropHandler, TARGET_URI, TARGET_TEXT

gi.require_version('Gtk', '3.0')
gi.require_version('Gspell', '1')
from gi.repository import Gtk, Gdk, GObject, GLib, Gspell

import logging

LOGGER = logging.getLogger('uberwriter')


class TextView(Gtk.TextView):
    """UberwriterTextView encapsulates all the features around the editor.

    It combines the following:
    - Undo / redo (via TextBufferUndoRedoHandler)
    - Format shortcuts (via TextBufferShortcutInserter)
    - Markup (via TextBufferMarkupHandler)
    - Preview popover (via TextBufferMarkupHandler)
    - Drag and drop (via TextViewDragDropHandler)
    - Scrolling (via TextViewScroller)
    - The various modes supported by UberWriter (eg. Focus Mode, Hemingway Mode)
    """

    __gsignals__ = {
        'insert-italic': (GObject.SignalFlags.ACTION, None, ()),
        'insert-bold': (GObject.SignalFlags.ACTION, None, ()),
        'insert-hrule': (GObject.SignalFlags.ACTION, None, ()),
        'insert-listitem': (GObject.SignalFlags.ACTION, None, ()),
        'insert-header': (GObject.SignalFlags.ACTION, None, ()),
        'insert-strikethrough': (GObject.SignalFlags.ACTION, None, ()),
        'undo': (GObject.SignalFlags.ACTION, None, ()),
        'redo': (GObject.SignalFlags.ACTION, None, ())
    }

    font_sizes = [18, 17, 16, 15, 14]  # Must match CSS selectors in gtk/base.css

    def __init__(self, line_chars):
        super().__init__()

        # Appearance
        self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.set_pixels_above_lines(4)
        self.set_pixels_below_lines(4)
        self.set_pixels_inside_wrap(8)
        self.get_style_context().add_class('uberwriter-editor')

        # Text sizing
        self.props.halign = Gtk.Align.FILL
        self.line_chars = line_chars
        self.font_size = 16
        self.get_style_context().add_class('size16')

        # General behavior
        self.connect('size-allocate', self.on_size_allocate)
        self.get_buffer().connect('changed', self.on_text_changed)

        # Spell checking
        self.gspell_view = Gspell.TextView.get_from_gtk_text_view(self)
        self.gspell_view.basic_setup()

        # Undo / redo
        self.undo_redo = UndoRedoHandler()
        self.get_buffer().connect('insert-text', self.undo_redo.on_insert_text)
        self.get_buffer().connect('delete-range', self.undo_redo.on_delete_range)
        self.connect('undo', self.undo_redo.undo)
        self.connect('redo', self.undo_redo.redo)

        # Format shortcuts
        self.shortcut = FormatInserter()
        self.connect('insert-italic', self.shortcut.insert_italic)
        self.connect('insert-bold', self.shortcut.insert_bold)
        self.connect('insert-strikethrough', self.shortcut.insert_strikethrough)
        self.connect('insert-hrule', self.shortcut.insert_horizontal_rule)
        self.connect('insert-listitem', self.shortcut.insert_list_item)
        self.connect('insert-header', self.shortcut.insert_header)

        # Markup
        self.markup = MarkupHandler(self)
        self.connect('style-updated', self.markup.on_style_updated)

        # Preview popover
        self.preview_popover = InlinePreview(self)

        # Drag and drop
        self.drag_drop = DragDropHandler(self, TARGET_URI, TARGET_TEXT)

        # Scrolling
        self.scroller = None
        self.connect('parent-set', self.on_parent_set)
        self.get_buffer().connect('mark-set', self.on_mark_set)

        # Focus mode
        self.focus_mode = False
        self.connect('button-release-event', self.on_button_release_event)

        # Hemingway mode
        self.hemingway_mode = False
        self.connect('key-press-event', self.on_key_press_event)

    def get_text(self):
        text_buffer = self.get_buffer()
        start_iter = text_buffer.get_start_iter()
        end_iter = text_buffer.get_end_iter()
        return text_buffer.get_text(start_iter, end_iter, False)

    def set_text(self, text):
        text_buffer = self.get_buffer()
        text_buffer.set_text(text)

    def get_scroll_scale(self):
        return self.scroller.get_scroll_scale() if self.scroller else 0

    def set_scroll_scale(self, scale):
        if self.scroller:
            self.scroller.set_scroll_scale(scale)

    def on_size_allocate(self, *_):
        self.update_horizontal_margin()
        self.update_vertical_margin()
        self.markup.update_margins_indents()

    def on_text_changed(self, *_):
        self.markup.apply()
        self.smooth_scroll_to()

    def on_parent_set(self, *_):
        parent = self.get_parent()
        if parent:
            parent.set_size_request(self.get_min_width(), 500)
            self.scroller = TextViewScroller(self, parent)
        else:
            self.scroller = None

    def on_mark_set(self, _text_buffer, _location, mark, _data=None):
        if mark.get_name() == 'insert':
            self.markup.apply()
            self.smooth_scroll_to(mark)
        elif mark.get_name() == 'gtk_drag_target':
            self.smooth_scroll_to(mark)
        return True

    def on_button_release_event(self, _widget, _event):
        if self.focus_mode:
            self.markup.apply()
        return False

    def set_focus_mode(self, focus_mode):
        """Toggle focus mode.

        When in focus mode, the cursor sits in the middle of the text view,
        and the surrounding text is greyed out."""

        self.focus_mode = focus_mode
        self.gspell_view.set_inline_spell_checking(not focus_mode)
        self.update_vertical_margin()
        self.markup.apply()
        self.smooth_scroll_to()

    def update_horizontal_margin(self):
        width = self.get_allocation().width

        # Ensure the appropriate font size is being used
        for font_size in self.font_sizes:
            if width >= self.get_min_width(font_size) or font_size == self.font_sizes[-1]:
                if font_size != self.font_size:
                    self.font_size = font_size
                    for fs in self.font_sizes:
                        self.get_style_context().remove_class("size{}".format(fs))
                    self.get_style_context().add_class("size{}".format(font_size))
                break

        # Apply margin with the remaining space to allow for markup
        line_width = (self.line_chars + 1) * int(self.get_char_width(self.font_size)) - 1
        horizontal_margin = (width - line_width) / 2
        self.props.left_margin = horizontal_margin
        self.props.right_margin = horizontal_margin

    def update_vertical_margin(self):
        if self.focus_mode:
            height = self.get_allocation().height
            self.props.top_margin = height / 2
            self.props.bottom_margin = height / 2
        else:
            self.props.top_margin = 80
            self.props.bottom_margin = 64

    def set_hemingway_mode(self, hemingway_mode):
        """Toggle hemingway mode.

        When in hemingway mode, the backspace and delete keys are ignored."""

        self.hemingway_mode = hemingway_mode

    def on_key_press_event(self, _widget, event):
        if self.hemingway_mode:
            return event.keyval == Gdk.KEY_BackSpace or event.keyval == Gdk.KEY_Delete
        else:
            return False

    def clear(self):
        """Clear text and undo history"""

        self.get_buffer().set_text('')
        self.undo_redo.clear()

    def smooth_scroll_to(self, mark=None):
        """Scrolls if needed to ensure mark is visible.

        If mark is unspecified, the cursor is used."""

        if self.scroller is None:
            return
        if mark is None:
            mark = self.get_buffer().get_insert()
        GLib.idle_add(self.scroller.smooth_scroll_to_mark, mark, self.focus_mode)

    def get_min_width(self, font_size=None):
        """Returns the minimum width of this text view."""

        if font_size is None:
            font_size = self.font_sizes[-1]
        return (self.line_chars + self.get_pad_chars(font_size) + 1) \
            * self.get_char_width(font_size) - 1

    def get_pad_chars(self, font_size):
        """Returns the amount of character padding for font_size.

        Markup can use up to 7 in normal conditions."""

        return 8 * (1 + font_size - self.font_sizes[-1])

    @staticmethod
    def get_char_width(font_size):
        """Returns the font width for a given size. Note: specific to Fira Mono!"""

        return font_size * 1 / 1.6
