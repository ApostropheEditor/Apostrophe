# Copyright (C) 2022, Manuel Genovés <manuel.genoves@gmail.com>
#               2021, Christian Hergert <chergert@redhat.com>
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
"""Open/recents popover
"""

from os import close
import gi

from gettext import gettext as _

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, GObject, Handy
from .settings import Settings

class RecentItem(GObject.Object):
    def __init__(self, name, path, uri, **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.path: str = path
        self.uri: str = uri

@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/Recents.ui')
class ApostropheOpenPopover(Gtk.Popover):

    __gtype_name__ = "ApostropheOpenPopover"

    """Open/recents popover
    """

    list_box = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    empty = Gtk.Template.Child()
    recent = Gtk.Template.Child()


    model = Gio.ListStore.new(RecentItem)
    recents_manager = Gtk.RecentManager.get_default()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.list_box.bind_model(self.model, self.create_row)

        self.on_manager_changed()
        self.recents_manager.connect("changed", self.on_manager_changed)

    def create_row(self, item, **args):
        row = Handy.ActionRow.new()
        row.item = item
        row.set_title(item.name)
        row.set_subtitle(item.path)

        delete_button = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        delete_button.get_style_context().add_class("flat")
        delete_button.get_style_context().add_class("circular")
        delete_button.set_valign(Gtk.Align.CENTER)
        delete_button.set_visible(True)
        delete_button.connect("clicked", self.on_delete_click, item)

        row.add(delete_button)
        row.set_activatable(True)
        row.set_action_name("win.open_file")
        row.set_action_target_value(GLib.Variant.new_string(item.uri))

        return row

    def on_manager_changed(self, *args, **kwargs):
        self.model.remove_all()
        for item in self.recents_manager.get_items():
            self.model.append(RecentItem(item.get_display_name(), item.get_uri_display(), item.get_uri()))

        self.stack.set_visible_child(self.recent if self.model else self.empty)

    @Gtk.Template.Callback()
    def on_search_entry_changed_cb(self, search_entry):
        # TODO: implement nice filters in GTK4
        recents_list = self.recents_manager.get_items()
        filtered_list = filter(lambda item: search_entry.get_text() in item.get_display_name(), recents_list)

        self.model.remove_all()
        for item in filtered_list:
            self.model.append(RecentItem(item.get_display_name(), item.get_uri_display(), item.get_uri()))

    @Gtk.Template.Callback()
    def on_search_entry_activate_cb(self, *arg, **kwargs):
        print("activate")

    @Gtk.Template.Callback()
    def on_search_entry_stop_cb(self, *arg, **kwargs):
        print("stop")

    def on_delete_click(self, _widget, item):
        self.recents_manager.remove_item(item.uri)