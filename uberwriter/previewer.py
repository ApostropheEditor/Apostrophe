import math
import webbrowser
from enum import auto, IntEnum

import gi

from uberwriter.helpers import get_builder

gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2

from uberwriter.preview_converter import PreviewConverter
from uberwriter.settings import Settings
from uberwriter.web_view import WebView


class Step(IntEnum):
    CONVERT_HTML = auto()
    LOAD_WEBVIEW = auto()
    RENDER = auto()


class Previewer:
    def __init__(self, content, editor, text_view):
        self.content = content
        self.editor = editor
        self.text_view = text_view

        self.web_view = None
        self.web_view_pending_html = None

        builder = get_builder("Preview")
        self.preview = builder.get_object("preview")
        self.preview_mode_button = builder.get_object("preview_mode_button")
        self.preview_mode_button.get_style_context().add_class('toggle-button')

        self.preview_converter = PreviewConverter()

        self.web_scroll_handler_id = None
        self.text_scroll_handler_id = None
        self.text_changed_handler_id = None

        self.settings = Settings.new()

        self.loading = False
        self.showing = False

    def show(self):
        self.__show()

    def reload(self):
        if self.showing:
            self.show()

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
                self.web_view = WebView()
                self.web_view.get_settings().set_allow_universal_access_from_file_urls(True)

                # Show preview once the load is finished
                self.web_view.connect("load-changed", self.on_load_changed)

                # All links will be opened in default browser, but local files are opened in apps.
                self.web_view.connect("decide-policy", self.on_click_link)

            if self.web_view.is_loading():
                self.web_view_pending_html = html
            else:
                self.web_view.load_html(html, 'file://localhost/')

        elif step == Step.RENDER:
            # Last and one-time step: show the web view.
            if self.showing:
                return
            self.showing = True

            if self.settings.get_boolean("preview-side-by-side"):
                self.content.set_size_request(self.text_view.get_min_width() * 2, -1)
                self.web_view.set_scroll_scale(self.text_view.get_scroll_scale())
                self.web_scroll_handler_id = \
                    self.web_view.connect("scroll-scale-changed", self.on_web_view_scrolled)
                self.text_scroll_handler_id = \
                    self.text_view.connect("scroll-scale-changed", self.on_text_view_scrolled)
                self.text_changed_handler_id = \
                    self.text_view.get_buffer().connect("changed", self.__show)
            else:
                self.content.remove(self.editor)

            self.preview.pack_start(self.web_view, True, True, 0)
            self.content.add(self.preview)
            self.web_view.show()

    def hide(self):
        if self.showing:
            self.showing = False

            if self.settings.get_boolean("preview-side-by-side"):
                self.content.set_size_request(-1, -1)
                self.web_view.disconnect(self.web_scroll_handler_id)
                self.text_view.disconnect(self.text_scroll_handler_id)
                self.text_view.get_buffer().disconnect(self.text_changed_handler_id)
            else:
                self.content.add(self.editor)

            self.content.remove(self.preview)
            self.preview.remove(self.web_view)

        if self.loading:
            self.loading = False

            self.web_view.destroy()
            self.web_view = None

    def on_load_changed(self, _web_view, event):
        if event == WebKit2.LoadEvent.FINISHED:
            self.loading = False
            if self.web_view_pending_html:
                self.__show(html=self.web_view_pending_html, step=Step.LOAD_WEBVIEW)
                self.web_view_pending_html = None
            else:
                self.__show(step=Step.RENDER)

    def on_text_view_scrolled(self, _text_view, scale):
        if not math.isclose(scale, self.web_view.get_scroll_scale(), rel_tol=1e-5):
            self.web_view.set_scroll_scale(scale)

    def on_web_view_scrolled(self, _web_view, scale):
        if not math.isclose(scale, self.text_view.get_scroll_scale(), rel_tol=1e-5):
            self.text_view.set_scroll_scale(scale)

    @staticmethod
    def on_click_link(web_view, decision, _decision_type):
        if web_view.get_uri().startswith(("http://", "https://", "www.")):
            webbrowser.open(web_view.get_uri())
            decision.ignore()
            return True
