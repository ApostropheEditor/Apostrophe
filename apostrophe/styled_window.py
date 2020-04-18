import gi

from apostrophe import helpers

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio


class StyledWindow(Gtk.ApplicationWindow):
    """A window that will redraw itself upon theme changes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set theme css
        css_provider_file = Gio.File.new_for_uri(
            "resource:///org/gnome/gitlab/somas/Apostrophe/media/css/gtk/base.css")
        style_provider = Gtk.CssProvider()
        style_provider.load_from_file(css_provider_file)
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
