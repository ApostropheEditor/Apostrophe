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

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gettext import gettext as _

from gi.repository import Adw, Gdk, Gio, GLib, Gtk

from apostrophe.helpers import get_debug_info, set_up_logging
# from apostrophe.preferences_dialog import ApostrophePreferencesDialog
from apostrophe.inhibitor import Inhibitor
from apostrophe.main_window import MainWindow
from apostrophe.settings import Settings
from apostrophe.theme_switcher import Theme


class Application(Adw.Application):

    def __init__(self, application_id, *args, **kwargs):
        super().__init__(*args, application_id=application_id,
                         flags=Gio.ApplicationFlags.HANDLES_OPEN | Gio.ApplicationFlags.NON_UNIQUE,
                         **kwargs)

        self.add_main_option("verbose", b"v", GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Verbose output", None)

        self.set_resource_base_path("/org/gnome/gitlab/somas/Apostrophe")
        # gtk_settings = Gtk.Settings.get_default()

        self.windows = []
        self.settings = Settings.new()
        self.inhibitor = None
        self._application_id = application_id

    def do_startup(self):
        Adw.Application.do_startup(self)

        # Set css theme
        css_sepia_provider_file = Gio.File.new_for_uri(
            "resource:///org/gnome/gitlab/somas/Apostrophe/style-sepia.css")
        self.sepia_style_provider = Gtk.CssProvider()
        self.sepia_style_provider.load_from_file(css_sepia_provider_file)

        # Style manager
        style_manager = Adw.StyleManager.get_default()
        style_manager.connect("notify::dark", self._set_color_scheme)
        style_manager.connect("notify::high-contrast", self._set_color_scheme)

        # Set icons
        Gtk.IconTheme.get_for_display(
            Gdk.Display.get_default()).add_resource_path(
            "/org/gnome/gitlab/somas/Apostrophe/icons"
        )


        color_scheme = self.settings.get_string("color-scheme")
        action = Gio.SimpleAction.new_stateful(
                 "color_scheme", GLib.VariantType.new("s"),
                 GLib.Variant.new_string(color_scheme))
        action.connect("activate", self._set_color_scheme)
        self.add_action(action)

        action = Gio.SimpleAction.new("new_window", None)
        action.connect("activate", self.on_new_window)
        self.add_action(action)

        # action = Gio.SimpleAction.new("preferences", None)
        # action.connect("activate", self.on_preferences)
        # self.add_action(action)

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

        self.set_accels_for_action("app.new", ["<Ctl>n"])
        self.set_accels_for_action("win.open", ["<Ctl>o"])
        self.set_accels_for_action("win.save", ["<Ctl>s"])
        self.set_accels_for_action("win.save_as", ["<Ctl><shift>s"])
        self.set_accels_for_action("app.quit", ["<Ctl>w", "<Ctl>q"])

        # Inhibitor
        self.inhibitor = Inhibitor()

    def do_activate(self, *args, **kwargs):

        if not self.windows:
            self.settings.connect("changed", self.on_settings_changed)

            group = Gtk.WindowGroup.new()
            group.add_window(MainWindow(self))

            self.windows.append(group)

        if self._application_id == 'org.gnome.gitlab.somas.Apostrophe.Devel':
            for window_group in self.windows:
                for window in window_group.list_windows():
                    window.get_style_context().add_class('devel')

        self._set_color_scheme()
        self.windows[-1].list_windows()[-1].present()

    def do_handle_local_options(self, options):
        if options.contains("verbose") or self._application_id \
                == 'org.gnome.gitlab.somas.Apostrophe.Devel':
            set_up_logging(1)
        return -1

    def do_open(self, files, _n_files, _hint):
        self.activate()
        empty_window_groups = list(filter(lambda window_group: 
                                          window_group.list_windows()[0].textview.get_text() == "" and\
                                          not window_group.list_windows()[0].did_change, self.windows))
        for i, file in enumerate(files):
            if i < len(empty_window_groups):
                window = empty_window_groups[i].list_windows()[0]
            else:
                window = MainWindow(self)

                group = Gtk.WindowGroup.new()
                group.add_window(window)
                self.windows.append(group)

            window.load_file(file)
            window.present()

    def _set_color_scheme(self, *args, **kwargs):
        sepia = Theme.get_current().name == "sepia"

        if not self.windows:
            return

        if sepia:
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(), self.sepia_style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER)
        else:
            Gtk.StyleContext.remove_provider_for_display(
                Gdk.Display.get_default(), self.sepia_style_provider
            )

        # refresh markup colors
        for group in self.windows:
            group.list_windows()[0].textview.markup.on_style_updated()

    def on_settings_changed(self, settings, key):
        # TODO: change this ffs
        if not self.windows:
            return
        if key == "color-scheme":
            self._set_color_scheme()
        elif key == "input-format":
            for group in self.windows():
                 group.list_windows()[0].reload_preview()
        elif key == "sync-scroll":
            for group in self.windows():
                 group.list_windows()[0].reload_preview(reshow=True)
        elif key == "stat-default":
            for group in self.windows():
                 group.list_windows()[0].update_default_stat()

    def on_new_window(self, _action, _value):
        window = MainWindow(self)
        window.present()
        group = Gtk.WindowGroup.new()
        group.add_window(window)
        self.windows.append(group)

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

        about_dialog.set_debug_info(get_debug_info())
        about_dialog.add_link(_("Donate"), "https://paypal.me/manuelgenoves")
        about_dialog.add_link(_("Translations"), "https://l10n.gnome.org/module/apostrophe/")

        about_dialog.present()

    def on_quit(self, _action, _param):
        quit = True
        for group in self.windows:
            if group.list_windows()[0].do_close_request():
                quit = False
        if quit:
            self.quit()

    def on_stat_default(self, action, value):
        action.set_state(value)
        self.settings.set_string("stat-default", value.get_string())
