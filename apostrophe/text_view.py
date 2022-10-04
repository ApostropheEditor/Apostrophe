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

import collections
import mimetypes
import urllib
from datetime import datetime
from gettext import gettext as _
from os.path import basename

import gi

from apostrophe.helpers import user_action
from apostrophe.inline_preview import InlinePreview
from apostrophe.settings import Settings
from apostrophe.text_view_format_inserter import FormatInserter
from apostrophe.text_view_markup_handler import MarkupHandler
from apostrophe.text_view_scroller import TextViewScroller
from apostrophe.text_buffer import ApostropheTextBuffer

gi.require_version('Gtk', '4.0')
#gi.require_version('Gspell', '1')
import logging

from gi.repository import Adw, Gdk, Gio, GLib, GObject, Gtk

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
    - Drag and drop
    - Scrolling (via TextViewScroller)
    - The various modes supported by Apostrophe (e. Focus Mode, Hemingway Mode)
    """

    __gtype_name__ = "ApostropheTextView"

    __gsignals__ = {
        'unindent': (GObject.SignalFlags.ACTION, None, ()),
        'insert-italic': (GObject.SignalFlags.ACTION, None, ()),
        'insert-bold': (GObject.SignalFlags.ACTION, None, ()),
        'insert-hrule': (GObject.SignalFlags.ACTION, None, ()),
        'insert-listitem': (GObject.SignalFlags.ACTION, None, ()),
        'insert-header': (GObject.SignalFlags.ACTION, None, (int,)),
        'insert-strikethrough': (GObject.SignalFlags.ACTION, None, ()),
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

    hemingway_attempts = collections.deque(4*[datetime.min], 4)

    @GObject.Property(type=float, default=0)
    def scroll_scale(self):
        return self.scroller.get_scroll_scale() if self.scroller else 0

    @scroll_scale.setter
    def scroll_scale(self, scale):
        if self.scroller:
            self.scroller.set_scroll_scale(scale)

    gesture_controller = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.settings = Settings.new()

        self.buffer = self.get_buffer()
        # Spell checking
        # self.gspell_view = Gspell.TextView.get_from_gtk_text_view(self)
        # self.gspell_view.basic_setup()

        # Format shortcuts
        self.shortcut = FormatInserter()
        self.connect('unindent', self.buffer._unindent)
        self.connect('insert-italic', self.shortcut.insert_italic)
        self.connect('insert-bold', self.shortcut.insert_bold)
        self.connect('insert-strikethrough', self.shortcut.insert_strikethrough)
        self.connect('insert-hrule', self.shortcut.insert_horizontal_rule)
        self.connect('insert-listitem', self.shortcut.insert_list_item)
        self.connect('insert-header', self.shortcut.insert_header)

        # Hemingway
        self.buffer.connect('attempted-hemingway', self.on_attempted_hemingway)

        # Markup
        self.markup = MarkupHandler(self)
        self.connect('destroy', self.markup.stop)

        # Preview popover
        # self.preview_popover = InlinePreview(self)

        # Drag and drop
        drop_target = Gtk.DropTarget.new(GObject.TYPE_STRING, Gdk.DragAction.COPY)
        drop_target.connect('drop', self.on_drop)
        self.add_controller(drop_target)

        # While resizing the TextView, there is unwanted scroll upwards
        # if a top margin is present.
        # When a size allocation is detected, this variable will hold
        # the scroll to re-set until the UI is idle again.

        # TODO: Find a better way to handle unwanted scroll.
        self.frozen_scroll_scale = None

        self.update_vertical_margin()

    def on_drop(self, drop_target, content, _x, _y):
        # check if a file was dropped
        try:
            GLib.Uri.is_valid(content, GLib.UriFlags.NONE)
            uri = GLib.Uri.parse(content, GLib.UriFlags.NONE)

            # we could try to use glib utils for handling uris but it's not that
            # worth it

            if content.startswith("file://"):
                # remove trailing newlines
                content = content.strip()

                name = basename(urllib.parse.unquote_plus(content))
                mime = Gio.content_type_guess(content)

                # stripe "file://"
                content = content[7:]

                if mime[0] is not None and mime[0].startswith('image/'):
                    basepath = self.settings.get_string("open-file-path")
                    basepath = urllib.parse.quote(basepath)


                    # for handling local URIs we need to substract the basepath
                    # except when it is "/" (document not saved)
                    # TODO: use g_uri_resolve_relative
                    if content.startswith(basepath) and basepath != "/":
                        content = content[len(basepath) + 1:]

                    content = "![{}]({})".format(name, content)
                    limit_left = 2
                    limit_right = len(name)
                else:
                    content = "[{}]({})".format(name, content)
                    limit_left = 1
                    limit_right = len(name)
            elif content.startswith(("https", "http")):
                content = "[{}]({})".format(_("web page"), content)
                limit_left = 1
                limit_right = len(_("web page"))
        # otherwise we just received text
        except Exception as e:
            # delete automatically added DnD text
            insert_mark = self.buffer.get_insert()
            cursor_iter_r = self.buffer.get_iter_at_mark(insert_mark)
            cursor_iter_l = cursor_iter_r.copy()
            cursor_iter_l.backward_chars(len(content))

            self.buffer.delete(cursor_iter_l, cursor_iter_r)

            limit_left = 0
            limit_right = 0

        self.buffer.place_cursor(self.buffer.get_iter_at_mark(
            self.buffer.get_mark('gtk_drag_target')))
        self.buffer.insert_at_cursor(content)
        insert_mark = self.buffer.get_insert()
        selection_bound = self.buffer.get_selection_bound()
        cursor_iter = self.buffer.get_iter_at_mark(insert_mark)
        cursor_iter.backward_chars(len(content) - limit_left)
        self.buffer.move_mark(insert_mark, cursor_iter)
        cursor_iter.forward_chars(limit_right)
        self.buffer.move_mark(selection_bound, cursor_iter)

    def get_text(self):
        start_iter = self.buffer.get_start_iter()
        end_iter = self.buffer.get_end_iter()
        return self.buffer.get_text(start_iter, end_iter, False)

    def set_text(self, text):
        """Set text and clear undo history"""

        self.buffer.begin_irreversible_action()
        with user_action(self.buffer):
            self.buffer.set_text(text)
        self.buffer.end_irreversible_action()

    def update_vertical_margin(self, top_margin=0):
        if self.focus_mode:
            height = self.get_allocation().height + top_margin 

            self.set_top_margin(height / 2 + top_margin)
            self.set_bottom_margin(height / 2)
        else:
            self.set_top_margin(80 + top_margin)
            self.set_bottom_margin(64)

    def clear(self):
        """Clear text and undo history"""

        self.set_text('')

    def smooth_scroll_to(self, mark=None):
        """Scrolls if needed to ensure mark is visible.

        If mark is unspecified, the cursor is used."""

        if self.scroller is None:
            return
        if mark is None:
            mark = self.buffer.get_insert()
        GLib.idle_add(self.scroller.smooth_scroll_to_mark,
                      mark, self.focus_mode)

    @Gtk.Template.Callback()
    def _on_button_release_event(self, *args, **kwargs):
        if self.focus_mode:
            self.markup.apply()
            self.smooth_scroll_to()
        return False

    @Gtk.Template.Callback()
    def _on_focus_mode_update(self, *args, **kwargs):
        self.update_vertical_margin()
        self.markup.apply()
        self.smooth_scroll_to()
        self._on_spellcheck_update()
        self.grab_focus()

    def on_attempted_hemingway(self, *args):
            # log the time into a list with max length of 4
            # then check if the time differences are small enough
            # to show the help popover again
            self.hemingway_attempts.appendleft(datetime.now())
            if (self.hemingway_attempts[0] - self.hemingway_attempts[3]).seconds <= 70:
                self.settings.set_int("hemingway-toast-count", 0)
                self.activate_action("win.show_hemingway_toast")

            spring_params = Adw.SpringParams.new(0.5, 0.5, 1000)
            target = Adw.PropertyAnimationTarget.new(self, "left-margin")
            hemingway_animation = Adw.SpringAnimation.new(self, self.get_left_margin(), self.get_left_margin(), spring_params, target)
            hemingway_animation.set_initial_velocity(10)
            hemingway_animation.play()

    @Gtk.Template.Callback()
    def _on_mark_set(self, _text_buffer, _location, mark, _data=None):
        # only scroll if the cursor was moved by keyboard.
        # otherwise check _on_button_release_event
        if mark.get_name() == 'selection_bound' and not self.gesture_controller.is_active():
            self.markup.apply()
            if not self.buffer.get_has_selection():
                self.smooth_scroll_to(mark)
        elif mark.get_name() == 'gtk_drag_target':
            self.smooth_scroll_to(mark)
        return True

    @Gtk.Template.Callback()
    def _on_paste_done(self, *_):
        self.smooth_scroll_to()

    def _on_size_allocate(self, *_):
        self._update_horizontal_margin()
        self.markup.update_margins_indents()
        self.queue_draw()

        # TODO: Find a better way to handle unwanted scroll on resize.
        self.frozen_scroll_scale = self.scroll_scale
        GLib.idle_add(self._unfreeze_scroll_scale)

    @Gtk.Template.Callback()
    def _on_spellcheck_update(self, *args, **kwargs):
        pass
        # self.gspell_view.set_inline_spell_checking(
        #     self.spellcheck and not self.focus_mode)

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
                    for size_class in filter(lambda style_class: style_class.startswith("size"), self.get_css_classes()):
                        self.remove_css_class(size_class)
                    self.add_css_class("size{}".format(font_size))
                break
        else:
            return

        # Apply margin with the remaining space to allow for markup
        line_width = (self.line_chars + 1) *\
            int(self._get_char_width(self.font_size)) - 1
        horizontal_margin = (width - line_width) / 2
        self.set_left_margin(horizontal_margin)
        self.set_right_margin(horizontal_margin)

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

    def do_size_allocate(self, width, height, baseline):
        Gtk.TextView.do_size_allocate(self,width, height, baseline)
        self._on_size_allocate()


    # TODO: refactor TextViewScroller
    def do_map(self, *args, **kwargs):
        Gtk.TextView.do_map(self)

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
