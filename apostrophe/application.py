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

import gi


gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import GLib, Gio, Gtk, Gdk, Handy

from apostrophe.main_window import MainWindow
from apostrophe.settings import Settings
from apostrophe.helpers import set_up_logging
from apostrophe.preferences_dialog import PreferencesDialog
from apostrophe.inhibitor import Inhibitor
from apostrophe.theme_switcher import Theme


class Application(Gtk.Application):

    def __init__(self, application_id, *args, **kwargs):
        super().__init__(*args, application_id=application_id,
                         flags=Gio.ApplicationFlags.HANDLES_OPEN,
                         **kwargs)

        self.add_main_option("verbose", b"v", GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Verbose output", None)

        # Hardcode Adwaita to prevent issues with third party themes
        gtk_settings = Gtk.Settings.get_default()
        self._set_theme(gtk_settings)
        gtk_settings.connect("notify::gtk-theme-name", self._set_theme)
        gtk_settings.connect("notify::gtk-icon-theme-name", self._set_theme)

        # Set css theme
        css_provider_file = Gio.File.new_for_uri(
            "resource:///org/gnome/gitlab/somas/Apostrophe/media/css/gtk/Adwaita.css")
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_file(css_provider_file)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Set editor keybindings
        # SCSS is not fit for this, so we do it in an external css file
        css_bindings_file = Gio.File.new_for_uri(
            "resource:///org/gnome/gitlab/somas/Apostrophe/media/css/gtk/bindings.css")
        self.bindings_provider = Gtk.CssProvider()
        self.bindings_provider.load_from_file(css_bindings_file)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.bindings_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Set icons
        Gtk.IconTheme.get_default().add_resource_path(
            "/org/gnome/gitlab/somas/Apostrophe/icons"
        )

        Handy.init()

        self.window = None
        self.settings = Settings.new()
        self.inhibitor = None
        self._application_id = application_id

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
        color_scheme = self.settings.get_string("color-scheme")
        action = Gio.SimpleAction.new_stateful(
                 "color_scheme", GLib.VariantType.new("s"),
                 GLib.Variant.new_string(color_scheme))
        action.connect("activate", self._set_color_scheme)
        self.add_action(action)

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

        action = Gio.SimpleAction.new("export", GLib.VariantType("s"))
        action.connect("activate", self.on_export)
        self.add_action(action)

        action = Gio.SimpleAction.new("advanced_export", None)
        action.connect("activate", self.on_advanced_export)
        self.add_action(action)

        action = Gio.SimpleAction.new("copy_html", None)
        action.connect("activate", self.on_copy_html)
        self.add_action(action)

        action = Gio.SimpleAction.new("search_replace", None)
        action.connect("activate", self.on_search_replace)
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
                 "stat_default", GLib.VariantType.new("s"),
                 GLib.Variant.new_string(stat_default))
        action.connect("activate", self.on_stat_default)
        self.add_action(action)

        # Preview Menu

        preview_mode = self.settings.get_string("preview-mode")
        action = Gio.SimpleAction.new_stateful(
                 "preview_mode",
                 GLib.VariantType.new("s"),
                 GLib.Variant.new_string(preview_mode))
        action.connect("activate", self.on_preview_mode)
        self.add_action(action)

        # Shortcuts

        # TODO: be aware that a couple of shortcuts are defined in base.css

        self.set_accels_for_action("app.focus_mode", ["<Ctl>d"])
        self.set_accels_for_action("app.hemingway_mode", ["<Ctl>t"])
        self.set_accels_for_action("app.fullscreen", ["F11"])
        self.set_accels_for_action("app.preview", ["<Ctl>p"])
        self.set_accels_for_action("app.search", ["<Ctl>f"])
        self.set_accels_for_action("app.search_replace", ["<Ctl>h"])
        self.set_accels_for_action("app.spellcheck", ["F7"])

        self.set_accels_for_action("app.new", ["<Ctl>n"])
        self.set_accels_for_action("app.open", ["<Ctl>o"])
        self.set_accels_for_action("app.save", ["<Ctl>s"])
        self.set_accels_for_action("app.save_as", ["<Ctl><shift>s"])
        self.set_accels_for_action("app.quit", ["<Ctl>w", "<Ctl>q"])

        # Inhibitor
        self.inhibitor = Inhibitor()

    def do_activate(self, *args, **kwargs):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(self)

        if self._application_id == 'org.gnome.gitlab.somas.Apostrophe.Devel':
            self.window.get_style_context().add_class('devel')

        self._set_color_scheme()
        self.window.present()

    def do_handle_local_options(self, options):
        if options.contains("verbose") or self._application_id \
                == 'org.gnome.gitlab.somas.Apostrophe.Devel':

            set_up_logging(1)
        return -1

    def do_open(self, files, _n_files, _hint):
        self.activate()
        self.window.load_file(files[0])

    def _set_theme(self, settings, *_pspec):
        # Third party themes cause issues with Apostrophe custom stylesheets
        # If the user has a third party theme selected, we just change it to
        # Adwaita to prevent those issues
 
        theme_name = settings.get_property("gtk-theme-name")
        icon_theme_name = settings.get_property("gtk-icon-theme-name")

        if (theme_name not in ["Adwaita",
                               "HighContrast",
                               "HighContrastInverse"]):
            settings.set_property("gtk-theme-name", "Adwaita")

        if icon_theme_name != "Adwaita":
            settings.set_property("gtk-icon-theme-name", "Adwaita")

    def _set_color_scheme(self):

        theme = Theme.get_current()

        settings = Gtk.Settings.get_default()
        prefer_dark_theme = (theme.name == 'dark')
        settings.props.gtk_application_prefer_dark_theme = prefer_dark_theme

        if not self.window:
            return

        self.style_provider.load_from_file(theme.gtk_css)

        if settings.props.gtk_theme_name == "HighContrast" and prefer_dark_theme:
            settings.props.gtk_theme_name = "HighContrastInverse"
        elif settings.props.gtk_theme_name == "HighContrastInverse" and not prefer_dark_theme:
            settings.props.gtk_theme_name = "HighContrast"

    def on_settings_changed(self, settings, key):
        if key == "color-scheme":
            self._set_color_scheme()
        elif key == "spellcheck":
            self.window.toggle_spellcheck(settings.get_value(key))
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

    def on_open_recent(self, recents_widget):
        recent_uri = recents_widget.get_current_uri()
        self.window.load_file(Gio.File.new_for_uri(recent_uri))

    def on_open_tutorial(self, _action, _value):
        tutorial = Gio.File.new_for_uri(
            "resource:///org/gnome/gitlab/somas/"
            "Apostrophe/media/apostrophe_markdown.md")
        self.window.load_file(tutorial)

    def on_save(self, _action, _value):
        self.window.save_document()

    def on_search(self, _action, _value):
        self.window.open_search()

    def on_search_replace(self, _action, _value):
        self.window.open_search(replace=True)

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

    def on_export(self, _action, value):
        self.window.open_export(value.get_string())

    def on_advanced_export(self, _action, _value):
        self.window.open_advanced_export()

    def on_copy_html(self, _action, _value):
        self.window.copy_html_to_clipboard()

    def on_preferences(self, _action, _value):
        PreferencesDialog(self.settings).show(self.window)

    def on_shortcuts(self, _action, _param):
        builder = Gtk.Builder()
        builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/ui/Shortcuts.ui")
        builder.get_object("shortcuts").set_transient_for(self.window)
        builder.get_object("shortcuts").show()

    def on_about(self, _action, _param):
        builder = Gtk.Builder()
        builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/About.ui")
        about_dialog = builder.get_object("AboutDialog")
        about_dialog.set_transient_for(self.window)

        about_dialog.present()

    def on_quit(self, _action, _param):
        if not self.window.on_delete_called(self):
            self.quit()

    def on_stat_default(self, action, value):
        action.set_state(value)
        self.settings.set_string("stat-default", value.get_string())

    def on_preview_mode(self, action, value):
        action.set_state(value)
        self.settings.set_string("preview-mode", value.get_string())
