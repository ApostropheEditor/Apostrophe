import gi

from uberwriter import helpers
from uberwriter.theme import Theme

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


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
            style_provider = Gtk.CssProvider()
            style_provider.load_from_path(helpers.get_css_path("gtk/base.css"))
            Gtk.StyleContext.add_provider_for_screen(
                self.get_screen(), style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

            # Redraw contents of window
            self.queue_draw()