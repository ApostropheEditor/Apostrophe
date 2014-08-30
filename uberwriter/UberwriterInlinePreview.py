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

import re
import http.client
import urllib
from urllib.error import URLError, HTTPError
import webbrowser
import locale
import subprocess
import tempfile

import threading

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from uberwriter_lib import LatexToPNG

from .FixTable import FixTable

from .MarkupBuffer import MarkupBuffer

from locale import gettext as _
locale.textdomain('uberwriter')

import logging
logger = logging.getLogger('uberwriter')

GObject.threads_init() # Still needed?

# TODO:
# - Don't insert a span with id, it breaks the text to often
#   Would be better to search for the nearest title and generate
#   A jumping URL from that (for preview)
#   Also, after going to preview, set cursor back to where it was

def check_url(url, item, spinner):
    logger.debug("thread started, checking url")
    error = False
    try:
        response = urllib.request.urlopen(url)
    except URLError as e:
        error = True
        text = "Error! Reason: %s" % e.reason

    if not error:
        if (response.code / 100) >= 4:
            logger.debug("Website not available")
            text = _("Website is not available")
        else:
            text = _("Website is available")
    logger.debug("Response: %s" % text)
    spinner.destroy()
    item.set_label(text)


def get_web_thumbnail(url, item, spinner):
    logger.debug("thread started, generating thumb")

    # error = False

    filename = tempfile.mktemp(suffix='.png')
    thumb_size = '256'  # size can only be 32, 64, 96, 128 or 256!
    args = ['gnome-web-photo', '--mode=thumbnail', '-s', thumb_size, url, filename]
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = p.communicate()[0]

    image = Gtk.Image.new_from_file(filename)
    image.show()

    # if not error:
    #    if (response.code / 100) >= 4:
    #        logger.debug("Website not available")
    #        text = _("Website is not available")
    #    else:
    #        text = _("Website is available")

    spinner.destroy()
    item.add(image)
    item.show()


