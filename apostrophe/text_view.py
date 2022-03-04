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

import gi

from apostrophe.helpers import user_action
from apostrophe.inline_preview import InlinePreview
from apostrophe.text_view_drag_drop_handler import DragDropHandler,\
                                                   TARGET_URI, TARGET_TEXT
from apostrophe.text_view_format_inserter import FormatInserter
from apostrophe.text_view_markup_handler import MarkupHandler
from apostrophe.text_view_scroller import TextViewScroller
from apostrophe.text_view_undo_redo_handler import UndoRedoHandler

gi.require_version('Gtk', '3.0')
gi.require_version('Gspell', '1')
from gi.repository import Gtk, Gdk, GObject, GLib, Gspell

import logging

LOGGER = logging.getLogger('apostrophe')

DEFAULT_DPI = 98304

@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/TextView.ui')
class ApostropheTextView(Gtk.TextView):
    """ApostropheTextView encapsulates all the features around the editor.

    It combines the following:
    - Undo / redo (via TextBufferUndoRedoHandler)
    - Format shortcuts (via TextBufferShortcutInserter)
    - Markup (via TextBufferMarkupHandler)
    - Preview popover (via TextBufferMarkupHandler)
    - Drag and drop (via TextViewDragDropHandler)
    - Scrolling (via TextViewScroller)
    - The various modes supported by Apostrophe (e. Focus Mode, Hemingway Mode)
    """

    __gtype_name__ = "ApostropheTextView"

    __gsignals__ = {
        'insert-italic': (GObject.SignalFlags.ACTION, None, ()),
        'insert-bold': (GObject.SignalFlags.ACTION, None, ()),
        'insert-hrule': (GObject.SignalFlags.ACTION, None, ()),
        'insert-listitem': (GObject.SignalFlags.ACTION, None, ()),
        'insert-header': (GObject.SignalFlags.ACTION, None, ()),
        'insert-strikethrough': (GObject.SignalFlags.ACTION, None, ()),
        'undo': (GObject.SignalFlags.ACTION, None, ()),
        'redo': (GObject.SignalFlags.ACTION, None, ()),
        'scroll-scale-changed': (GObject.SIGNAL_RUN_LAST, None, (float,)),
    }


    bigger_text = GObject.Property(type=bool, default=False)
    hemingway_mode = GObject.Property(type=bool, default=False)
    focus_mode = GObject.Property(type=bool, default=False)
    font_size = GObject.Property(type=int, default=16)
    line_chars = GObject.Property(type=int, default=66)
    spellcheck = GObject.Property(type=bool, default=True)

    scroller = None

    _scroll_scale = 0

    @GObject.Property(type=float, default=0)
    def scroll_scale(self):
        return self.scroller.get_scroll_scale() if self.scroller else 0

    @scroll_scale.setter
    def scroll_scale(self, scale):
        if self.scroller:
            self.scroller.set_scroll_scale(scale)

    def __init__(self):
        super().__init__()

        # Spell checking
        self.gspell_view = Gspell.TextView.get_from_gtk_text_view(self)
        self.gspell_view.basic_setup()

        # Undo / redo
        self.undo_redo = UndoRedoHandler()
        self.get_buffer().connect('begin-user-action',
                                  self.undo_redo.on_begin_user_action)
        self.get_buffer().connect('end-user-action',
                                  self.undo_redo.on_end_user_action)
        self.get_buffer().connect('insert-text',
                                  self.undo_redo.on_insert_text)
        self.get_buffer().connect('delete-range',
                                  self.undo_redo.on_delete_range)
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
        self.connect('destroy', self.markup.stop)

        # Preview popover
        self.preview_popover = InlinePreview(self)

        # Drag and drop
        self.drag_drop = DragDropHandler(self, TARGET_URI, TARGET_TEXT)

        # While resizing the TextView, there is unwanted scroll upwards
        # if a top margin is present.
        # When a size allocation is detected, this variable will hold
        # the scroll to re-set until the UI is idle again.

        # TODO: Find a better way to handle unwanted scroll.
        self.frozen_scroll_scale = None

    def get_text(self):
        text_buffer = self.get_buffer()
        start_iter = text_buffer.get_start_iter()
        end_iter = text_buffer.get_end_iter()
        return text_buffer.get_text(start_iter, end_iter, False)

    def set_text(self, text):
        """Set text and clear undo history"""

        text_buffer = self.get_buffer()
        with user_action(text_buffer):
            text_buffer.set_text(text)
        self.undo_redo.clear()

    def update_vertical_margin(self, top_margin=0):
        if self.focus_mode:
            height = self.get_allocation().height + top_margin 
            # The height/6 may seem strange. It's a workaround for a GTK bug
            # If a top-margin is larger than a certain amount of
            # the TextView height, jumps may occur when pressing enter.

            # TODO: check again in GTK4
            self.set_top_margin(height / 2 + top_margin - height/6)
            self.set_bottom_margin(height / 2)
        else:
            self.props.top_margin = 80 + top_margin
            self.props.bottom_margin = 64

    def clear(self):
        """Clear text and undo history"""

        self.set_text('')

    def smooth_scroll_to(self, mark=None):
        """Scrolls if needed to ensure mark is visible.

        If mark is unspecified, the cursor is used."""

        if self.scroller is None:
            return
        if mark is None:
            mark = self.get_buffer().get_insert()
        GLib.idle_add(self.scroller.smooth_scroll_to_mark,
                      mark, self.focus_mode)

    @Gtk.Template.Callback()
    def _on_button_release_event(self, _widget, _event):
        if self.focus_mode:
            self.markup.apply()
        return False

    @Gtk.Template.Callback()
    def _on_focus_mode_update(self, *args, **kwargs):
        self.update_vertical_margin()
        self.markup.apply()
        self.smooth_scroll_to()
        self._on_spellcheck_update()
        self.grab_focus()

    @Gtk.Template.Callback()
    def _on_key_press_event(self, _widget, event):
        if self.hemingway_mode:
            return event.keyval == Gdk.KEY_BackSpace or event.keyval == Gdk.KEY_Delete

        if event.state & Gdk.ModifierType.SHIFT_MASK == Gdk.ModifierType.SHIFT_MASK \
                and event.keyval == Gdk.KEY_ISO_Left_Tab:  # Capure Shift-Tab
            self._on_shift_tab()
            return True

    @Gtk.Template.Callback()
    def _on_mark_set(self, _text_buffer, _location, mark, _data=None):
        if mark.get_name() == 'selection_bound':
            self.markup.apply()
            if not self.get_buffer().get_has_selection():
                self.smooth_scroll_to(mark)
        elif mark.get_name() == 'gtk_drag_target':
            self.smooth_scroll_to(mark)
        return True

    # TODO: this seems a little backwards way to hook things up
    @Gtk.Template.Callback()
    def _on_parent_set(self, *_):
        parent = self.get_parent()
        if parent:
            parent.set_size_request(self.get_min_width(), 500)
            self.scroller = TextViewScroller(self, parent)
            parent.get_vadjustment().connect("changed",
                                             self._on_vadjustment_changed)
            parent.get_vadjustment().connect("value-changed",
                                             self._on_vadjustment_changed)
        else:
            self.scroller = None

    @Gtk.Template.Callback()
    def _on_paste_done(self, *_):
        self.smooth_scroll_to()

    def _on_shift_tab(self):
        """Delete last character if it is a tab"""
        text_buffer = self.get_buffer()
        pen_iter = text_buffer.get_end_iter()
        pen_iter.backward_char()
        end_iter = text_buffer.get_end_iter()

        if pen_iter.get_char() == "\t":
            with user_action(text_buffer):
                text_buffer.delete(pen_iter, end_iter)

    @Gtk.Template.Callback()
    def _on_size_allocate(self, *_):
        self._update_horizontal_margin()
        self.markup.update_margins_indents()
        self.queue_draw()

        # TODO: Find a better way to handle unwanted scroll on resize.
        self.frozen_scroll_scale = self.scroll_scale
        GLib.idle_add(self._unfreeze_scroll_scale)

    @Gtk.Template.Callback()
    def _on_spellcheck_update(self, *args, **kwargs):
        self.gspell_view.set_inline_spell_checking(
            self.spellcheck and not self.focus_mode)

    @Gtk.Template.Callback()
    def _on_text_changed(self, *_):
        self.markup.apply()
        self.smooth_scroll_to()

    def _on_vadjustment_changed(self, *_):
        if self.frozen_scroll_scale is not None:
            self.scroll_scale = self.frozen_scroll_scale
        elif self.scroller.can_scroll():
            self.emit("scroll-scale-changed", self.scroll_scale)

    def _unfreeze_scroll_scale(self):
        self.frozen_scroll_scale = None
        self.queue_draw()

    @Gtk.Template.Callback()
    def _update_horizontal_margin(self, *args, **kwargs):
        width = self.get_allocation().width
        # Ensure the appropriate font size is being used
        for font_size in self._get_font_sizes():
            if width >= self.get_min_width(font_size):
                if font_size != self.font_size:
                    self.font_size = font_size
                    style_ctxt = self.get_style_context()
                    for size_class in filter(lambda style_class: style_class.startswith("size"), style_ctxt.list_classes()):
                        style_ctxt.remove_class(size_class)
                    style_ctxt.add_class("size{}".format(font_size))
                break
        else:
            return

        # Apply margin with the remaining space to allow for markup
        line_width = (self.line_chars + 1) *\
            int(self._get_char_width(self.font_size)) - 1
        horizontal_margin = (width - line_width) / 2
        self.props.left_margin = horizontal_margin
        self.props.right_margin = horizontal_margin

    def _get_font_sizes(self):
        font_sizes_list = [20, 18, 17, 16, 15, 14]
        if self.bigger_text:
            font_sizes_list[:0] = [24, 22]

        return font_sizes_list

    def get_min_width(self, font_size=None):
        """Returns the minimum width of this text view."""

        if font_size is None:
            font_size = self._get_font_sizes()[-1]
        return (self.line_chars + self._get_pad_chars(font_size) + 1) \
            * self._get_char_width(font_size) - 1

    def _get_pad_chars(self, font_size):
        """Returns the amount of character padding for font_size.

        Markup can use up to 7 in normal conditions."""

        if self.bigger_text:
            return 8 * int((1 + (font_size - self._get_font_sizes()[-1])/3))
        else:
            return 8 * (1 + font_size - self._get_font_sizes()[-1])

    @staticmethod
    def _get_char_width(font_size):
        """Returns the font width for a given size.
        Note: specific to Fira Mono!"""

        # We scale by the text scale factor system-wide setting.
        # In the css the units are in em so they're automatically scaled
        # 14.666px == 1em

        settings = Gtk.Settings.get_default()
        scale_factor = settings.props.gtk_xft_dpi / DEFAULT_DPI

        return scale_factor * font_size * 1 / 1.6
