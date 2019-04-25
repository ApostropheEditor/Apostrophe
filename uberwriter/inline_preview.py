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

import logging
import re
import subprocess
import telnetlib
import tempfile
import threading
import urllib
import webbrowser
from gettext import gettext as _
from urllib.error import URLError
from urllib.parse import unquote

import gi

from uberwriter.text_view_markup_handler import MarkupHandler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from uberwriter import latex_to_PNG
from uberwriter.settings import Settings

from uberwriter.fix_table import FixTable

LOGGER = logging.getLogger('uberwriter')

# TODO:
# - Don't insert a span with id, it breaks the text to often
#   Would be better to search for the nearest title and generate
#   A jumping URL from that (for preview)
#   Also, after going to preview, set cursor back to where it was


class DictAccessor():

    def __init__(self, host='pan.alephnull.com', port=2628, timeout=60):
        self.telnet = telnetlib.Telnet(host, port)
        self.timeout = timeout
        self.login_response = self.telnet.expect(
            [self.reEndResponse], self.timeout)[2]

    def get_online(self, word):
        process = subprocess.Popen(['dict', '-d', 'wn', word],
                                   stdout=subprocess.PIPE)
        return process.communicate()[0]

    def run_command(self, cmd):
        self.telnet.write(cmd.encode('utf-8') + b'\r\n')
        return self.telnet.expect([self.reEndResponse], self.timeout)[2]

    def get_matches(self, database, strategy, word):
        if database in ['', 'all']:
            d = '*'
        else:
            d = database
        if strategy in ['', 'default']:
            s = '.'
        else:
            s = strategy
        w = word.replace('"', r'\"')
        tsplit = self.run_command('MATCH %s %s "%s"' % (d, s, w)).splitlines()
        mlist = list()
        if tsplit[-1].startswith(b'250 ok') and tsplit[0].startswith(b'1'):
            mlines = tsplit[1:-2]
            for line in mlines:
                lsplit = line.strip().split()
                db = lsplit[0]
                word = unquote(' '.join(lsplit[1:]))
                mlist.append((db, word))
        return mlist

    reEndResponse = re.compile(
        br'^[2-5][0-58][0-9] .*\r\n$', re.DOTALL + re.MULTILINE)
    reDefinition = re.compile(br'^151(.*?)^\.', re.DOTALL + re.MULTILINE)

    def get_definition(self, database, word):
        if database in ['', 'all']:
            d = '*'
        else:
            d = database
        w = word.replace('"', r'\"')
        dsplit = self.run_command('DEFINE %s "%s"' % (d, w)).splitlines(True)
        # dsplit = self.getOnline(word).splitlines()

        dlist = list()
        if dsplit[-1].startswith(b'250 ok') and dsplit[0].startswith(b'1'):
            dlines = dsplit[1:-1]
            dtext = b''.join(dlines)
            dlist = self.reDefinition.findall(dtext)
            # print(dlist)
            dlist = [dtext]
        # dlist = dsplit # not using the localhost telnet connection
        return dlist

    def close(self):
        t = self.run_command('QUIT')
        self.telnet.close()
        return t

    def parse_wordnet(self, response):
        # consisting of group (n,v,adj,adv)
        # number, description, examples, synonyms, antonyms

        lines = response.splitlines()
        lines = lines[2:]
        lines = ' '.join(lines)
        lines = re.sub(r'\s+', ' ', lines).strip()
        lines = re.split(r'( adv | adj | n | v |^adv |^adj |^n |^v )', lines)
        res = []
        act_res = {'defs': [], 'class': 'none', 'num': 'None'}
        for l in lines:
            l = l.strip()
            if not l:
                continue
            if l in ['adv', 'adj', 'n', 'v']:
                if act_res:
                    res.append(act_res.copy())
                act_res = {}
                act_res['defs'] = []
                act_res['class'] = l
            else:
                ll = re.split(r'(?: |^)(\d): ', l)
                act_def = {}
                for lll in ll:
                    if lll.strip().isdigit() or not lll.strip():
                        if 'description' in act_def and act_def['description']:
                            act_res['defs'].append(act_def.copy())
                        act_def = {'num': lll}
                        continue
                    a = re.findall(r'(\[(syn|ant): (.+?)\] ??)+', lll)
                    for n in a:
                        if n[1] == 'syn':
                            act_def['syn'] = re.findall(r'\{(.*?)\}.*?', n[2])
                        else:
                            act_def['ant'] = re.findall(r'\{(.*?)\}.*?', n[2])
                    tbr = re.search(r'\[.+\]', lll)
                    if tbr:
                        lll = lll[:tbr.start()]
                    lll = lll.split(';')
                    act_def['examples'] = []
                    act_def['description'] = []
                    for llll in lll:
                        llll = llll.strip()
                        if llll.strip().startswith('"'):
                            act_def['examples'].append(llll)
                        else:
                            act_def['description'].append(llll)

                if act_def and 'description' in act_def:
                    act_res['defs'].append(act_def.copy())

        # pprint(act_res)
        res.append(act_res.copy())
        return res


