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

import logging
import re

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk

# from plugins import plugins

LOGGER = logging.getLogger('uberwriter')


class SearchAndReplace:
    """
    Adds (regex) search and replace functionality to
    uberwriter
    """

    def __init__(self, parentwindow, textview):
        self.parentwindow = parentwindow
        self.box = parentwindow.builder.get_object("searchbar_placeholder")
        self.box.set_reveal_child(False)
        self.searchbar = parentwindow.builder.get_object("searchbar")
        self.searchentry = parentwindow.builder.get_object("searchentrybox")
        self.searchentry.connect('changed', self.search)
        self.searchentry.connect('activate', self.scrolltonext)
        self.searchentry.connect('key-press-event', self.key_pressed)

        self.open_replace_button = parentwindow.builder.get_object("replace")
        self.open_replace_button.connect("toggled", self.toggle_replace)

        self.textview = textview
        self.textbuffer = textview.get_buffer()

        self.nextbutton = parentwindow.builder.get_object("next_result")
        self.prevbutton = parentwindow.builder.get_object("previous_result")
        self.regexbutton = parentwindow.builder.get_object("regex")
        self.casesensitivebutton = parentwindow.builder.get_object("case_sensitive")

        self.replacebox = parentwindow.builder.get_object("replace_placeholder")
        self.replacebox.set_reveal_child(False)
        self.replace_one_button = parentwindow.builder.get_object("replace_one")
        self.replace_all_button = parentwindow.builder.get_object("replace_all")
        self.replaceentry = parentwindow.builder.get_object("replaceentrybox")

        self.replace_all_button.connect('clicked', self.replace_all)
        self.replace_one_button.connect('clicked', self.replace_clicked)
        self.replaceentry.connect('activate', self.replace_clicked)

        self.nextbutton.connect('clicked', self.scrolltonext)
        self.prevbutton.connect('clicked', self.scrolltoprev)
        self.regexbutton.connect('toggled', self.search)
        self.casesensitivebutton.connect('toggled', self.search)
        self.highlight = self.textbuffer.create_tag('search_highlight',
                                                    background="yellow")

        self.textview.connect("focus-in-event", self.focused_texteditor)

    def toggle_replace(self, widget, _data=None):
        """toggle the replace box
        """
        if widget.get_active():
            self.replacebox.set_reveal_child(True)
        else:
            self.replacebox.set_reveal_child(False)

    # TODO: refactorize!
    def key_pressed(self, _widget, event, _data=None):
        """hide the search and replace content box when ESC is pressed
        """
        if event.keyval in [Gdk.KEY_Escape]:
            self.hide()

    def focused_texteditor(self, _widget, _data=None):
        """hide the search and replace content box
        """
        self.hide()

    def toggle_search(self, _widget=None, _data=None):
        """
        show search box
        """
        if self.box.get_reveal_child() is False or self.searchbar.get_search_mode() is False:
            self.searchbar.set_search_mode(True)
            self.box.set_reveal_child(True)
            self.searchentry.grab_focus()
        else:
            self.hide()
            self.open_replace_button.set_active(False)

    def search(self, _widget=None, _data=None, scroll=True):
        searchtext = self.searchentry.get_text()
        buf = self.textbuffer
        context_start = buf.get_start_iter()
        context_end = buf.get_end_iter()
        text = buf.get_slice(context_start, context_end, False)

        self.textbuffer.remove_tag(self.highlight, context_start, context_end)

        # case sensitive?
        flags = False
        if not self.casesensitivebutton.get_active():
            flags = flags | re.I

        # regex?
        if not self.regexbutton.get_active():
            searchtext = re.escape(searchtext)

        matches = re.finditer(searchtext, text, flags)

        self.matchiters = []
        self.active = 0
        for match in matches:
            start_iter = buf.get_iter_at_offset(match.start())
            end_iter = buf.get_iter_at_offset(match.end())
            self.matchiters.append((start_iter, end_iter))
            self.textbuffer.apply_tag(self.highlight, start_iter, end_iter)
        if scroll:
            self.scrollto(self.active)
        LOGGER.debug(searchtext)

    def scrolltonext(self, _widget, _data=None):
        self.scrollto(self.active + 1)

    def scrolltoprev(self, _widget, _data=None):
        self.scrollto(self.active - 1)

    def scrollto(self, index):
        if not self.matchiters:
            return
        if index < len(self.matchiters):
            self.active = index
        else:
            self.active = 0

        matchiter = self.matchiters[self.active]
        self.textview.get_buffer().select_range(matchiter[0], matchiter[1])

        # self.texteditor.scroll_to_iter(matchiter[0], 0.0, True, 0.0, 0.5)

    def hide(self):
        self.replacebox.set_reveal_child(False)
        self.box.set_reveal_child(False)
        self.textbuffer.remove_tag(self.highlight,
                                   self.textbuffer.get_start_iter(),
                                   self.textbuffer.get_end_iter())
        self.textview.grab_focus()

    def replace_clicked(self, _widget, _data=None):
        self.replace(self.active)

    def replace_all(self, _widget=None, _data=None):
        while self.matchiters:
            match = self.matchiters[0]
            self.textbuffer.delete(match[0], match[1])
            self.textbuffer.insert(match[0], self.replaceentry.get_text())
            self.search(scroll=False)

    def replace(self, searchindex, _inloop=False):
        match = self.matchiters[searchindex]
        self.textbuffer.delete(match[0], match[1])
        self.textbuffer.insert(match[0], self.replaceentry.get_text())
        active = self.active
        self.search(scroll=False)
        self.active = active
        self.scrollto(self.active)
