# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
# Copyright (C) 2019, Wolf Vollprecht <w.vollprecht@gmail.com>
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
from gi.repository import Gtk, GLib
from apostrophe.helpers import get_descendant
from apostrophe.settings import Settings


class BaseHeaderbar:
    """Base class for all headerbars
    """
    # preview modes
    FULL_WIDTH = 0
    HALF_WIDTH = 1
    HALF_HEIGHT = 2
    WINDOWED = 3

    def __init__(self, app):

        self.settings = Settings.new()

        self.builder = Gtk.Builder()
        self.builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/ui/Headerbar.ui")
        self.builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/ui/ExportPopover.ui")

        self.hb = self.builder.get_object(
            "Headerbar")
        self.hb_revealer = self.builder.get_object(
            "titlebar_revealer")

        self.preview_toggle_revealer = self.builder.get_object(
            "preview_switch_revealer")
        self.preview_switcher_icon = self.builder.get_object(
            "preview_switch_toggle_icon")

        self.__populate_layout_switcher_menu()
        self.update_preview_layout_icon()

        self.sync_scroll_switch = self.builder.get_object("sync_scroll_switch")
        self.sync_scroll_switch.set_active(self.settings.get_value("sync-scroll"))
        self.sync_scroll_switch.connect("state-set", self.__on_sync_scroll)

        self.menu_button = self.builder.get_object("menu_button")
        self.recents_button = self.builder.get_object("recents_button")
        self.export_button = self.builder.get_object("export_button")
        export_popover = self.builder.get_object("export_menu")        
        self.preview_switch_button = self.builder.get_object("preview_switch_button")

        self.export_button.set_popover(export_popover)

        add_menus(self, app)

        settings = Gtk.Settings.get_default()
        # TODO: use walrust operator whenever Python3.8 lands on SDK
        # if global_dark:= settings.props.gtk_theme_name.endswith("-dark"):
        global_dark = settings.props.gtk_theme_name.endswith("-dark")
        if global_dark:
            self.light_button.set_sensitive(False)
            self.light_button.set_tooltip_text(_(
                "Light mode isn’t available while using a dark global theme"))

        self.dark_button.set_active(self.settings.get_boolean("dark-mode") or global_dark)

        self.light_button.connect("toggled", self.__on_dark_mode)

        self.select_preview_layout_row()

    def update_preview_layout_icon(self):
        mode = self.settings.get_enum("preview-mode")
        self.preview_switcher_icon.set_from_icon_name(
            self.__get_icon_for_preview_mode(mode), 4)

    def select_preview_layout_row(self):
        mode = self.settings.get_enum("preview-mode")
        row = self.preview_menu.get_row_at_index(mode)
        self.preview_menu.select_row(row)

    def __populate_layout_switcher_menu(self):
        self.preview_menu = self.builder.get_object("preview_switch_options")
        modes = self.settings.props.settings_schema.get_key("preview-mode").get_range()[1]

        for i, mode in enumerate(modes):
            item_builder = Gtk.Builder()
            item_builder.add_from_resource(
                "/org/gnome/gitlab/somas/Apostrophe/ui/PreviewLayoutSwitcherItem.ui")
            menu_item = item_builder.get_object("switcherItem")

            menu_item.label = item_builder.get_object("label")
            menu_item.label.set_text(self.__get_text_for_preview_mode(i))

            menu_item.icon = item_builder.get_object("icon")
            menu_item.icon.set_from_icon_name(self.__get_icon_for_preview_mode(i), 16)

            menu_item.set_action_name("app.preview_mode")
            menu_item.set_action_target_value(GLib.Variant.new_string(mode))

            menu_item.show_all()
            self.preview_menu.insert(menu_item, -1)

    def __get_text_for_preview_mode(self, mode):
        if mode == self.FULL_WIDTH:
            return _("Full-Width")
        elif mode == self.HALF_WIDTH:
            return _("Half-Width")
        elif mode == self.HALF_HEIGHT:
            return _("Half-Height")
        elif mode == self.WINDOWED:
            return _("Windowed")
        else:
            raise ValueError("Unknown preview mode {}".format(mode))

    def __get_icon_for_preview_mode(self, mode):
        if mode == self.FULL_WIDTH:
            return "preview-layout-full-width-symbolic"
        elif mode == self.HALF_WIDTH:
            return "preview-layout-half-width-symbolic"
        elif mode == self.HALF_HEIGHT:
            return "preview-layout-half-height-symbolic"
        elif mode == self.WINDOWED:
            return "preview-layout-windowed-symbolic"
        else:
            raise ValueError("Unknown preview mode {}".format(mode))

    def __on_sync_scroll(self, _, state):
        self.settings.set_boolean("sync-scroll", state)
        return False

    def __on_dark_mode(self, _):
        self.settings.set_boolean("dark-mode", self.dark_button.get_active())

class MainHeaderbar(BaseHeaderbar):  # pylint: disable=too-few-public-methods
    """Sets up the main application headerbar
    """

    def __init__(self, app):

        BaseHeaderbar.__init__(self, app)

        self.hb.set_show_close_button(True)

        self.hb_revealer.props.transition_duration = 0