def check_url(url, item, spinner):
    LOGGER.debug("thread started, checking url")
    error = False
    try:
        response = urllib.request.urlopen(url)
    except URLError as e:
        error = True
        text = "Error! Reason: %s" % e.reason

    if not error:
        if (response.code / 100) >= 4:
            LOGGER.debug("Website not available")
            text = _("Website is not available")
        else:
            text = _("Website is available")
    LOGGER.debug("Response: %s" % text)
    spinner.destroy()
    item.set_label(text)


def get_dictionary(term):
    da = DictAccessor()
    output = da.get_definition('wn', term)
    if output:
        output = output[0]
    else:
        return None
    return da.parse_wordnet(output.decode(encoding='UTF-8'))


def get_web_thumbnail(url, item, spinner):
    LOGGER.debug("thread started, generating thumb")

    # error = False

    # gnome-web-photo only understands http urls
    if url.startswith("www"):
        url = "http://" + url

    filename = tempfile.mktemp(suffix='.png')
    thumb_size = '256'  # size can only be 32, 64, 96, 128 or 256!
    args = ['gnome-web-photo', '--mode=thumbnail',
            '-s', thumb_size, url, filename]
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    _output = process.communicate()[0]

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


def fill_lexikon_bubble(vocab, lexikon_dict):
    grid = Gtk.Grid.new()
    i = 0
    grid.set_name('LexikonBubble')
    grid.set_row_spacing(2)
    grid.set_column_spacing(4)
    if lexikon_dict:
        for entry in lexikon_dict:
            vocab_label = Gtk.Label.new(vocab + ' ~ ' + entry['class'])
            vocab_label.get_style_context().add_class('lexikon-heading')
            vocab_label.set_halign(Gtk.Align.START)
            vocab_label.set_justify(Gtk.Justification.LEFT)
            grid.attach(vocab_label, 0, i, 3, 1)

            for definition in entry['defs']:
                i = i + 1
                num_label = Gtk.Label.new(definition['num'])
                num_label.get_style_context().add_class('lexikon-num')
                num_label.set_justify(Gtk.Justification.RIGHT)
                grid.attach(num_label, 0, i, 1, 1)

                def_label = Gtk.Label.new(' '.join(definition['description']))
                def_label.set_halign(Gtk.Align.START)
                def_label.set_justify(Gtk.Justification.LEFT)
                def_label.get_style_context().add_class('lexikon-definition')
                def_label.props.wrap = True
                grid.attach(def_label, 1, i, 1, 1)
            i = i + 1
        grid.show_all()
        return grid
    return None


