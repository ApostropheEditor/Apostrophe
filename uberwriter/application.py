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
from gettext import gettext as _

import gi

from uberwriter.main_window import MainWindow

gi.require_version('Gtk', '3.0') # pylint: disable=wrong-import-position
from gi.repository import GLib, Gio, Gtk, GdkPixbuf

from uberwriter import main_window
from uberwriter.settings import Settings
from uberwriter.helpers import set_up_logging
from uberwriter.preferences_dialog import PreferencesDialog
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

        self.settings.connect("changed", self.on_settings_changed)

        # Header bar

        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.on_new)
        self.add_action(action)

        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.on_open)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_recent", None)
        action.connect("activate", self.on_open_recent)
        self.add_action(action)

        action = Gio.SimpleAction.new("save", None)
        action.connect("activate", self.on_save)
        self.add_action(action)

        action = Gio.SimpleAction.new("search", None)
        action.connect("activate", self.on_search)
        self.add_action(action)

        # App Menu

        action = Gio.SimpleAction.new_stateful(
            "focus_mode", None, GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_focus_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful(
            "hemingway_mode", None, GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_hemingway_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful(
            "preview", None, GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_preview)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful(
            "fullscreen", None, GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_fullscreen)
        self.add_action(action)

        action = Gio.SimpleAction.new("save_as", None)
        action.connect("activate", self.on_save_as)
        self.add_action(action)

        action = Gio.SimpleAction.new("export", None)
        action.connect("activate", self.on_export)
        self.add_action(action)

        action = Gio.SimpleAction.new("copy_html", None)
        action.connect("activate", self.on_copy_html)
        self.add_action(action)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_preferences)
        self.add_action(action)

        action = Gio.SimpleAction.new("shortcuts", None)
        action.connect("activate", self.on_shortcuts)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_tutorial", None)
        action.connect("activate", self.on_open_tutorial)
        self.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        # Stats Menu

        stat_default = self.settings.get_string("stat-default")
        action = Gio.SimpleAction.new_stateful(
            "stat_default", GLib.VariantType.new("s"), GLib.Variant.new_string(stat_default))
        action.connect("activate", self.on_stat_default)
        self.add_action(action)

        # Preview Menu

        preview_mode = self.settings.get_string("preview-mode")
        action = Gio.SimpleAction.new_stateful(
            "preview_mode", GLib.VariantType.new("s"), GLib.Variant.new_string(preview_mode))
        action.connect("activate", self.on_preview_mode)
        self.add_action(action)

        # Shortcuts

        # TODO: be aware that a couple of shortcuts are defined in base.css

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
        self.set_accels_for_action("app.quit", ["<Ctl>w", "<Ctl>q"])

    def do_activate(self, *args, **kwargs):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            # self.window = Window(application=self, title="UberWriter")
            self.window = MainWindow(self)
            if self.args:
                self.window.load_file(self.args[0])

        self.window.present()

    def do_command_line(self, _command_line):
        """Support for command line options"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v", "--verbose", action="count", dest="verbose",
            help=_("Show debug messages (-vv debugs uberwriter also)"))
        parser.add_argument(
            "-e", "--experimental-features", help=_("Use experimental features"),
            action='store_true')
        (self.options, self.args) = parser.parse_known_args()

        set_up_logging(self.options)

        self.activate()
        return 0

    def on_settings_changed(self, settings, key):
        if key == "dark-mode-auto" or key == "dark-mode":
            self.window.apply_current_theme()
        elif key == "spellcheck":
            self.window.toggle_spellcheck(settings.get_value(key))
        elif key == "gradient-overlay":
            self.window.toggle_gradient_overlay(settings.get_value(key))
        elif key == "input-format":
            self.window.reload_preview()
        elif key == "sync-scroll":
            self.window.reload_preview(reshow=True)
        elif key == "stat-default":
            self.window.update_default_stat()
        elif key == "preview-mode":
            self.window.update_preview_mode()

    def on_new(self, _action, _value):
        self.window.new_document()

    def on_open(self, _action, _value):
        self.window.open_document()

    def on_open_recent(self, file):
        self.window.load_file(file.get_current_uri())

    def on_save(self, _action, _value):
        self.window.save_document()

    def on_search(self, _action, _value):
        self.window.open_search_and_replace()

    def on_focus_mode(self, action, value):
        action.set_state(value)
        self.window.set_focus_mode(value)

    def on_hemingway_mode(self, action, value):
        action.set_state(value)
        self.window.set_hemingway_mode(value)

    def on_preview(self, action, value):
        action.set_state(value)
        self.window.toggle_preview(value)

    def on_fullscreen(self, action, value):
        action.set_state(value)
        self.window.set_fullscreen(value)

    def on_save_as(self, _action, _value):
        self.window.save_document_as()

    def on_export(self, _action, _value):
        self.window.open_advanced_export()

    def on_copy_html(self, _action, _value):
        self.window.copy_html_to_clipboard()

    def on_preferences(self, _action, _value):
        PreferencesDialog(self.settings).show(self.window)

    def on_shortcuts(self, _action, _param):
        builder = get_builder('Shortcuts')
        builder.get_object("shortcuts").set_transient_for(self.window)
        builder.get_object("shortcuts").show()

    def on_open_tutorial(self, _action, _value):
        self.window.open_uberwriter_markdown()

    def on_about(self, _action, _param):
        builder = get_builder('About')
        about_dialog = builder.get_object("AboutDialog")
        about_dialog.set_transient_for(self.window)

        logo_file = get_media_path("de.wolfvollprecht.UberWriter.svg")
        logo = GdkPixbuf.Pixbuf.new_from_file(logo_file)

        about_dialog.set_logo(logo)
        about_dialog.present()

    def on_quit(self, _action, _param):
        self.quit()

    def on_stat_default(self, action, value):
        action.set_state(value)
        self.settings.set_string("stat-default", value.get_string())

    def on_preview_mode(self, action, value):
        action.set_state(value)
        self.settings.set_string("preview-mode", value.get_string())

# ~ if __name__ == "__main__":
    # ~ app = Application()
    # ~ app.run(sys.argv)
