# Copyright (C) 2022, Manuel Genovés <manuel.genoves@gmail.com>
#               2019, Wolf Vollprecht <w.vollprecht@gmail.com>
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
from apostrophe.preferences_dialog import ApostrophePreferencesDialog
from apostrophe.inhibitor import Inhibitor
from apostrophe.theme_switcher import Theme


class Application(Gtk.Application):

    def __init__(self, application_id, *args, **kwargs):
        super().__init__(*args, application_id=application_id,
                         flags=Gio.ApplicationFlags.HANDLES_OPEN | Gio.ApplicationFlags.NON_UNIQUE,
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

        self.windows = []
        self.settings = Settings.new()
        self.inhibitor = None
        self._application_id = application_id

    def do_startup(self, *args, **kwargs):

        Gtk.Application.do_startup(self)


        color_scheme = self.settings.get_string("color-scheme")
        action = Gio.SimpleAction.new_stateful(
                 "color_scheme", GLib.VariantType.new("s"),
                 GLib.Variant.new_string(color_scheme))
        action.connect("activate", self._set_color_scheme)
        self.add_action(action)

        action = Gio.SimpleAction.new("new_window", None)
        action.connect("activate", self.on_new_window)
        self.add_action(action)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_preferences)
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

        # Stats Menu

        stat_default = self.settings.get_string("stat-default")
        action = Gio.SimpleAction.new_stateful(
                 "stat_default", GLib.VariantType.new("s"),
                 GLib.Variant.new_string(stat_default))
        action.connect("activate", self.on_stat_default)
        self.add_action(action)
        
        # Shortcuts

        # TODO: be aware that a couple of shortcuts are defined in base.css

        self.set_accels_for_action("win.focus_mode", ["<Ctl>d"])
        self.set_accels_for_action("win.hemingway_mode", ["<Ctl>t"])
        self.set_accels_for_action("win.fullscreen", ["F11"])
        self.set_accels_for_action("win.find", ["<Ctl>f"])
        self.set_accels_for_action("win.find_replace", ["<Ctl>h"])
        self.set_accels_for_action("app.spellcheck", ["F7"])

        self.set_accels_for_action("win.new", ["<Ctl>n"])
        self.set_accels_for_action("win.open", ["<Ctl>o"])
        self.set_accels_for_action("win.save", ["<Ctl>s"])
        self.set_accels_for_action("win.save_as", ["<Ctl><shift>s"])
        self.set_accels_for_action("app.quit", ["<Ctl>w", "<Ctl>q"])

        # Inhibitor
        self.inhibitor = Inhibitor()

    def do_activate(self, *args, **kwargs):

        if not self.windows:
            self.settings.connect("changed", self.on_settings_changed)

        self.windows.append(MainWindow(self))

        if self._application_id == 'org.gnome.gitlab.somas.Apostrophe.Devel':
            for window in self.windows:
                window.get_style_context().add_class('devel')

        self._set_color_scheme()
        self.windows[-1].present()

    def do_handle_local_options(self, options):
        if options.contains("verbose") or self._application_id \
                == 'org.gnome.gitlab.somas.Apostrophe.Devel':

            set_up_logging(1)
        return -1

    def do_open(self, files, _n_files, _hint):
        self.activate()
        for i, file in enumerate(files):
            if i == 0:
                window = self.windows[0]
            else:
                window = MainWindow(self)
            window.load_file(file)
            window.present()
            self.windows.append(window)

    def _set_theme(self, settings, *_pspec):
        # Third party themes cause issues with Apostrophe custom stylesheets
        # If the user has a third party theme selected, we just change it to
        # Adwaita to prevent those issues

        # TODO: GTK4 - remove this
 
        theme_name = settings.get_property("gtk-theme-name")
        icon_theme_name = settings.get_property("gtk-icon-theme-name")

        if (theme_name not in ["Adwaita",
                               "HighContrast",
                               "HighContrastInverse"]):
            settings.set_property("gtk-theme-name", "Adwaita")

        if icon_theme_name != "Adwaita":
            settings.set_property("gtk-icon-theme-name", "Adwaita")

    def _set_color_scheme(self):

        # TODO: GTK4 - remove this
        theme = Theme.get_current()

        settings = Gtk.Settings.get_default()
        prefer_dark_theme = (theme.name == 'dark')
        settings.props.gtk_application_prefer_dark_theme = prefer_dark_theme

        if not self.windows:
            return

        self.style_provider.load_from_file(theme.gtk_css)

        if settings.props.gtk_theme_name == "HighContrast" and prefer_dark_theme:
            settings.props.gtk_theme_name = "HighContrastInverse"
        elif settings.props.gtk_theme_name == "HighContrastInverse" and not prefer_dark_theme:
            settings.props.gtk_theme_name = "HighContrast"

    def on_settings_changed(self, settings, key):
        # TODO: change this ffs
        if not self.windows:
            return
        if key == "color-scheme":
            self._set_color_scheme()
        elif key == "input-format":
            for window in self.windows:
                window.reload_preview()
        elif key == "sync-scroll":
            for window in self.windows:
                window.reload_preview(reshow=True)
        elif key == "stat-default":
            for window in self.windows:
                window.update_default_stat()

    def on_new_window(self, _action, _value):
        window = MainWindow(self)
        window.present()
        self.windows.append(window)

    def on_preferences(self, _action, _value):
        preferences_dialog = ApostrophePreferencesDialog()
        preferences_dialog.set_transient_for(self.get_active_window())
        preferences_dialog.show()

    def on_shortcuts(self, _action, _param):
        builder = Gtk.Builder()
        builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/ui/Shortcuts.ui")
        builder.get_object("shortcuts").set_transient_for(self.get_active_window())
        builder.get_object("shortcuts").show()

    def on_about(self, _action, _param):
        # TODO: what about non-csd
        builder = Gtk.Builder()
        builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/About.ui")
        about_dialog = builder.get_object("AboutDialog")
        about_dialog.set_transient_for(self.get_active_window())

        about_dialog.present()

    def on_quit(self, _action, _param):
        quit = True
        for window in self.windows:
            window.present()
            if window.on_delete_called(self):
                quit = False
        if quit:       
            self.quit()

    def on_stat_default(self, action, value):
        action.set_state(value)
        self.settings.set_string("stat-default", value.get_string())
