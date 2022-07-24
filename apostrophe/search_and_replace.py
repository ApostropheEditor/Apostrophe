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

import logging
import re

import gi

from apostrophe.helpers import user_action

gi.require_version('Gtk', '4.0')
from gi.repository import Adw, GObject, Gtk

LOGGER = logging.getLogger('apostrophe')

@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/SearchBar.ui')
class ApostropheSearchBar(Adw.Bin):
    """
    Adds (regex) search and replace functionality to
    apostrophe
    """
    __gtype_name__ = "ApostropheSearchBar"

    replace_mode_enabled = GObject.property(type=bool, default=False)
    search_mode_enabled = GObject.property(type=bool, default=False)
    searchbar = Gtk.Template.Child()
    search_entry = Gtk.Template.Child()
    regex = Gtk.Template.Child()
    case_sensitive = Gtk.Template.Child()
    replace_entry = Gtk.Template.Child()

    def __init__(self):
        self.textbuffer = None

        self.matches = []
        self.active = 0

        # contruct a paintable to check size changes
        self.paintable = Gtk.WidgetPaintable.new(self)
        self.paintable.connect("invalidate-size", self.update_textview_margin)

        self.connect("notify::search-mode-enabled", self.search_enabled)
        self.connect("notify::replace-mode-enabled", self.replace_enabled)

    def attach(self, textview):
        self.textview = textview
        self.textbuffer = self.textview.get_buffer()
        self.highlight = self.textbuffer.create_tag('search_highlight',
                                                    background="yellow")

    def search_enabled(self, *args, **kwargs):
        if self.searchbar.get_search_mode():
            self.textbuffer = self.textview.get_buffer()
            if self.textbuffer.get_has_selection():
                self.search_entry.set_text(self.textbuffer.get_slice(*self.textbuffer.get_selection_bounds(), False))
            self.search_entry.grab_focus()
            self.search()
        else:
            self.textbuffer.remove_tag(self.highlight,
                                   self.textbuffer.get_start_iter(),
                                   self.textbuffer.get_end_iter())
            self.matches = []
            self.replace_mode_enabled = False
            self.textview.grab_focus()

    def replace_enabled(self, _widget, _data):
        if self.replace_mode_enabled and not self.search_mode_enabled:
            self.search_mode_enabled = True

    @Gtk.Template.Callback()
    def search(self, _widget=None, _data=None, scroll=True):
        if not self.textbuffer:
            return
        searchtext = self.search_entry.get_text()
        context_start = self.textbuffer.get_start_iter()
        context_end = self.textbuffer.get_end_iter()
        text = self.textbuffer.get_slice(context_start, context_end, False)

        self.textbuffer.remove_tag(self.highlight, context_start, context_end)

        # case sensitive?
        flags = False
        if not self.case_sensitive.get_active():
            flags = flags | re.I

        ## regex?
        if not self.regex.get_active():
            searchtext = re.escape(searchtext)

        matches = re.finditer(searchtext, text, flags)

        self.matches = []
        self.active = 0
        for match in matches:
            self.matches.append((match.start(), match.end()))
            start_iter = self.textbuffer.get_iter_at_offset(match.start())
            end_iter = self.textbuffer.get_iter_at_offset(match.end())
            self.textbuffer.apply_tag(self.highlight, start_iter, end_iter)
        if scroll:
            self.scrollto(self.active)
        LOGGER.debug(searchtext)

    @Gtk.Template.Callback()
    def scrolltonext(self, _widget, _data=None):
        self.scrollto(self.active + 1)

    @Gtk.Template.Callback()
    def scrolltoprev(self, _widget, _data=None):
        self.scrollto(self.active - 1)

    def scrollto(self, index):
        if not self.matches:
            return
        self.active = index % len(self.matches)

        match = self.matches[self.active]

        start_iter = self.textbuffer.get_iter_at_offset(match[0])
        end_iter = self.textbuffer.get_iter_at_offset(match[1])

        # create a mark at the start of the coincidence to scroll to it
        mark = self.textbuffer.create_mark(None, start_iter, False)
        self.textview.scroller.smooth_scroll_to_mark(mark, center=True)

        # select coincidence
        self.textbuffer.select_range(start_iter, end_iter)

    @Gtk.Template.Callback()
    def hide(self, *arg, **kwargs):
        self.set_search_mode(False)

    @Gtk.Template.Callback()
    def replace_clicked(self, _widget, _data=None):
        self.replace(self.active)

    @Gtk.Template.Callback()
    def replace_all(self, _widget=None, _data=None):
        with user_action(self.textbuffer):
            for match in reversed(self.matches):
                self.__do_replace(match)
        self.search(scroll=False)

    def replace(self, searchindex, _inloop=False):
        with user_action(self.textbuffer):
            self.__do_replace(self.matches[searchindex])
        active = self.active
        self.search(scroll=False)
        self.active = active
        self.scrollto(self.active)

    def __do_replace(self, match):
        start_iter = self.textbuffer.get_iter_at_offset(match[0])
        end_iter = self.textbuffer.get_iter_at_offset(match[1])
        self.textbuffer.delete(start_iter, end_iter)
        start_iter = self.textbuffer.get_iter_at_offset(match[0])
        self.textbuffer.insert(start_iter, self.replace_entry.get_text())

    # Since the searchbar is overlayed to the textview we need to 
    # update its margin when the searchbar appears
    def update_textview_margin(self, paintable):
        self.textview.update_vertical_margin(self.paintable.get_intrinsic_height())
