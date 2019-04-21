import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2, GLib


class WebViewScroller:
    """Provides read/write scrolling functionality to a WebView.

    It does so using JavaScript, by continuously monitoring it while loaded and focused.
    The alternative is using a WebExtension and C-bindings (see reference), but that is more
    complicated implementation-wise, and build-wise, at least we start building with Meson.

    Reference: https://github.com/aperezdc/webkit2gtk-python-webextension-example
    """

    SETUP_SROLL_SCALE_JS = """
const e = document.documentElement;
function get_scroll_scale() {
    if (document.readyState !== "complete" || e.clientHeight === 0) {
        return null;
    } else if (e.scrollHeight <= e.clientHeight) {
        return 0;
    } else {
        return e.scrollTop / (e.scrollHeight - e.clientHeight);
    }
}
function set_scroll_scale(scale) {
    if (document.readyState !== "complete") {
        window.addEventListener("load", function() { set_scroll_scale(scale); });
    } else if (e.clientHeight === 0) {
        window.addEventListener("resize", function() { set_scroll_scale(scale); });
    } else if (e.scrollHeight > e.clientHeight) {
        e.scrollTop = (e.scrollHeight - e.clientHeight) * scale;
    }
    return get_scroll_scale();
}
get_scroll_scale();
""".strip()

    GET_SCROLL_SCALE_JS = "get_scroll_scale();"

    SET_SCROLL_SCALE_JS = "set_scroll_scale({:.16f});"

    def __init__(self, webview):
        super().__init__()

        self.webview = webview

        self.webview.connect("focus-in-event", self.on_focus_changed)
        self.webview.connect("focus-out-event", self.on_focus_changed)
        self.webview.connect("load-changed", self.on_load_changed)
        self.webview.connect("destroy", self.on_destroy)

        self.scroll_scale = 0

        self.state_loaded = False
        self.state_setup = False
        self.state_focused = True
        self.state_dirty = False
        self.state_waiting = False

        self.timeout_id = None

    def get_scroll_scale(self):
        return self.scroll_scale

    def set_scroll_scale(self, scale):
        self.scroll_scale = scale
        self.state_dirty = True
        self.state_loop()

    def on_focus_changed(self, _webview, event):
        self.state_focused = event.in_
        self.state_loop()

    def on_load_changed(self, _webview, event):
        self.state_loaded = event == WebKit2.LoadEvent.FINISHED
        self.state_loop()

    def on_destroy(self, _widget):
        self.state_loaded = False
        self.state_focused = False
        self.state_loop()
        self.webview = None

    def setup_scroll_state(self):
        self.state_waiting = True
        self.state_setup = True
        self.webview.run_javascript(
            self.SETUP_SROLL_SCALE_JS, None, self.sync_scroll_scale)

    def read_scroll_scale(self):
        self.state_waiting = True
        self.webview.run_javascript(
            self.GET_SCROLL_SCALE_JS, None, self.sync_scroll_scale)

    def write_scroll_scale(self):
        self.state_waiting = True
        self.state_dirty = False
        self.webview.run_javascript(
            self.SET_SCROLL_SCALE_JS.format(self.scroll_scale), None, self.sync_scroll_scale)

    def sync_scroll_scale(self, _webview, result):
        self.state_waiting = False
        result = self.webview.run_javascript_finish(result)
        self.state_loop(result.get_js_value().to_double())

    def state_loop(self, scroll_scale=None, read_delay=500):
        # Remove any pending callbacks
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None

        # Set scroll scale if specified, and the state is not dirty
        if scroll_scale is not None and not self.state_dirty:
            self.scroll_scale = scroll_scale

        # Handle the current state
        if self.state_waiting:
            return
        elif not self.state_loaded:
            return
        elif not self.state_setup:
            self.setup_scroll_state()
        elif self.state_dirty:
            self.write_scroll_scale()
        elif self.state_focused:
            if read_delay > 0:
                self.timeout_id = GLib.timeout_add(read_delay, self.state_loop, None, 0)
            else:
                self.read_scroll_scale()

