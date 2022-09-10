# BEGIN LICENSE
# Copyright (C) 2022, Manuel Genovés <manuel.genoves@gmail.com>
# Copyright (C) 2021, Adrien Plazas <kekun.plazas@laposte.net>
# Copyright (C) 2021, Alexander Mikhaylenko <exalm7659@gmail.com>
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

import enum
from enum import IntEnum
from gettext import gettext as _

import gi
from gi.repository import GObject, Gtk

from apostrophe.settings import Settings

gi.require_version('Gtk', '4.0')


class PreviewLayout(IntEnum):

    # preview modes
    FULL_WIDTH = 0
    HALF_WIDTH = 1
    HALF_HEIGHT = 2
    WINDOWED = 3

    def get_text(self):
        if self == PreviewLayout.FULL_WIDTH:
            return _("Full-Width")
        elif self == PreviewLayout.HALF_WIDTH:
            return _("Half-Width")
        elif self == PreviewLayout.HALF_HEIGHT:
            return _("Half-Height")
        elif self == PreviewLayout.WINDOWED:
            return _("Windowed")
        else:
            raise ValueError("Unknown preview mode")

    def get_icon(self):
        if self == PreviewLayout.FULL_WIDTH:
            return "preview-layout-full-width-symbolic"
        elif self == PreviewLayout.HALF_WIDTH:
            return "preview-layout-half-width-symbolic"
        elif self == PreviewLayout.HALF_HEIGHT:
            return "preview-layout-half-height-symbolic"
        elif self == PreviewLayout.WINDOWED:
            return "preview-layout-windowed-symbolic"
        else:
            raise ValueError("Unknown preview mode")


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/PreviewLayoutSwitcherItem.ui')
class PreviewLayoutSwitcherItem(Gtk.ListBoxRow):
    __gtype_name__ = "PreviewLayoutSwitcherItem"

    icon = Gtk.Template.Child()
    title = Gtk.Template.Child()
    checkmark = Gtk.Template.Child()
    selected = GObject.property(type=bool, default=False)

    def __init__(self, _layout):
        super().__init__()
        self.layout = _layout
        self.icon.set_from_icon_name(self.layout.get_icon())
        self.title.set_label(self.layout.get_text())

        self.connect("notify::selected", self.on_selected)

    def on_selected(self, *args, **kwargs):
        self.checkmark.props.opacity = 1 if self.selected else 0


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/PreviewLayoutSwitcher.ui')
class PreviewLayoutSwitcher(Gtk.Box):
    __gtype_name__ = "PreviewLayoutSwitcher"

    list_box = Gtk.Template.Child()
    layout_image = Gtk.Template.Child()
    layout_popover = Gtk.Template.Child()
    preview_switcher_toggle = Gtk.Template.Child()
    items = []

    preview_layout = GObject.property(type=int)
    settings = Settings.new()

    def __init__(self):
        super().__init__()

        for i, layout in enumerate(PreviewLayout):
            item = PreviewLayoutSwitcherItem(layout)
            self.list_box.append(item)
            self.items.append(item)

        self.update_ui()
        self.connect("notify::preview-layout", self.update_ui)

    @Gtk.Template.Callback()
    def update_ui(self, *args, **kwargs):
        self.layout_image.set_from_icon_name(PreviewLayout(self.preview_layout).get_icon())

        for item in self.items:
            item.selected = item.layout == self.preview_layout

        item = self.items[self.preview_layout]
        self.list_box.select_row(item)

    @Gtk.Template.Callback()
    def on_row_activated(self, _listbox, row):
        self.preview_layout = row.layout
        self.layout_popover.popdown()
