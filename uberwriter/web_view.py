import gi

gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2, GLib, GObject


class WebView(WebKit2.WebView):
    """A WebView that provides read/write access to scroll.

    It does so using JavaScript, by continuously monitoring it while loaded.
    The alternative is using a WebExtension and C-bindings (see reference), but that is more
    complicated implementation-wise, as well as build-wise until we start building with Meson.

    Reference: https://github.com/aperezdc/webkit2gtk-python-webextension-example
    """

    GET_SCROLL_SCALE_JS = """
e = document.documentElement;
e.scrollHeight > e.clientHeight ? e.scrollTop / (e.scrollHeight - e.clientHeight) : -1;
"""

    SET_SCROLL_SCALE_JS = """
scale = {:.16f};
e = document.documentElement;
e.scrollTop = (e.scrollHeight - e.clientHeight) * scale;
"""

    __gsignals__ = {
        "scroll-scale-changed": (GObject.SIGNAL_RUN_LAST, None, (float,)),
    }

    def __init__(self):
        super().__init__()

        self.connect("load-changed", self.on_load_changed)
        self.connect("load-failed", self.on_load_failed)
        self.connect("destroy", self.on_destroy)

        self.scroll_scale = 0.0
        self.pending_scroll_scale = None

        self.state_loaded = False
        self.state_load_failed = False
        self.state_waiting = False

        self.timeout_id = None

    def get_scroll_scale(self):
        return self.scroll_scale

    def set_scroll_scale(self, scale):
        self.pending_scroll_scale = scale
        self.state_loop()

    def on_load_changed(self, _web_view, event):
        self.state_loaded = event >= WebKit2.LoadEvent.COMMITTED and not self.state_load_failed
        self.state_load_failed = False
        self.pending_scroll_scale = self.scroll_scale
        self.state_loop()

    def on_load_failed(self, _web_view, _event):
        self.state_loaded = False
        self.state_load_failed = True
        self.state_loop()

    def on_destroy(self, _widget):
        self.state_loaded = False
        self.state_loop()

    def read_scroll_scale(self):
        self.state_waiting = True
        self.run_javascript(
            self.GET_SCROLL_SCALE_JS, None, self.sync_scroll_scale)

    def write_scroll_scale(self, scroll_scale):
        self.run_javascript(
            self.SET_SCROLL_SCALE_JS.format(scroll_scale), None, None)

    def sync_scroll_scale(self, _web_view, result):
        self.state_waiting = False
        result = self.run_javascript_finish(result)
        self.state_loop(result.get_js_value().to_double())

    def state_loop(self, scroll_scale=None, delay=16):  # 16ms ~ 60hz
        # Remove any pending callbacks
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None

        # Set scroll scale if specified, and the state is not dirty
        if scroll_scale not in (None, -1, self.scroll_scale):
            self.scroll_scale = scroll_scale
            self.emit("scroll-scale-changed", self.scroll_scale)

        # Handle the current state
        if not self.state_loaded or self.state_load_failed or self.state_waiting:
            return
        if self.pending_scroll_scale:
            self.write_scroll_scale(self.pending_scroll_scale)
            self.pending_scroll_scale = None
            self.read_scroll_scale()
        elif delay > 0:
            self.timeout_id = GLib.timeout_add(delay, self.state_loop, None, 0)
        else:
            self.read_scroll_scale()
