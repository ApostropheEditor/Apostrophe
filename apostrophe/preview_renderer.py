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

from gettext import gettext as _

from gi.repository import Gtk, GLib, Adw, GObject

from apostrophe.settings import Settings
from apostrophe.preview_layout_switcher import PreviewLayout
from apostrophe.preview_window import PreviewWindow

class PreviewRenderer(GObject.Object):
    """Renders the preview according to the user selected mode."""

    __gtype_name__ = "PreviewRenderer"

    preview_layout = GObject.Property(type=int, default=0)
    preview_window_title = GObject.Property(type=str, default="")

    def __init__(
            self, main_window, text_view, flap):
        super().__init__()
        self.main_window = main_window
        self.main_window.connect("close-request", self.on_window_closed)
        self.main_window.connect("notify::title", self.on_window_title_changed)
        self.text_view = text_view

        self.window_size_cache = 0

        self.settings = Settings.new()
        self.window = None
        self.preview_stack = self.main_window.preview_stack

        # we may get the preview layout changed underneath us, so we store
        # a cache for proper hidding the previous layout
        self.preview_layout_cache = None

        self.flap = flap

        request_width_target = Adw.PropertyAnimationTarget.new(self.flap, "width-request")
        self.requested_width_tw = Adw.TimedAnimation.new(self.flap, 
                                                         self.text_view.get_min_width(),
                                                         self.text_view.get_min_width() * 2 + 2,
                                                         250, request_width_target)


        self.connect("notify::preview-layout", self.update_mode)

    def update_mode(self, *args, web_view=None):
        """Update preview mode"""
        if not self.main_window.preview:
            return
        self.show()

    def load_webview(self, webview):
        webview.show()
        self.main_window.preview_stack.add_child(webview)
        self.main_window.preview_stack.set_visible_child(webview)

    def hide(self):
        """Hide the preview, depending on the currently selected mode."""
        self.flap.set_reveal_flap(False)

        self.preview_stack.remove_css_class("half-width")
        self.preview_stack.remove_css_class("full-width")

        # Windowed preview: remove preview and destroy window.
        if self.preview_layout_cache == PreviewLayout.WINDOWED:
            self.main_window.present()
            self.window.preview_box.remove(self.preview_stack)
            self.window.destroy()
            self.window = None
        else:
            # Half-width/height previews: remove preview and reset size
            # requirements.
            if self.preview_layout_cache == PreviewLayout.HALF_WIDTH:
                self.shrink_window()

        self.preview_layout_cache = None

    def shrink_window(self):
        self.flap.set_size_request(self.text_view.get_min_width(), -1)

        resize_tw_target = Adw.PropertyAnimationTarget.new(self.main_window, "default-width")
        resize_tw = Adw.TimedAnimation.new(self.main_window,
                                                self.main_window.get_width(),
                                                self.window_size_cache,
                                                250, resize_tw_target)
        resize_tw.play()

    def grow_window(self):
        self.window_size_cache = self.main_window.get_width()
        self.requested_width_tw.play()

    def resize_window(self):
        match (self.preview_layout_cache, self.preview_layout):
            case (None | PreviewLayout.HALF_HEIGHT | PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH):
                self.grow_window()
            case (PreviewLayout.HALF_WIDTH, PreviewLayout.HALF_HEIGHT | PreviewLayout.FULL_WIDTH):
                self.shrink_window()
            case (_, _):
                return

    def show_preview_window(self):
        if not self.window:
            self.window = PreviewWindow()
            self.window.connect("close-request", self.on_window_closed)

            self.main_window.flap.set_flap(None)
            self.window.preview_box.append(self.preview_stack)

            self.bind_property("preview_window_title", self.window, "title")

            width, height = self.main_window.get_default_size()
            self.window.set_default_size(width, height)

            self.window.show()

            self.preview_layout_cache = PreviewLayout.WINDOWED

    def show(self):
        """Show the preview, depending on the currently selected mode."""
        def set_flap_mode(*args, **kwargs):
            # Ideally this doesn't show the flap but since it's called as a callback
            # when other flaps hide, we gotta do it here. That's why it's important
            # this nevers gets called if the preview is not shown

            if c and self.flap.get_reveal_progress() != 0:
                return

            if c:
                self.main_window.flap.disconnect(c)

            self.preview_stack.remove_css_class("half-width")
            self.preview_stack.remove_css_class("full-width")

            match self.preview_layout:
                case PreviewLayout.FULL_WIDTH:
                    self.flap.set_orientation(Gtk.Orientation.HORIZONTAL)
                    self.flap.set_fold_policy(Adw.FlapFoldPolicy.ALWAYS)
                    self.preview_stack.add_css_class("full-width")
                    self.flap.set_reveal_flap(True)

                case PreviewLayout.HALF_WIDTH:
                    self.flap.set_orientation(Gtk.Orientation.HORIZONTAL)
                    self.flap.set_fold_policy(Adw.FlapFoldPolicy.NEVER)
                    self.preview_stack.add_css_class("half-width")
                    self.flap.set_reveal_flap(True)

                case PreviewLayout.HALF_HEIGHT:
                    self.flap.set_orientation(Gtk.Orientation.VERTICAL)
                    self.flap.set_fold_policy(Adw.FlapFoldPolicy.NEVER)
                    self.flap.set_reveal_flap(True)

                case _:
                    raise ValueError("Unknown preview mode {}".format(self.preview_layout))

            self.preview_layout_cache = self.preview_layout

        def reatach_stack(*args, **kwargs):
            if self.flap.get_reveal_progress() != 0:
                return
            self.main_window.flap.disconnect(d)
            self.main_window.flap.set_flap(None)

            self.preview_layout_cache = self.preview_layout
            self.show_preview_window()

        match (self.preview_layout_cache, self.preview_layout):
            case (None, PreviewLayout.WINDOWED):
                self.show_preview_window()

            case (PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH) |\
                 (PreviewLayout.HALF_WIDTH, PreviewLayout.FULL_WIDTH) |\
                 (None, PreviewLayout.FULL_WIDTH | PreviewLayout.HALF_WIDTH | PreviewLayout.HALF_HEIGHT):
                self.resize_window()
                c = None
                set_flap_mode()

            case (PreviewLayout.HALF_HEIGHT, PreviewLayout.FULL_WIDTH | PreviewLayout.HALF_WIDTH) |\
                 (PreviewLayout.FULL_WIDTH | PreviewLayout.HALF_WIDTH, PreviewLayout.HALF_HEIGHT):
                self.hide()
                self.resize_window()
                c = self.main_window.flap.connect("notify::reveal-progress", set_flap_mode)

            case (PreviewLayout.WINDOWED, PreviewLayout.FULL_WIDTH | PreviewLayout.HALF_WIDTH | PreviewLayout.HALF_HEIGHT):
                self.hide()
                self.main_window.flap.set_flap(self.preview_stack)
                self.show()

            case (PreviewLayout.FULL_WIDTH | PreviewLayout.HALF_WIDTH | PreviewLayout.HALF_HEIGHT, PreviewLayout.WINDOWED):
                self.hide()
                d = self.main_window.flap.connect("notify::reveal-progress", reatach_stack)

    def on_window_title_changed(self, *args, **kwargs):
        self.preview_window_title = self.main_window.get_title() + " - " + _("Preview")

    def on_window_closed(self, *args):
        self.main_window.lookup_action("preview").change_state(GLib.Variant.new_boolean(False))
