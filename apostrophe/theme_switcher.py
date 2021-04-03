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


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/ThemeSwitcher.ui')
class ThemeSwitcher(Gtk.Box):
    __gtype_name__ = "ThemeSwitcher"

    color_scheme = "light"

    light_mode_button = Gtk.Template.Child()
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
        if self.dark_mode_button.get_active():
            self.selected_color_scheme = "dark"
