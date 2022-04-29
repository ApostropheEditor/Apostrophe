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

import math
import webbrowser
from enum import auto, IntEnum

import gi

from apostrophe.preview_renderer import PreviewRenderer
from apostrophe.settings import Settings

gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2, GLib, Gtk, GObject

from apostrophe.preview_converter import PreviewConverter
from apostrophe.preview_web_view import PreviewWebView


class Step(IntEnum):
    CONVERT_HTML = auto()
    LOAD_WEBVIEW = auto()
    RENDER = auto()


class PreviewHandler:
    """Handles showing/hiding the preview, and allows the user to toggle between modes.

    The rendering itself is handled by `PreviewRendered`. This class handles conversion/loading and
    connects it all together (including synchronization, ie. text changes, scroll)."""

    def __init__(self, window, text_view, flap):
        self.text_view = text_view

        self.web_view = None
        self.web_view_pending_html = None

        self.preview_converter = PreviewConverter()
        self.preview_renderer = PreviewRenderer(
            window, text_view, flap)

        window.connect("style-updated", self.reload)

        self.text_changed_handler_id = None

        self.settings = Settings.new()
        self.web_scroll_handler_id = None
        self.text_scroll_handler_id = None

        self.loading = False
        self.shown = False
        self.preview_visible = False

    def show(self):
        self.__show()
        self.preview_renderer.show()

    def __show(self, html=None, step=Step.CONVERT_HTML):

        if step == Step.CONVERT_HTML:
            # First step: convert text to HTML.
            buf = self.text_view.get_buffer()
            self.preview_converter.convert(
                buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False),
                self.__show, Step.LOAD_WEBVIEW)

        elif step == Step.LOAD_WEBVIEW:
            # Second step: load HTML.
            self.loading = True

            if not self.web_view:
                self.web_view = PreviewWebView()
                self.web_view.get_settings().set_allow_universal_access_from_file_urls(True)
                #TODO: enable devtools on Devel profile
                self.web_view.get_settings().set_enable_developer_extras(True)

                # Show preview once the load is finished
                self.web_view.connect("load-changed", self.on_load_changed)

                # All links will be opened in default browser, but local files are opened in apps.
                self.web_view.connect("decide-policy", self.on_click_link)

                self.web_view.connect("context-menu", self.on_right_click)

            if self.web_view.is_loading():
                self.web_view_pending_html = html
            else:
                self.web_view.load_html(html, "file://localhost/")

        elif step == Step.RENDER:
            # Last step: show the preview. This is a one-time step.
            if not self.preview_visible:
                self.preview_visible = True

                self.text_changed_handler_id = \
                    self.text_view.get_buffer().connect("changed", self.__show)

                self.__show()

            GLib.idle_add(self.web_view.set_scroll_scale, self.text_view.scroll_scale)

            if self.settings.get_boolean("sync-scroll"):
                self.web_scroll_handler_id = \
                    self.web_view.connect("scroll-scale-changed", self.on_web_view_scrolled)
                self.text_scroll_handler_id = \
                    self.text_view.connect("scroll-scale-changed", self.on_text_view_scrolled)

    def reload(self, *_widget, reshow=False):
        if self.preview_visible:
            if reshow:
                self.hide()
            self.show()

    def hide(self):
        if self.preview_visible:
            self.preview_visible = False

            #GLib.idle_add(self.text_view.scroll_scale, self.web_view.get_scroll_scale())
            self.text_view.scroll_scale = self.web_view.get_scroll_scale()

            self.preview_renderer.hide()

            if self.text_scroll_handler_id:
                self.text_view.disconnect(self.text_scroll_handler_id)
                self.text_scroll_handler_id = None
            if self.web_scroll_handler_id:
                self.web_view.disconnect(self.web_scroll_handler_id)
                self.web_scroll_handler_id = None

        if self.text_changed_handler_id:
            self.text_view.get_buffer().disconnect(self.text_changed_handler_id)

        if self.loading:
            self.loading = False

            self.web_view.destroy()
            self.web_view = None

    def update_preview_mode(self):
        self.preview_renderer.update_mode(self.web_view)

    def on_load_changed(self, _web_view, event):
        if event == WebKit2.LoadEvent.FINISHED:
            self.loading = False
            if self.web_view_pending_html:
                self.__show(html=self.web_view_pending_html, step=Step.LOAD_WEBVIEW)
                self.web_view_pending_html = None
            else:
                # we only lazyload the webview once
                if not self.shown:
                    self.preview_renderer.load_webview(self.web_view)
                    self.shown = True
                self.__show(step=Step.RENDER)

    def on_text_view_scrolled(self, _text_view, scale):
        if self.preview_visible and not math.isclose(scale,
                                           self.web_view.get_scroll_scale(),
                                           rel_tol=1e-4):
            self.web_view.set_scroll_scale(scale)

    def on_web_view_scrolled(self, _web_view, scale):
        if self.preview_visible and self.text_view.get_mapped() and not math.isclose(
                scale, self.text_view.scroll_scale, rel_tol=1e-1):
            self.text_view.scroll_scale = scale

    @staticmethod
    def on_click_link(web_view, decision, _decision_type):
        if web_view.get_uri().startswith(("http://", "https://", "www.")):
            webbrowser.open(web_view.get_uri())
            decision.ignore()
            return True

    @staticmethod
    def on_right_click(web_view, context_menu, _event, _hit_test):
        # disable some context menu option
        for item in context_menu.get_items():
            if item.get_stock_action() in [WebKit2.ContextMenuAction.RELOAD,
                                           WebKit2.ContextMenuAction.GO_BACK,
                                           WebKit2.ContextMenuAction.GO_FORWARD,
                                           WebKit2.ContextMenuAction.STOP]:
                context_menu.remove(item)
