# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
# Copyright (C) 2012, Wolf Vollprecht <w.vollprecht@gmail.com>
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

from collections import namedtuple
from gettext import gettext as _
from gi.repository import Gtk
from uberwriter_lib.helpers import get_builder


class MainHeaderbar:  #pylint: disable=too-few-public-methods
    """Sets up the main application headerbar
    """

    def __init__(self):
        self.hb = Gtk.HeaderBar().new() #pylint: disable=C0103
        self.hb.props.show_close_button = True
        self.hb.get_style_context().add_class("titlebar")

        self.hb_revealer = Gtk.Revealer(name='titlebar_revealer')
        self.hb_revealer.add(self.hb)
        self.hb_revealer.props.transition_duration = 1000
        self.hb_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE
        self.hb_revealer.show()
        self.hb_revealer.set_reveal_child(True)

        self.hb_container = Gtk.Frame(name='titlebar_container')
        self.hb_container.set_shadow_type(Gtk.ShadowType.NONE)
        self.hb_container.add(self.hb_revealer)
        self.hb_container.show()

        btns = buttons()
        pack_buttons(self.hb, btns)

        # btns.recent.set_popup(self.generate_recent_files_menu())

        self.hb.show_all()


class FsHeaderbar:
    """Sets up and manages the fullscreen headerbar and his events
    """

    def __init__(self, builder):
        self.events = builder.get_object("FullscreenEventbox")
        self.revealer = builder.get_object(
            "FullscreenHbPlaceholder")
        self.revealer.show()
        self.revealer.set_reveal_child(False)

        self.hb = builder.get_object("FullscreenHeaderbar") #pylint: disable=C0103
        self.hb.get_style_context().add_class("titlebar")
        self.hb.show()
        self.events.hide()

        self.btns = buttons()

        fs_btn_exit = Gtk.Button().new_from_icon_name("view-restore-symbolic",
                                                      Gtk.IconSize.BUTTON)
        fs_btn_exit.set_tooltip_text(_("Exit Fullscreen"))
        fs_btn_exit.set_action_name("app.fullscreen")

        pack_buttons(self.hb, self.btns, fs_btn_exit)

        self.hb.show_all()

        # this is a little tricky
        # we show hb when the cursor enters an area of 1 px at the top of the window
        # as the hb is shown the height of the eventbox grows to accomodate it
        self.events.connect('enter_notify_event', self.show_fs_hb)
        self.events.connect('leave_notify_event', self.hide_fs_hb)
        self.btns.menu.get_popover().connect('closed', self.hide_fs_hb)

    def show_fs_hb(self, _widget, _data=None):
        """show headerbar of the fullscreen mode
        """
        self.revealer.set_reveal_child(True)

    def hide_fs_hb(self, _widget, _data=None):
        """hide headerbar of the fullscreen mode
        """
        if self.btns.menu.get_active():
            pass
        else:
            self.revealer.set_reveal_child(False)

def buttons():
    """constructor for the headerbar buttons

    Returns:
        [NamedTupple] -- tupple of Gtk.Buttons
    """
    builder_window_menu = get_builder('Menu')
    model = builder_window_menu.get_object("Menu")

    Button = namedtuple("Button", "new open recent save search menu")
    btn = Button(Gtk.Button().new_with_label(_("New")),
                 Gtk.Button().new_with_label(_("Open")),
                 Gtk.MenuButton().new(),
                 Gtk.Button().new_with_label(_("Save")),
                 Gtk.Button().new_from_icon_name("system-search-symbolic",
                                                 Gtk.IconSize.BUTTON),
                 Gtk.MenuButton().new())

    btn.recent.set_image(Gtk.Image.new_from_icon_name("go-down-symbolic",
                                                      Gtk.IconSize.BUTTON))
    btn.recent.set_tooltip_text(_("Open Recent"))
    btn.search.set_tooltip_text(_("Search and replace"))
    btn.menu.set_tooltip_text(_("Menu"))
    btn.menu.set_image(Gtk.Image.new_from_icon_name("open-menu-symbolic",
                                                    Gtk.IconSize.BUTTON))
    btn.menu.set_use_popover(True)
    btn.menu.set_menu_model(model)
    btn.new.set_action_name("app.new")
    btn.open.set_action_name("app.open")
    btn.recent.set_action_name("app.open_recent")
    btn.save.set_action_name("app.save")
    btn.search.set_action_name("app.search")

    return btn

def pack_buttons(headerbar, btn, btn_exit=None):
    """Pack the given buttons in the given headerbar

    Arguments:
        headerbar {Gtk.HeaderBar} -- The headerbar where to put the buttons
        btn {Tupple of Gtk.Buttons} -- The buttons to pack

    Keyword Arguments:
        btn_exit {Gtk.Button} -- Optional exit fullscreen button (default: {None})
    """

    headerbar.pack_start(btn.new)
    headerbar.pack_start(btn.open)
    headerbar.pack_start(btn.recent)
    if btn_exit:
        headerbar.pack_end(btn_exit)
    headerbar.pack_end(btn.menu)
    headerbar.pack_end(btn.search)
    headerbar.pack_end(btn.save)