class UberwriterInlinePreview():

    def __init__(self, view, text_buffer):
        self.TextView = view
        self.TextBuffer = text_buffer
        self.LatexConverter = LatexToPNG.LatexToPNG()
        cursor_mark = self.TextBuffer.get_insert()
        cursor_iter = self.TextBuffer.get_iter_at_mark(cursor_mark)
        self.ClickMark = self.TextBuffer.create_mark('click', cursor_iter)
        # Events for popup menu
        self.TextView.connect_after('populate-popup', self.populate_popup)
        self.TextView.connect_after('popup-menu', self.move_popup)
        self.TextView.connect('button-press-event', self.click_move_button)

    def click_move_button(self, widget, event):
        if event.button == 3:
            x, y = self.TextView.window_to_buffer_coords(2,
                                                         int(event.x),
                                                         int(event.y))
            self.TextBuffer.move_mark(self.ClickMark,
                                      self.TextView.get_iter_at_location(x, y))

    def fix_table(self, widget, data=None):
        logger.debug('fixing that table')
        f = FixTable(self.TextBuffer)
        f.fix_table()

    def populate_popup(self, editor, menu, data=None):
        popover = Gtk.Popover.new(editor)
        # pop_cont = Gtk.Container.new()
        # popover.add(pop_cont)
        popover.show_all()

        item = Gtk.MenuItem.new()
        item.set_name("PreviewMenuItem")
        separator = Gtk.SeparatorMenuItem.new()

        table_item = Gtk.MenuItem.new()
        table_item.set_label('Fix that table')

        table_item.connect('activate', self.fix_table)
        table_item.show()
        menu.prepend(table_item)
        menu.show()

        start_iter = self.TextBuffer.get_iter_at_mark(self.ClickMark)
        # Line offset of click mark
        line_offset = start_iter.get_line_offset()
        end_iter = start_iter.copy()
        start_iter.set_line_offset(0)
        end_iter.forward_to_line_end()

        text = self.TextBuffer.get_text(start_iter, end_iter, False)

        math = MarkupBuffer.regex["MATH"]
        link = MarkupBuffer.regex["LINK"]

        footnote = re.compile('\[\^([^\s]+?)\]')
        image = re.compile("!\[(.+?)\]\((.+?)\)")

        buf = self.TextBuffer
        context_offset = 0

        matchlist = []

        found_match = False

        matches = re.finditer(math, text)
        for match in matches:
            logger.debug(match.group(1))
            if match.start() < line_offset and match.end() > line_offset:
                success, result = self.LatexConverter.generatepng(match.group(1))
                if success:
                    image = Gtk.Image.new_from_file(result)
                    image.show()
                    logger.debug("logging image")
                    # item.add(image)
                    popover.add(image)
                    popover.show_all()
                    item.set_property('width-request', 50)
                    popover.set_property('width-request', 50)
                else:
                    label = Gtk.Label()
                    msg = 'Formula looks incorrect:\n' + result
                    label.set_alignment(0.0, 0.5)
                    label.set_text(msg)
                    label.show()
                    item.add(label)
                item.show()
                menu.prepend(separator)
                separator.show()
                menu.prepend(item)
                menu.show()
                found_match = True
                break

        if not found_match:
            # Links
            matches = re.finditer(link, text)
            for match in matches:
                if match.start() < line_offset and match.end() > line_offset:
                    text = text[text.find("http://"):-1]

                    item.connect("activate", lambda w: webbrowser.open(text))

                    logger.debug(text)

                    statusitem = Gtk.MenuItem.new()
                    statusitem.show()

                    spinner = Gtk.Spinner.new()
                    spinner.start()
                    statusitem.add(spinner)
                    spinner.show()
                    
                    thread = threading.Thread(target=check_url, 
                        args=(text, statusitem, spinner))
                    thread.start()

                    webphoto_item = Gtk.MenuItem.new()
                    webphoto_item.show()
                    spinner_2 = Gtk.Spinner.new()
                    spinner_2.start()
                    webphoto_item.add(spinner_2)
                    spinner_2.show()

                    thread_image = threading.Thread(target=get_web_thumbnail, 
                        args=(text, webphoto_item, spinner_2))

                    thread_image.start()

                    item.set_label(_("Open Link in Webbrowser"))
                    item.show()
    
                    menu.prepend(separator)
                    separator.show()

                    menu.prepend(webphoto_item)
                    menu.prepend(statusitem)
                    menu.prepend(item)
                    menu.show()


                    found_match = True
                    break

        if not found_match:
            matches = re.finditer(image, text)
            for match in matches:
                if match.start() < line_offset and match.end() > line_offset:
                    path = match.group(2)
                    if path.startswith("file://"):
                        path = path[7:]
                    logger.info(path)
                    pb = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 400, 300)
                    image = Gtk.Image.new_from_pixbuf(pb)
                    image.show()
                    popover.add(image)
                    popover.show_all()
                    item.set_property('width-request', 50)
                    popover.set_property('width-request', 50)

                    # item.add(image)
                    # item.set_property('width-request', 50)
                    # item.show()
                    # menu.prepend(separator)
                    # separator.show()
                    # menu.prepend(item)
                    # menu.show()
                    found_match = True
                    break

        if not found_match:
            matches = re.finditer(footnote, text)
            for match in matches:
                if match.start() < line_offset and match.end() > line_offset:
                    logger.debug(match.group(1))
                    footnote_match = re.compile("\[\^" + match.group(1) + "\]: (.+(?:\n|\Z)(?:^[\t].+(?:\n|\Z))*)", re.MULTILINE)
                    replace = re.compile("^\t", re.MULTILINE)
                    start, end = self.TextBuffer.get_bounds()
                    fn_match = re.search(footnote_match, self.TextBuffer.get_text(start, end, False))
                    label = Gtk.Label()
                    label.set_alignment(0.0, 0.5)
                    logger.debug(fn_match)
                    if fn_match:
                        result = re.sub(replace, "", fn_match.group(1))
                        if result.endswith("\n"):
                            result = result[:-1]
                    else:
                        result = _("No matching footnote found")
                    label.set_max_width_chars(40)
                    label.set_line_wrap(True)
                    label.set_text(result)
                    label.show()
                    item.add(label)
                    item.show()

                    menu.prepend(separator)
                    separator.show()
                    menu.prepend(item)
                    menu.show()
                    found_match = True
                    break
        return

    def move_popup(self):
        pass
