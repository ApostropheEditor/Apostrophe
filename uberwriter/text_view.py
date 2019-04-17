import gi

from uberwriter.inline_preview import InlinePreview
from uberwriter.text_view_format_inserter import FormatInserter
from uberwriter.text_view_markup_handler import MarkupHandler
from uberwriter.text_view_undo_redo_handler import UndoRedoHandler
from uberwriter.text_view_drag_drop_handler import DragDropHandler, TARGET_URI, TARGET_TEXT
from uberwriter.scroller import Scroller

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib

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

    def __init__(self):
        super().__init__()

        # Appearance
        self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.set_pixels_above_lines(4)
        self.set_pixels_below_lines(4)
        self.set_pixels_inside_wrap(8)
        self.get_style_context().add_class('uberwriter-editor')

        # General behavior
        self.get_buffer().connect('changed', self.on_text_changed)
        self.connect('size-allocate', self.on_size_allocate)

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
        self.get_buffer().connect('mark-set', self.on_mark_set)

        # Focus mode
        self.focus_mode = False
        self.original_top_margin = self.props.top_margin
        self.original_bottom_margin = self.props.bottom_margin
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

    def on_text_changed(self, *_):
        self.markup.apply()
        GLib.idle_add(self.scroll_to)

    def on_size_allocate(self, *_):
        self.update_vertical_margin()
        self.markup.update_margins_indents()

    def set_focus_mode(self, focus_mode):
        """Toggle focus mode.

        When in focus mode, the cursor sits in the middle of the text view,
        and the surrounding text is greyed out."""

        self.focus_mode = focus_mode
        self.update_vertical_margin()
        self.markup.apply()
        self.scroll_to()

    def update_vertical_margin(self):
        if self.focus_mode:
            height = self.get_allocation().height
            self.props.top_margin = height / 2
            self.props.bottom_margin = height / 2
        else:
            self.props.top_margin = self.original_top_margin
            self.props.bottom_margin = self.original_bottom_margin

    def on_button_release_event(self, _widget, _event):
        if self.focus_mode:
            self.markup.apply()
        return False

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

    def scroll_to(self, mark=None):
        """Scrolls if needed to ensure mark is visible.

        If mark is unspecified, the cursor is used."""

        margin = 80
        scrolled_window = self.get_ancestor(Gtk.ScrolledWindow.__gtype__)
        if not scrolled_window:
            return
        va = scrolled_window.get_vadjustment()
        if va.props.page_size < margin * 2:
            return

        text_buffer = self.get_buffer()
        if mark:
            mark_iter = text_buffer.get_iter_at_mark(mark)
        else:
            mark_iter = text_buffer.get_iter_at_mark(text_buffer.get_insert())
        mark_rect = self.get_iter_location(mark_iter)

        pos_y = mark_rect.y + mark_rect.height + self.props.top_margin
        pos = pos_y - va.props.value
        target_pos = None
        if self.focus_mode:
            if pos != (va.props.page_size * 0.5):
                target_pos = pos_y - (va.props.page_size * 0.5)
        elif pos > va.props.page_size - margin:
            target_pos = pos_y - va.props.page_size + margin
        elif pos < margin:
            target_pos = pos_y - margin

        if self.scroller and self.scroller.is_started:
            self.scroller.end()
        if target_pos:
            self.scroller = Scroller(scrolled_window, va.props.value, target_pos)
            self.scroller.start()

    def on_mark_set(self, _text_buffer, _location, mark, _data=None):
        if mark.get_name() == 'insert':
            self.markup.apply()
            if self.focus_mode:
                self.scroll_to(mark)
        elif mark.get_name() == 'gtk_drag_target':
            self.scroll_to(mark)
        return True
