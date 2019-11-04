import gi

from uberwriter import helpers
from uberwriter.theme import Theme

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio


class StyledWindow(Gtk.ApplicationWindow):
    """A window that will redraw itself upon theme changes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connect("style-updated", self.apply_current_theme)
        self.apply_current_theme()

    def apply_current_theme(self, *_):
        """Adjusts the window, CSD and preview for the current theme."""
        # Get current theme
        theme, changed = Theme.get_current_changed()
        if changed:
            # Set theme variant (dark/light)
            Gtk.Settings.get_default().set_property(
                "gtk-application-prefer-dark-theme",
                GLib.Variant("b", theme.is_dark))

            # Set theme css
            css_provider_file = Gio.File.new_for_uri(
                "resource:///de/wolfvollprecht/UberWriter/media/css/gtk/base.css")
            style_provider = Gtk.CssProvider()
            style_provider.load_from_file(css_provider_file)
            Gtk.StyleContext.add_provider_for_screen(
                self.get_screen(), style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

            # Redraw contents of window
            self.queue_draw()