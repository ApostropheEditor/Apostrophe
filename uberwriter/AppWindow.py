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
# with this program.  If not, see &lt;http://www.gnu.org/licenses/&gt;.

import argparse
import webbrowser
from gettext import gettext as _

import gi

from uberwriter.Theme import Theme

gi.require_version('Gtk', '3.0') # pylint: disable=wrong-import-position
from gi.repository import GLib, Gio, Gtk, Gdk, GdkPixbuf

from uberwriter import UberwriterWindow
from uberwriter.Settings import Settings
from uberwriter.helpers import set_up_logging
from uberwriter.PreferencesDialog import PreferencesDialog
from uberwriter.helpers import get_builder, get_media_path


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="de.wolfvollprecht.UberWriter",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None
        self.settings = Settings.new()

    def do_startup(self, *args, **kwargs):

        Gtk.Application.do_startup(self)

        # Actions

        action = Gio.SimpleAction.new("help", None)
        action.connect("activate", self.on_help)
        self.add_action(action)

        action = Gio.SimpleAction.new("shortcuts", None)
        action.connect("activate", self.on_shortcuts)
        self.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        set_dark_mode = self.settings.get_value("dark-mode")
        action = Gio.SimpleAction.new_stateful("dark_mode",
                                               None,
                                               GLib.Variant.new_boolean(set_dark_mode))
        action.connect("change-state", self.on_dark_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("focus_mode",
                                               None,
                                               GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_focus_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("hemingway_mode",
                                               None,
                                               GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_hemingway_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("fullscreen",
                                               None,
                                               GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_fullscreen)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("preview",
                                               None,
                                               GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_preview)
        self.add_action(action)

        action = Gio.SimpleAction.new("search", None)
        action.connect("activate", self.on_search)
        self.add_action(action)

        set_spellcheck = self.settings.get_value("spellcheck")
        action = Gio.SimpleAction.new_stateful("spellcheck",
                                               None,
                                               GLib.Variant.new_boolean(set_spellcheck))
        action.connect("change-state", self.on_spellcheck)
        self.add_action(action)

        set_gradient_overlay = self.settings.get_value("gradient-overlay")
        action = Gio.SimpleAction.new_stateful("draw_gradient",
                                               None,
                                               GLib.Variant.new_boolean(set_gradient_overlay))
        action.connect("change-state", self.on_draw_gradient)
        self.add_action(action)

        # Menu Actions

        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.on_new)
        self.add_action(action)

        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.on_open)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_recent", None)
        action.connect("activate", self.on_open_recent)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_examples", None)
        action.connect("activate", self.on_example)
        self.add_action(action)

        action = Gio.SimpleAction.new("save", None)
        action.connect("activate", self.on_save)
        self.add_action(action)

        action = Gio.SimpleAction.new("save_as", None)
        action.connect("activate", self.on_save_as)
        self.add_action(action)

        action = Gio.SimpleAction.new("export", None)
        action.connect("activate", self.on_export)
        self.add_action(action)

        action = Gio.SimpleAction.new("HTML_copy", None)
        action.connect("activate", self.on_html_copy)
        self.add_action(action)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_preferences)
        self.add_action(action)

        # Shortcuts

        self.set_accels_for_action("app.focus_mode", ["<Ctl>d"])
        self.set_accels_for_action("app.hemingway_mode", ["<Ctl>t"])
        self.set_accels_for_action("app.fullscreen", ["F11"])
        self.set_accels_for_action("app.preview", ["<Ctl>p"])
        self.set_accels_for_action("app.search", ["<Ctl>f"])
        self.set_accels_for_action("app.spellcheck", ["F7"])

        self.set_accels_for_action("app.new", ["<Ctl>n"])
        self.set_accels_for_action("app.open", ["<Ctl>o"])
        self.set_accels_for_action("app.save", ["<Ctl>s"])
        self.set_accels_for_action("app.save_as", ["<Ctl><shift>s"])

        self.apply_current_theme()

    def do_activate(self, *args, **kwargs):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            # self.window = Window(application=self, title="UberWriter")
            self.window = UberwriterWindow.UberwriterWindow(self)
            if self.args:
                self.window.load_file(self.args[0])
            if self.options.experimental_features:
                self.window.use_experimental_features(True)

        self.window.present()

    def do_command_line(self, _command_line):
        """Support for command line options"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v", "--verbose", action="count", dest="verbose",
            help=_("Show debug messages (-vv debugs uberwriter also)"))
        parser.add_argument(
            "-e", "--experimental-features", help=_("Use experimental features"),
            action='store_true'
        )
        (self.options, self.args) = parser.parse_known_args()

        set_up_logging(self.options)

        self.activate()
        return 0

    def apply_current_theme(self):
        # get current theme
        theme = Theme.get_current()

        # set theme variant (dark/light)
        Gtk.Settings.get_default().set_property(
            "gtk-application-prefer-dark-theme",
            GLib.Variant("b", theme.is_dark))

        # set theme css
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(theme.gtk_css_path)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_about(self, _action, _param):
        builder = get_builder('About')
        about_dialog = builder.get_object("AboutDialog")
        about_dialog.set_transient_for(self.window)

        logo_file = get_media_path("de.wolfvollprecht.UberWriter.svg")
        logo = GdkPixbuf.Pixbuf.new_from_file(logo_file)

        about_dialog.set_logo(logo)

        about_dialog.present()

    def on_help(self, _action, _param):
        """open pandoc markdown web
        """
        webbrowser.open(
            "http://johnmacfarlane.net/pandoc/README.html#pandocs-markdown")

    def on_shortcuts(self, _action, _param):
        builder = get_builder('Shortcuts')
        builder.get_object("shortcuts").set_transient_for(self.window)
        builder.get_object("shortcuts").show()

    def on_dark_mode(self, action, value):
        action.set_state(value)
        self.settings.set_value("dark-mode", GLib.Variant("b", value))

        # this changes the headerbar theme accordingly
        self.apply_current_theme()

        # adjust window for theme
        self.window.apply_current_theme()

    def on_focus_mode(self, action, value):
        action.set_state(value)
        self.window.set_focus_mode(value)

    def on_hemingway_mode(self, action, value):
        action.set_state(value)
        self.window.set_hemingway_mode(value)

    def on_fullscreen(self, action, value):
        action.set_state(value)
        self.window.set_fullscreen(value)

    def on_preview(self, action, value):
        action.set_state(value)
        self.window.toggle_preview(value)

    def on_search(self, _action, _value):
        self.window.open_search_and_replace()

    def on_spellcheck(self, action, value):
        action.set_state(value)
        self.settings.set_value("spellcheck",
                                GLib.Variant("b", value))
        self.window.toggle_spellcheck(value)

    def on_draw_gradient(self, action, value):
        action.set_state(value)
        self.settings.set_value("gradient-overlay",
                                GLib.Variant("b", value))
        if value:
            self.window.overlay = self.window.scrolled_window.connect_after(
                                "draw", self.window.draw_gradient)
        else:
            self.window.scrolled_window.disconnect(self.window.overlay)

    def on_new(self, _action, _value):
        self.window.new_document()

    def on_open(self, _action, _value):
        self.window.open_document()

    def on_open_recent(self, file):
        self.window.load_file(file.get_current_uri())

    def on_example(self, _action, _value):
        self.window.open_uberwriter_markdown()

    def on_save(self, _action, _value):
        self.window.save_document()

    def on_save_as(self, _action, _value):
        self.window.save_document_as()

    def on_export(self, _action, _value):
        self.window.open_advanced_export()

    def on_html_copy(self, _action, _value):
        self.window.copy_html_to_clipboard()

    def on_preferences(self, _action, _value):
        PreferencesWindow = PreferencesDialog()
        PreferencesWindow.set_application(self)
        PreferencesWindow.set_transient_for(self.window)
        PreferencesWindow.show()

    def on_quit(self, _action, _param):
        self.quit()

# ~ if __name__ == "__main__":
    # ~ app = Application()
    # ~ app.run(sys.argv)
