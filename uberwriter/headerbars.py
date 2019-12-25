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

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from uberwriter.helpers import get_descendant


class BaseHeaderbar:
    """Base class for all headerbars
    """
    def __init__(self, app):

        self.builder = Gtk.Builder()
        self.builder.add_from_resource(
            "/de/wolfvollprecht/UberWriter/ui/Headerbar.ui")

        self.hb = self.builder.get_object("Headerbar")
        self.hb_revealer = self.builder.get_object("titlebar_revealer")

        self.menu_button = self.builder.get_object("menu_button")
        self.recents_button = self.builder.get_object("recents_button")


class MainHeaderbar(BaseHeaderbar):  # pylint: disable=too-few-public-methods
    """Sets up the main application headerbar
    """

    def __init__(self, app):

        BaseHeaderbar.__init__(self, app)

        self.hb.set_show_close_button(True)

        add_menus(self, app)

        self.hb_revealer.props.transition_duration = 0


class FullscreenHeaderbar(BaseHeaderbar):
    """Sets up and manages the fullscreen headerbar and his events
    """

    def __init__(self, fs_builder, app):

        BaseHeaderbar.__init__(self, app)

        self.hb.set_show_close_button(False)

        self.exit_fs_button = self.builder.get_object("exit_fs_button")
        self.exit_fs_button.set_visible(True)

        add_menus(self, app)

        self.events = fs_builder.get_object("FullscreenEventbox")
        self.events.add(self.hb_revealer)

        # this is a little tricky
        # we show hb when the cursor enters an area of 1px at the top
        # as the hb is shown the height of the eventbox grows to accomodate it
        self.events.connect('enter_notify_event', self.show_fs_hb)
        self.events.connect('leave_notify_event', self.hide_fs_hb)
        self.menu_button.get_popover().connect('closed', self.hide_fs_hb)
        self.recents_button.get_popover().connect('closed', self.hide_fs_hb)

    def show_fs_hb(self, _widget=None, _data=None):
        """show headerbar of the fullscreen mode
        """
        self.hb_revealer.set_reveal_child(True)

    def hide_fs_hb(self, _widget=None, _data=None):
        """hide headerbar of the fullscreen mode
        """
        if (self.menu_button.get_active() or
           self.recents_button.get_active()):
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

        self.menu_button.set_sensitive(True)
        self.recents_button.set_sensitive(True)

    def show_dm_hb(self):
        """show dummy headerbar:
           It appears instantly to inmediatly fade away
        """
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
        "/de/wolfvollprecht/UberWriter/ui/Menu.ui")
    model = builder_window_menu.get_object("Menu")

    headerbar.menu_button.set_menu_model(model)

    # Add recents menu to the open recents button

    recents_builder = Gtk.Builder()
    recents_builder.add_from_resource(
        "/de/wolfvollprecht/UberWriter/ui/Recents.ui")
    recents = recents_builder.get_object("recent_md_popover")

    recents_treeview = get_descendant(recents, "recent_view", level=0)
    recents_treeview.set_activate_on_single_click(True)

    recents_wd = recents_builder.get_object("recent_md_widget")
    recents_wd.connect('item-activated', app.on_open_recent)

    headerbar.recents_button.set_popover(recents)
    headerbar.recents_button.set_sensitive(True)
