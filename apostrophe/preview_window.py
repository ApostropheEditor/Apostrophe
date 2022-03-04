# Copyright (C) 2021, Manuel Genovés <manuel.genoves@gmail.com>
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
from gi.repository import Gtk, Gdk, GObject, GLib, Gio, Handy


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/PreviewWindow.ui')
class PreviewWindow(Handy.ApplicationWindow):

    __gtype_name__ = "ApostrophePreviewWindow"

    preview_box = Gtk.Template.Child()

    def __init__(self):
        super().__init__(application=Gio.Application.get_default(),
                         title="Preview")
