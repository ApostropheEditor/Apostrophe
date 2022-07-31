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

import webbrowser

import gi

gi.require_version('WebKit2', '5.0')
from gi.repository import WebKit2, GLib, GObject


class PreviewWebView(WebKit2.WebView):
    """A WebView that provides read/write access to scroll.

    It does so using JavaScript, by continuously monitoring it while loaded.
    The alternative is using a WebExtension and C-bindings (see reference),
    but that is more complicated implementation-wise,
    as well as build-wise until we start building with Meson.

    Reference: https://github.com/aperezdc/webkit2gtk-python-webextension-example
    """

    SYNC_SCROLL_SCALE_JS = """
scale = {:.16f};
write = {};

// Configure MathJax.
if (typeof hasMathJax === "undefined") {{

    hasMathJax = false;
    if (typeof MathJax !== "undefined") {{
        hasMathJax = typeof MathJax.Hub !== "undefined";
    }}
    
    if (hasMathJax) {{
        MathJax.Hub.Config({{ messageStyle: "none" }});
    }}
}}

// Figure out if scrollable and rendered.
e = document.documentElement;
canScroll = e.scrollHeight > e.clientHeight;
wasRendered = typeof isRendered !== "undefined" && isRendered;
isRendered = wasRendered ||
        !hasMathJax ||
        MathJax.Hub.queue.running == 0 && MathJax.Hub.queue.pending == 0;

// Write the current scroll if instructed or if it was just rendered.
if (canScroll && (write || isRendered && !wasRendered)) {{
    e.scrollTop = (e.scrollHeight - e.clientHeight) * scale;
}}

// Return the current scroll if scrollable and rendered, or -1.
if (canScroll && isRendered) {{
    e.scrollTop / (e.scrollHeight - e.clientHeight);
}} else {{
    -1;
}}
""".strip()

    __gsignals__ = {
        "scroll-scale-changed": (GObject.SIGNAL_RUN_LAST, None, (float,)),
    }

    def __init__(self):
        super().__init__()

        # TODO
        #self.connect("size-allocate", self.on_size_allocate)
        self.connect("decide-policy", self.on_decide_policy)
        self.connect("load-changed", self.on_load_changed)
        self.connect("load-failed", self.on_load_failed)
        self.connect("destroy", self.on_destroy)

        #self.props.expand = True

        self.scroll_scale = -1

        self.state_loaded = False
        self.state_load_failed = False
        self.state_discard_read = False
        self.state_dirty = False
        self.state_waiting = False

        self.timeout_id = None

    def can_scroll(self):
        return self.scroll_scale != -1

    def get_scroll_scale(self):
        return self.scroll_scale

    def set_scroll_scale(self, scale):
        self.state_dirty = scale != self.scroll_scale
        self.scroll_scale = scale
        self.state_loop()

    def on_size_allocate(self, *_):
        self.set_scroll_scale(self.scroll_scale)

    def on_decide_policy(self, _web_view, decision, decision_type):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION and \
                decision.get_navigation_action().is_user_gesture():
            webbrowser.open(decision.get_request().get_uri())
            decision.ignore()       # Do not follow the link in the WebView
            return True
        return False

    def on_load_changed(self, _web_view, event):
        self.state_loaded = event >= WebKit2.LoadEvent.COMMITTED and not self.state_load_failed
        self.state_load_failed = False
        self.state_discard_read = event == WebKit2.LoadEvent.STARTED and self.state_waiting
        self.state_dirty = True
        self.state_loop()

    def on_load_failed(self, _web_view, _event):
        self.state_loaded = False
        self.state_load_failed = True
        self.state_loop()

    def on_destroy(self, _widget):
        self.state_loaded = False
        self.state_loop()

    def sync_scroll_scale(self, scroll_scale, write):
        self.state_waiting = True
        self.run_javascript(
            self.SYNC_SCROLL_SCALE_JS.format(
                scroll_scale, "true" if write else "false"),
            None, self.finish_sync_scroll_scale)

    def finish_sync_scroll_scale(self, _web_view, result):
        self.state_waiting = False
        result = self.run_javascript_finish(result)
        self.state_loop(result.get_js_value().to_double())

    def state_loop(self, scroll_scale=None, delay=16):  # 16ms ~ 60hz
        # Remove any pending callbacks
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None

        # Set scroll scale if specified, and the state is not dirty
        if not self.state_discard_read and scroll_scale not in (
                None, self.scroll_scale):
            self.scroll_scale = scroll_scale
            if self.scroll_scale != -1:
                self.emit("scroll-scale-changed", self.scroll_scale)
        self.state_discard_read = False

        # Handle the current state
        if not self.state_loaded or self.state_load_failed or self.state_waiting:
            return
        elif self.state_dirty or delay == 0:
            self.sync_scroll_scale(self.scroll_scale, self.state_dirty)
            self.state_dirty = False
        else:
            self.timeout_id = GLib.timeout_add(delay, self.state_loop, None, 0)
