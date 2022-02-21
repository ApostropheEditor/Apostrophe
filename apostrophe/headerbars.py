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

import gi

from gettext import gettext as _

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject, Handy
from .settings import Settings
from .theme_switcher import ThemeSwitcher
from .preview_layout_switcher import PreviewLayoutSwitcher
from .open_popover import ApostropheOpenPopover


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/Headerbar.ui')
class BaseHeaderbar(Gtk.Revealer):

    __gtype_name__ = "BaseHeaderbar"

    """Base class for all headerbars
    """

    headerbar = Gtk.Template.Child()
    tutorial_button = Gtk.Template.Child()
    preview_layout_switcher = Gtk.Template.Child()

    is_fullscreen = GObject.property(type=bool, default=False)
    title = GObject.Property(type=str)
    subtitle = GObject.Property(type=str)

    @GObject.Property(type=int)
    def allocated_height(self):
        return self.get_allocated_height()

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.bind_property("is-fullscreen", self.headerbar, "show-close-button", 6)

        tutorial = GLib.Variant.new_string("resource:///org/gnome/gitlab/somas/"
                                           "Apostrophe/media/apostrophe_markdown.md")
        self.tutorial_button.set_action_target_value(tutorial)

        self.settings = Settings.new()

        #self.select_preview_layout_row()
    @Gtk.Template.Callback()
    def on_show_hide(self, widget, event):
        ''' The crossfade animation doesn't hide the alocated space
            for the headerbar. This prevents having an empty space there
        '''
        if not self.get_child_revealed():
            self.set_visible(False)