class FullscreenHeaderbar(BaseHeaderbar):
    """Sets up and manages the fullscreen headerbar and his events
    """

    def __init__(self, fs_builder, app):

        BaseHeaderbar.__init__(self, app)

        self.hb.set_show_close_button(False)

        self.exit_fs_button = self.builder.get_object("exit_fs_button")
        self.exit_fs_button.set_visible(True)

        self.events = fs_builder.get_object("FullscreenEventbox")
        self.events.add(self.hb_revealer)

        # this is a little tricky
        # we show hb when the cursor enters an area of 1px at the top
        # as the hb is shown the height of the eventbox grows to accomodate it
        self.events.connect('enter_notify_event', self.show_fs_hb)
        self.events.connect('leave_notify_event', self.hide_fs_hb)
        self.menu_button.get_popover().connect('closed', self.hide_fs_hb)
        self.recents_button.get_popover().connect('closed', self.hide_fs_hb)
        self.export_button.get_popover().connect('closed', self.hide_fs_hb)
        self.preview_switch_button.get_popover().connect('closed', self.hide_fs_hb)

    def show_fs_hb(self, _widget=None, _data=None):
        """show headerbar of the fullscreen mode
        """
        self.hb_revealer.set_reveal_child(True)

    def hide_fs_hb(self, _widget=None, _data=None):
        """hide headerbar of the fullscreen mode
        """
        if (self.menu_button.get_active() or
                self.recents_button.get_active() or
                self.export_button.get_active() or
                self.preview_switch_button.get_active()):
            pass
        else:
            self.hb_revealer.set_reveal_child(False)


class DummyHeaderbar(BaseHeaderbar):
    """Sets up and manages the dummy headerbar wich fades away when entering
       the free-distracting mode
    """

    def __init__(self, app):

        BaseHeaderbar.__init__(self, app)

        self.hb.set_show_close_button(True)
        self.hb_revealer.set_transition_type(
            Gtk.RevealerTransitionType.CROSSFADE)
        self.hb_revealer.set_reveal_child(False)
        self.hb_revealer.hide()

        self.menu_button.set_sensitive(True)
        self.recents_button.set_sensitive(True)

    def show_dm_hb(self):
        """show dummy headerbar:
           It appears instantly to inmediatly fade away
        """
        self.hb_revealer.show()
        self.hb_revealer.set_transition_duration(0)
        self.hb_revealer.set_reveal_child(True)
        self.hb_revealer.set_transition_duration(600)
        self.hb_revealer.set_reveal_child(False)

    def hide_dm_hb(self):
        """hide dummy headerbar
           It appears slowly to inmediatly dissapear
        """
        self.hb_revealer.set_transition_duration(400)
        self.hb_revealer.set_reveal_child(True)
        GLib.timeout_add(400, self.hide_dm_hb_with_wait)

    def hide_dm_hb_with_wait(self):
        self.hb_revealer.set_transition_duration(0)
        self.hb_revealer.set_reveal_child(False)
        self.hb_revealer.hide()
        return False


class PreviewHeaderbar:
    """Sets up the preview headerbar
    """

    def __init__(self):
        self.hb = Gtk.HeaderBar().new()
        self.hb.props.show_close_button = True
        self.hb.get_style_context().add_class("titlebar")

        self.hb_revealer = Gtk.Revealer(name="titlebar-revealer-pv")
        self.hb_revealer.add(self.hb)
        self.hb_revealer.props.transition_duration = 750
        self.hb_revealer.set_transition_type(
            Gtk.RevealerTransitionType.CROSSFADE)
        self.hb_revealer.show()
        self.hb_revealer.set_reveal_child(True)

        self.hb_container = Gtk.Frame(name="titlebar-container")
        self.hb_container.set_shadow_type(Gtk.ShadowType.NONE)
        self.hb_container.add(self.hb_revealer)
        self.hb_container.show()

        self.hb.show_all()


def add_menus(headerbar, app):
    """ Add menu models to hb buttons
    """

    # Add menu model to the menu button

    builder_window_menu = Gtk.Builder()
    builder_window_menu.add_from_resource(
        "/org/gnome/gitlab/somas/Apostrophe/ui/Menu.ui")
    model = builder_window_menu.get_object("Menu")
    headerbar.light_button = builder_window_menu.get_object("light_mode_button")
    headerbar.dark_button = builder_window_menu.get_object("dark_mode_button")

    headerbar.menu_button.set_popover(model)

    # Add recents menu to the open recents button

    recents_builder = Gtk.Builder()
    recents_builder.add_from_resource(
        "/org/gnome/gitlab/somas/Apostrophe/ui/Recents.ui")
    recents = recents_builder.get_object("recent_md_popover")

    recents_treeview = get_descendant(recents, "recent_view", level=0)
    recents_treeview.set_activate_on_single_click(True)

    recents_wd = recents_builder.get_object("recent_md_widget")
    recents_wd.connect('item-activated', app.on_open_recent)

    headerbar.recents_button.set_popover(recents)
    headerbar.recents_button.set_sensitive(True)
