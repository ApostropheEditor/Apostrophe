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

from gi.repository import Gtk, GLib, Handy, GObject

from apostrophe.settings import Settings
from apostrophe.preview_layout_switcher import PreviewLayout
from apostrophe.preview_window import PreviewWindow
from .tweener import Tweener

class PreviewRenderer(GObject.Object):
    """Renders the preview according to the user selected mode."""

    __gtype_name__ = "PreviewRenderer"

    preview_layout = GObject.Property(type=int, default=0)
    preview_window_title = GObject.Property(type=str, default="")

    def __init__(
            self, main_window, text_view, flap):
        super().__init__()
        self.main_window = main_window
        self.main_window.connect("delete-event", self.on_window_closed)
        self.main_window.connect("notify::title", self.on_window_title_changed)
        self.text_view = text_view

        self.window_size_cache = None

        self.settings = Settings.new()
        self.window = None
        self.preview_stack = self.main_window.preview_stack

        # we may get the preview layout changed underneath us, so we store
        # a cache for proper hidding the previous layout
        self.preview_layout_cache = None

        self.flap = flap

        self.connect("notify::preview-layout", self.update_mode)

    def show(self):
        """Show the preview, depending on the currently selected mode."""

        # Windowed preview: create a window and show the preview in it.
        if self.preview_layout == PreviewLayout.WINDOWED and not self.window:
            # Create transient window of the main window.
            self.window = PreviewWindow()
            self.window.connect("delete-event", self.on_window_closed)

            self.window.preview_box.pack_start(self.preview_stack, False, True, 0)

            self.bind_property("preview_window_title", self.window, "title")

            # Position it next to the main window.
            width, height = self.main_window.get_size()
            self.window.resize(width, height)
            x, y = self.main_window.get_position()
            if x is not None and y is not None:
                self.main_window.move(x, y)
                self.window.move(x + width + 16, y)

            self.window.show()

        elif self.preview_layout == PreviewLayout.HALF_WIDTH:
            self.window_size_cache = self.main_window.get_size()
            requested_width_tw = Tweener(self.flap,
                                        self.flap.set_size_request,
                                        self.text_view.get_min_width(),
                                        self.text_view.get_min_width() * 2 + 2,
                                        250, 
                                        setter_args = [-1])
            requested_width_tw.start()
            self.flap.set_reveal_flap(True)

        else:
            # if it's the first time we open the preview, set
            # the corresponding flap mode
            if self.preview_layout_cache is None:
                self.update_mode()
            self.flap.set_reveal_flap(True)

    def load_webview(self, webview):
        webview.show()
        self.main_window.preview_stack.add(webview)
        self.main_window.preview_stack.set_visible_child(webview)

    def hide(self):
        """Hide the preview, depending on the currently selected mode."""
        self.flap.set_reveal_flap(False)

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

    def shrink_window(self):
        self.flap.set_size_request(self.text_view.get_min_width(), -1)
        resize_tw = Tweener(self.main_window,
                            self.main_window.resize,
                            self.main_window.get_size()[0],
                            self.window_size_cache[0],
                            250, 
                            setter_args = [self.window_size_cache[1]])
        resize_tw.start()

    def update_mode(self, *args, web_view=None):
        """Update preview mode
        """

        def set_flap_mode(*args, **kwargs):
            # TODO: use structural pattern matching in python3.10
            if c and self.flap.get_reveal_progress() != 0:
                return

            if c:
                self.main_window.flap.disconnect(c)

            if self.preview_layout == PreviewLayout.FULL_WIDTH:
                if self.preview_layout_cache == PreviewLayout.HALF_WIDTH:
                    self.shrink_window()
                self.flap.set_fold_policy(Handy.FlapFoldPolicy.ALWAYS)
                self.flap.set_orientation(Gtk.Orientation.HORIZONTAL)

            elif self.preview_layout == PreviewLayout.HALF_WIDTH:
                self.window_size_cache = self.main_window.get_size()
                requested_width_tw = Tweener(self.flap,
                                            self.flap.set_size_request,
                                            self.text_view.get_min_width(),
                                            self.text_view.get_min_width() * 2 + 2,
                                            250, 
                                            setter_args = [-1])
                requested_width_tw.start()

                self.flap.set_fold_policy(Handy.FlapFoldPolicy.NEVER)
                self.flap.set_orientation(Gtk.Orientation.HORIZONTAL)

            elif self.preview_layout == PreviewLayout.HALF_HEIGHT:
                self.flap.set_fold_policy(Handy.FlapFoldPolicy.NEVER)
                self.flap.set_orientation(Gtk.Orientation.VERTICAL)

            else:
                raise ValueError("Unknown preview mode {}".format(self.preview_layout))

            # don't automatically show the preview when syncing the preview-layout property first time
            if self.preview_layout_cache is not None:
                self.show()
            self.preview_layout_cache = self.preview_layout

        def reatach_stack(*args, **kwargs):
            if self.flap.get_reveal_progress() != 0:
                return
            self.main_window.flap.disconnect(d)
            self.main_window.flap.remove(self.main_window.flap.get_flap())

            self.preview_layout_cache = self.preview_layout
            self.show()

        # none -> paned
        if (self.preview_layout in [PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH, PreviewLayout.HALF_HEIGHT] and
            self.preview_layout_cache is None):
            c = None
            set_flap_mode()
        # horizontal paned -> horizontal paned
        elif (self.preview_layout in [PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH] and
            self.preview_layout_cache in [PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH]):
            c = None
            set_flap_mode()
        # window -> paned
        elif (self.preview_layout_cache == PreviewLayout.WINDOWED and
              self.preview_layout in [PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH, PreviewLayout.HALF_HEIGHT]):
              self.hide()
              self.main_window.flap.set_flap(self.preview_stack)
              c = None
              set_flap_mode()
        # whatever -> paned
        elif (self.preview_layout in [PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH, PreviewLayout.HALF_HEIGHT]):
            self.hide()
            c = self.main_window.flap.connect("notify::reveal-progress", set_flap_mode)
        # paned -> windowed
        elif self.preview_layout == PreviewLayout.WINDOWED and  self.preview_layout_cache in [PreviewLayout.FULL_WIDTH, PreviewLayout.HALF_WIDTH, PreviewLayout.HALF_HEIGHT]:
            self.hide()
            d = self.main_window.flap.connect("notify::reveal-progress", reatach_stack)
        # none -> windowed
        else:
            self.main_window.flap.remove(self.main_window.flap.get_flap())
            self.preview_layout_cache = self.preview_layout

    def on_window_title_changed(self, *args, **kwargs):
        self.preview_window_title = self.main_window.get_title() + " - " + _("Preview")

    def on_window_closed(self, window, _event):
        self.main_window.lookup_action("preview").change_state(GLib.Variant.new_boolean(False))
