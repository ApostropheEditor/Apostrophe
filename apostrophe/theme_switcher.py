# BEGIN LICENSE
# Copyright 2020, Manuel Genovés <manuel.genoves@gmail.com>
#
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
# with this program.  If not, see <http://www.gnu.org/licenses/>.
# END LICENSE

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio

from .settings import Settings
from apostrophe.helpers import get_media_path

class Theme:
    '''Abstracts getters for the current theme related
    resources'''

    settings = Settings.new()

    def __init__(self, name, gtk_css, web_css):
        self.name = name
        self.gtk_css = gtk_css
        self.web_css = web_css

    @classmethod
    def get_for_name(cls, name, default=None):
        current_theme = default or defaultThemes[0]
        for theme in defaultThemes:
            if name == theme.name:
                current_theme = theme
        return current_theme

    @classmethod
    def get_current(cls):
        color_scheme = cls.settings.get_string("color-scheme")
        return cls.get_for_name(color_scheme)

defaultThemes = [
    Theme('light', Gio.File.new_for_uri("resource:///org/gnome/gitlab/somas/Apostrophe/media/css/gtk/Adwaita.css"),
          get_media_path('/media/css/web/adwaita.css')),
    Theme('dark', Gio.File.new_for_uri("resource:///org/gnome/gitlab/somas/Apostrophe/media/css/gtk/Adwaita-dark.css"),
          get_media_path('/media/css/web/adwaita.css')),
    Theme('sepia', Gio.File.new_for_uri("resource:///org/gnome/gitlab/somas/Apostrophe/media/css/gtk/Adwaita-sepia.css"),
          get_media_path('/media/css/web/adwaita-sepia.css')),
]



@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/ThemeSwitcher.ui')
class ThemeSwitcher(Gtk.Box):
    __gtype_name__ = "ThemeSwitcher"

    color_scheme = "light"

    light_mode_button = Gtk.Template.Child()
    sepia_mode_button = Gtk.Template.Child()
    dark_mode_button = Gtk.Template.Child()

    settings = Settings.new()

    @GObject.Property(type=str)
    def selected_color_scheme(self):
        """Read-write integer property."""

        return self.color_scheme

    @selected_color_scheme.setter
    def selected_color_scheme(self, color_scheme):
        self.color_scheme = color_scheme

        if color_scheme == "light":
            self.light_mode_button.set_active(True)
        if color_scheme == "sepia":
            self.sepia_mode_button.set_active(True)
        if color_scheme == "dark":
            self.dark_mode_button.set_active(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        color_scheme = self.settings.get_string("color-scheme")
        self.color_scheme = color_scheme

        self.settings.bind(
            "color-scheme",
            self,
            "selected_color_scheme",
            Gio.SettingsBindFlags.DEFAULT)

    @Gtk.Template.Callback()
    def _on_color_scheme_changed(self, widget, paramspec):
        if self.light_mode_button.get_active():
            self.selected_color_scheme = "light"
        if self.sepia_mode_button.get_active():
            self.selected_color_scheme = "sepia"
        if self.dark_mode_button.get_active():
            self.selected_color_scheme = "dark"
