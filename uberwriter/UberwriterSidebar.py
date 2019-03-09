# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
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
### END LICENSE

import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# from plugins import plugins

import logging
logger = logging.getLogger('uberwriter')

class Shelve():
    """
    Shelve holds a collection of folders
    folders:
        List of folders
    name:
        descriptive name of shelve e.g. blog, notes etc.
    """

    name = ""
    folders = []

    def __init__(self, name, folders):
        self.name = name
        self.folders = folders

    def get_tree(self, store):
        node = {}
        for folder in self.folders:
            node[folder] = store.append(None, [os.path.basename(folder), folder])
            for root, dirs, files in os.walk(folder):
                logger.debug(root)
                for directory in dirs:
                    node[root + "/" + directory] = store.append(node[root], [directory, root + "/" + directory])
                for filename in files:
                    store.append(node[root], [filename, root + "/" + filename])


class UberwriterSidebar():
    """
    Presentational class for shelves and files managed by the "sidebar"

    parentwindow:
        Reference to UberwriterWindow
    """
    def __init__(self, parentwindow):
        """
        Initialize Treeview and Treestore
        """

        self.parentwindow = parentwindow
        self.paned_window = parentwindow.paned_window
        self.sidebar_box  = parentwindow.sidebar_box
        self.sidebar_open = True
        #         (GtkBox *box,
        # GtkWidget *child,
        # gboolean expand,
        # gboolean fill,
        # guint padding);
    
        self.shelve_store = Gtk.ListStore(str)
        self.shelve_store.append(["testshelve"])
        self.shelves_dropdown = Gtk.ComboBox.new_with_model_and_entry(self.shelve_store)
        
        self.sidebar_box.pack_start(self.shelves_dropdown, False, False, 5)

        self.sidebar_scrolledwindow = Gtk.ScrolledWindow()
        self.sidebar_scrolledwindow.set_hexpand(True)
        self.sidebar_scrolledwindow.set_vexpand(True)

        self.store = Gtk.TreeStore(str, str)
        self.active_shelf = Shelve("testshelve", ["/home/wolf/Documents/asd/"])
        self.active_shelf.get_tree(self.store)

        self.treeview = Gtk.TreeView(self.store)
        self.treeview.set_headers_visible(False)
        # expand first folder (root folder, but not children)
        self.treeview.expand_row(Gtk.TreePath.new_from_string("0"), False)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0)
        self.treeview.append_column(column)
        # new selection
        self.treeview.connect('cursor_changed', self.get_selected_file)
        # right click handler
        self.treeview.connect('button-press-event', self.handle_button_press)
        self.treeview.show()

        self.sidebar_scrolledwindow.add(self.treeview)        
        self.sidebar_box.pack_start(self.sidebar_scrolledwindow, True, True, 5)

        self.menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.menu_button = Gtk.MenuButton.new()

        # TODO refactor
        mb_menu = Gtk.Menu.new()
        mitem = Gtk.MenuItem.new_with_label('etstasd asd as d')
        mitem.show()
        mb_menu.append(mitem)
        mb_menu.show()

        self.menu_button.set_popup(mb_menu)

        self.menu_box.pack_start(self.menu_button, False, False, 5)
        self.sidebar_box.pack_end(self.menu_box, False, False, 5)

        self.sidebar_box.show_all()
        self.paned_window.pack1(self.sidebar_box, True, True);
        self.paned_window.show_all()


    def get_selected_file(self, widget, data=None):
        """
        Handle left click on file
        """
        selection = self.treeview.get_selection()
        if not selection:
            return
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        treemodel, treeiter = selection.get_selected()
        selected_file = treemodel.get_value(treeiter, 1)
        self.parentwindow.load_file(selected_file)
        logger.debug(selected_file)

    def handle_button_press(self, widget, event):
        """
        Handle right click (context menu)
        """
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            # reference to self to not have it garbage collected
            self.popup = Gtk.Menu.new()
            pathinfo = self.treeview.get_path_at_pos(event.x, event.y)
            if pathinfo:
                path, col, cellx, celly = pathinfo
                treeiter = self.store.get_iter(path)
                filename = self.store.get_value(treeiter, 1)
                item = Gtk.MenuItem.new()
                item.set_label("Open ...")
                # item.connect("activate", self.context_menu_open_file)
                # item.filename = filename
                item.show()
                #  self.popup.append(item)
            self.popup.show()
            self.popup.popup(None, None, None, None, event.button, event.time)
            return True

    def get_treeview(self):
        """
        Return Treeview to append to scrolled window
        """
        return self.treeview


    def context_menu_open_file(self, widget, data=None):
        """
        Open selected file with xdg-open
        """
        selected_file = widget.filename
        subprocess.call(["xdg-open", selected_file])

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.close_sidebar()
        else:
            self.open_sidebar()


    def open_sidebar(self):
        # self.paned_window.set_property('min-position', 0)
        self.paned_window.set_position(200)
        self.sidebar_open = True


    def close_sidebar(self):
        # self.paned_window.set_property('min-position', 0)
        self.paned_window.set_position(0)
        self.sidebar_open = False