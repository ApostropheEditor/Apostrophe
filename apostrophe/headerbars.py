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
# with this program.  If not, see <http://www.gnu.org/licenses/>.
# END LICENSE
"""Manage all the headerbars related stuff
"""

from gettext import gettext as _

import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Adw, GLib, GObject, Gtk

from .open_popover import ApostropheOpenPopover
from .preview_layout_switcher import PreviewLayoutSwitcher
from .settings import Settings
from .theme_switcher import ThemeSwitcher


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/Headerbar.ui')
class BaseHeaderbar(Gtk.Revealer):

    __gtype_name__ = "BaseHeaderbar"

    """Base class for all headerbars
    """

    headerbar = Gtk.Template.Child()
    menu_button = Gtk.Template.Child()
    open_menu = Gtk.Template.Child()
    preview_layout_switcher = Gtk.Template.Child()

    is_fullscreen = GObject.property(type=bool, default=False)
    title = GObject.Property(type=str)
    subtitle = GObject.Property(type=str)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # TODO - move to ui file, check on start
        self.bind_property("is-fullscreen", self.headerbar, "show-start-title-buttons", 6)
        self.bind_property("is-fullscreen", self.headerbar, "show-end-title-buttons", 6)

        popover = self.menu_button.get_popover()
        popover.add_child(ThemeSwitcher(), "themeswitcher")

        self.settings = Settings.new()

        #self.select_preview_layout_row()