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
from collections import namedtuple
import gi # pylint: disable=wrong-import-position
from gi.repository import Gtk  # pylint: disable=E0611
from gettext import gettext as _

class headerbar():
    def main_headerbar(self):
        self.hb_container = Gtk.Frame(name='titlebar_container')
        self.hb_container.set_shadow_type(Gtk.ShadowType.NONE)
        self.hb_revealer = Gtk.Revealer(name='titlebar_revealer')
        self.hb = Gtk.HeaderBar()
        self.hb_revealer.add(self.hb)
        self.hb_revealer.props.transition_duration = 1000
        self.hb_revealer.props.transition_type = Gtk.RevealerTransitionType.CROSSFADE
        self.hb.props.show_close_button = True
        self.hb.get_style_context().add_class("titlebar")
        self.hb_container.add(self.hb_revealer)
        self.hb_container.show()
        self.set_titlebar(self.hb_container)
        self.hb_revealer.show()
        self.hb_revealer.set_reveal_child(True)
        self.hb.show()

        btn_recent.set_popup(self.generate_recent_files_menu())

        self.builder_window_menu = get_builder('Menu')
        self.model = self.builder_window_menu.get_object("Menu")
        btn_menu.set_menu_model(self.model)

        self.hb.pack_start(btn_new)
        self.hb.pack_start(btn_open)
        self.hb.pack_start(btn_recent)
        self.hb.pack_end(btn_menu)
        self.hb.pack_end(btn_search)
        self.hb.pack_end(btn_save)
        self.hb.show_all()

    def fs_headerbar(self):
        self.fullscr_events = self.builder.get_object("FullscreenEventbox")
        self.fullscr_hb_revealer = self.builder.get_object(
            "FullscreenHbPlaceholder")
        self.fullscr_hb = self.builder.get_object("FullscreenHeaderbar")
        self.fullscr_hb.get_style_context().add_class("titlebar")
        self.fullscr_hb_revealer.show()
        self.fullscr_hb_revealer.set_reveal_child(False)
        self.fullscr_hb.show()
        self.fullscr_events.hide()
       
        fs_btn_exit = Gtk.Button().new_from_icon_name("view-restore-symbolic",
                                                      Gtk.IconSize.BUTTON)
        fs_btn_exit.set_tooltip_text(_("Exit Fullscreen"))
        fs_btn_exit.set_action_name("app.fullscreen")

        self.builder_window_menu = get_builder('Menu')
        self.model = self.builder_window_menu.get_object("Menu")
        self.fs_btn_menu.set_menu_model(self.model)

        self.fullscr_hb.pack_start(fs_btn_new)
        self.fullscr_hb.pack_start(fs_btn_open)
        self.fullscr_hb.pack_start(self.fs_btn_recent)
        self.fullscr_hb.pack_end(fs_btn_exit)
        self.fullscr_hb.pack_end(self.fs_btn_menu)
        self.fullscr_hb.pack_end(fs_btn_search)
        self.fullscr_hb.pack_end(fs_btn_save)
        self.fullscr_hb.show_all()
        # this is a little tricky
        # we show hb when the cursor enters an area of 1 px at the top of the window
        # as the hb is shown the height of the eventbox grows to accomodate it
        self.fullscr_events.connect('enter_notify_event', self.show_fs_hb)
        self.fullscr_events.connect('leave_notify_event', self.hide_fs_hb)
        self.fs_btn_menu.get_popover().connect('closed', self.hide_fs_hb)

def buttons():
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
    btn.new.set_action_name("app.new")
    btn.open.set_action_name("app.open")
    btn.recent.set_action_name("app.open_recent")
    btn.save.set_action_name("app.save")
    btn.search.set_action_name("app.search")
    
    return btn