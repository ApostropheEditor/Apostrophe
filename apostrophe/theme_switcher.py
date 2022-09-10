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

gi.require_version('Gtk', '4.0')
from gi.repository import Adw, Gio, GObject, Gtk

from apostrophe.helpers import get_media_path

from .settings import Settings


class Theme:
    '''Abstracts getters for the current theme related
    resources'''

    settings = Settings.new()

    def __init__(self, name, web_css):
        self.name    = name
        self.web_css = web_css

    @classmethod
    def get_current(cls):
        current_theme = defaultThemes[0]
        color_scheme = cls.settings.get_string("color-scheme")
        for theme in defaultThemes:
            if color_scheme == theme.name:
                current_theme = theme
        return current_theme

defaultThemes = [
    Theme('light', get_media_path('/media/css/web/adwaita.css')),
    Theme('dark',  get_media_path('/media/css/web/adwaita.css')),
    Theme('sepia', get_media_path('/media/css/web/adwaita-sepia.css')),
]



@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/ThemeSwitcher.ui')
class ThemeSwitcher(Gtk.Box):
    __gtype_name__ = "ThemeSwitcher"

    color_scheme = "light"

    system_selector = Gtk.Template.Child()
    light_selector = Gtk.Template.Child()
    sepia_selector = Gtk.Template.Child()
    dark_selector = Gtk.Template.Child()

    settings = Settings.new()

    show_system = GObject.property(type=bool, default=True)

    @GObject.Property(type=str)
    def selected_color_scheme(self):
        """Read-write integer property."""

        return self.color_scheme

    @selected_color_scheme.setter
    def selected_color_scheme(self, color_scheme):
        self.color_scheme = color_scheme

        if color_scheme == "auto":
            self.system_selector.set_active(True)
            self.style_manager.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)
        if color_scheme == "light":
            self.light_selector.set_active(True)
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        if color_scheme == "sepia":
            self.sepia_selector.set_active(True)
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        if color_scheme == "dark":
            self.dark_selector.set_active(True)
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.style_manager = Adw.StyleManager.get_default()

        color_scheme = self.settings.get_string("color-scheme")
        self.color_scheme = color_scheme

        self.settings.bind(
            "color-scheme",
            self,
            "selected_color_scheme",
            Gio.SettingsBindFlags.DEFAULT)

        self.style_manager.bind_property("system-supports-color-schemes",
                                         self, "show_system",
                                         GObject.BindingFlags.SYNC_CREATE)

    @Gtk.Template.Callback()
    def _on_color_scheme_changed(self, widget, paramspec):
        if self.system_selector.get_active():
            self.selected_color_scheme = "auto"
        if self.light_selector.get_active():
            self.selected_color_scheme = "light"
        if self.sepia_selector.get_active():
            self.selected_color_scheme = "sepia"
        if self.dark_selector.get_active():
            self.selected_color_scheme = "dark"