class InlinePreview:

    def __init__(self, text_view):
        self.text_view = text_view
        self.text_buffer = text_view.get_buffer()
        self.latex_converter = latex_to_PNG.LatexToPNG()
        cursor_mark = self.text_buffer.get_insert()
        cursor_iter = self.text_buffer.get_iter_at_mark(cursor_mark)
        self.click_mark = self.text_buffer.create_mark('click', cursor_iter)
        # Events for popup menu
        # self.TextView.connect_after('populate-popup', self.populate_popup)
        # self.TextView.connect_after('popup-menu', self.move_popup)
        self.text_view.connect('button-press-event', self.click_move_button)
        self.popover = None
        self.settings = Settings.new()

    def open_popover_with_widget(self, widget):
        a = self.text_buffer.create_child_anchor(
            self.text_buffer.get_iter_at_mark(self.click_mark))
        lbl = Gtk.Label('')
        self.text_view.add_child_at_anchor(lbl, a)
        lbl.show()
        # a = Gtk.Window.new(Gtk.WindowType.POPUP)
        # a.set_transient_for(self.TextView.get_toplevel())
        # a.grab_focus()
        # a.set_name("QuickPreviewPopup")
        # # a.set_attached_to(self.TextView)
        # a.move(300, 300)
        # a.set_modal(True)
        # def close(widget, event, *args):
        #     if(event.keyval == Gdk.KEY_Escape):
        #         widget.destroy()
        # a.connect('key-press-event', close)
        alignment = Gtk.Alignment()
        alignment.props.margin_bottom = 5
        alignment.props.margin_top = 5
        alignment.props.margin_left = 4
        alignment.add(widget)
        # self.TextView.add_child_in_window(b, Gtk.TextWindowType.WIDGET, 200, 200)
        # b.attach(Gtk.Label.new("test 123"), 0, 0, 1, 1)
        # b.show_all()
        # a.show_all()
        self.popover = Gtk.Popover.new(lbl)
        self.popover.get_style_context().add_class("quick-preview-popup")
        self.popover.add(alignment)
        # a.add(alignment)
        _dismiss, rect = self.popover.get_pointing_to()
        rect.y = rect.y - 20
        self.popover.set_pointing_to(rect)
        # widget = Gtk.Label.new("testasds a;12j3 21 lk3j213")
        widget.show_all()

        # b.attach(widget, 0, 1, 1, 1)
        self.popover.set_modal(True)
        self.popover.show_all()
        # print(self.popover)
        self.popover.set_property('width-request', 50)

    def click_move_button(self, _widget, event):
        if event.button == 1 and event.state & Gdk.ModifierType.CONTROL_MASK:
            x, y = self.text_view.window_to_buffer_coords(2,
                                                          int(event.x),
                                                          int(event.y))
            self.text_buffer.move_mark(self.click_mark,
                                       self.text_view.get_iter_at_location(x, y).iter)
            self.populate_popup(self.text_view)

    def fix_table(self, _widget, _data=None):
        LOGGER.debug('fixing that table')
        fix_table = FixTable(self.text_buffer)
        fix_table.fix_table()

    def populate_popup(self, _editor, _data=None):
        # popover = Gtk.Popover.new(editor)
        # pop_cont = Gtk.Container.new()
        # popover.add(pop_cont)
        # popover.show_all()

        item = Gtk.MenuItem.new()
        item.set_name("PreviewMenuItem")
        separator = Gtk.SeparatorMenuItem.new()

        # table_item = Gtk.MenuItem.new()
        # table_item.set_label('Fix that table')

        # table_item.connect('activate', self.fix_table)
        # table_item.show()
        # menu.prepend(table_item)
        # menu.show()

        start_iter = self.text_buffer.get_iter_at_mark(self.click_mark)
        # Line offset of click mark
        line_offset = start_iter.get_line_offset()
        end_iter = start_iter.copy()
        start_iter.set_line_offset(0)
        end_iter.forward_to_line_end()

        text = self.text_buffer.get_text(start_iter, end_iter, False)

        math = MarkupHandler.regex["MATH"]
        link = MarkupHandler.regex["LINK"]

        footnote = re.compile(r'\[\^([^\s]+?)\]')
        image = re.compile(r"!\[(.*?)\]\((.+?)\)")

        found_match = False

        matches = re.finditer(math, text)
        for match in matches:
            LOGGER.debug(match.group(1))
            if match.start() < line_offset < match.end():
                success, result = self.latex_converter.generatepng(
                    match.group(1))
                if success:
                    image = Gtk.Image.new_from_file(result)
                    image.show()
                    LOGGER.debug("logging image")
                    # item.add(image)
                    self.open_popover_with_widget(image)
                else:
                    label = Gtk.Label()
                    msg = 'Formula looks incorrect:\n' + result
                    label.set_alignment(0.0, 0.5)
                    label.set_text(msg)
                    label.show()
                    item.add(label)
                    self.open_popover_with_widget(item)
                item.show()
                # menu.prepend(separator)
                # separator.show()
                # menu.prepend(item)
                # menu.show()
                found_match = True
                break

        if not found_match:
            # Links
            matches = re.finditer(link, text)
            for match in matches:
                if match.start() < line_offset < match.end():
                    text = text[text.find("http://"):-1]

                    item.connect("activate", lambda w: webbrowser.open(text))

                    LOGGER.debug(text)

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
                    self.open_popover_with_widget(webphoto_item)

                    # menu.prepend(separator)
                    # separator.show()

                    # menu.prepend(webphoto_item)
                    # menu.prepend(statusitem)
                    # menu.prepend(item)
                    # menu.show()

                    found_match = True
                    break

        if not found_match:
            matches = re.finditer(image, text)
            for match in matches:
                if match.start() < line_offset < match.end():
                    path = match.group(2)
                    if path.startswith("file://"):
                        path = path[7:]
                    elif not path.startswith("/"):
                        # then the path is relative
                        base_path = self.settings.get_value(
                            "open-file-path").get_string()
                        path = base_path + "/" + path

                    LOGGER.info(path)
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 400, 300)
                    image = Gtk.Image.new_from_pixbuf(pixbuf)
                    image.show()
                    self.open_popover_with_widget(image)
                    item.set_property('width-request', 50)

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
                if match.start() < line_offset < match.end():
                    LOGGER.debug(match.group(1))
                    footnote_match = re.compile(
                        r"\[\^" + match.group(1) + r"\]: (.+(?:\n|\Z)(?:^[\t].+(?:\n|\Z))*)",
                        re.MULTILINE)
                    replace = re.compile(r"^\t", re.MULTILINE)
                    start, end = self.text_buffer.get_bounds()
                    fn_match = re.search(
                        footnote_match, self.text_buffer.get_text(start, end, False))
                    label = Gtk.Label()
                    label.set_alignment(0.0, 0.5)
                    LOGGER.debug(fn_match)
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
                    self.open_popover_with_widget(item)

                    # menu.prepend(separator)
                    # separator.show()
                    # menu.prepend(item)
                    # menu.show()
                    found_match = True
                    break

        if not found_match:
            start_iter = self.text_buffer.get_iter_at_mark(self.click_mark)
            start_iter.backward_word_start()
            end_iter = start_iter.copy()
            end_iter.forward_word_end()
            word = self.text_buffer.get_text(start_iter, end_iter, False)
            terms = get_dictionary(word)
            if terms:
                scrolled_window = Gtk.ScrolledWindow.new()
                scrolled_window.add(fill_lexikon_bubble(word, terms))
                scrolled_window.props.width_request = 500
                scrolled_window.props.height_request = 400
                scrolled_window.show_all()
                self.open_popover_with_widget(scrolled_window)

    def move_popup(self):
        pass
