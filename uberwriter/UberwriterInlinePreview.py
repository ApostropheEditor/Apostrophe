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
import gettext
import subprocess
import tempfile

import threading
from pprint import pprint

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from uberwriter_lib import LatexToPNG

from .FixTable import FixTable

from .MarkupBuffer import MarkupBuffer

from gettext import gettext as _

import logging
logger = logging.getLogger('uberwriter')

GObject.threads_init() # Still needed?

# TODO:
# - Don't insert a span with id, it breaks the text to often
#   Would be better to search for the nearest title and generate
#   A jumping URL from that (for preview)
#   Also, after going to preview, set cursor back to where it was

import telnetlib

import subprocess

class DictAccessor(object):

    def __init__( self, host='pan.alephnull.com', port=2628, timeout=60 ):
        self.tn = telnetlib.Telnet( host, port )
        self.timeout = timeout
        self.login_response = self.tn.expect( [ self.reEndResponse ], self.timeout )[ 2 ]


    def getOnline(self, word):
        p = subprocess.Popen(['dict', '-d', 'wn', word], stdout=subprocess.PIPE)
        return p.communicate()[0]

    def runCommand( self, cmd ):
        self.tn.write( cmd.encode('utf-8') + b'\r\n' )
        return self.tn.expect( [ self.reEndResponse ], self.timeout )[ 2 ]

    def getMatches( self, database, strategy, word ):
        if database in [ '', 'all' ]:
            d = '*'
        else:
            d = database
        if strategy in [ '', 'default' ]:
            s = '.'
        else:
            s = strategy
        w = word.replace( '"', r'\"' )
        tsplit = self.runCommand( 'MATCH %s %s "%s"' % ( d, s, w ) ).splitlines( )
        mlist = list( )
        if  tsplit[ -1 ].startswith( b'250 ok' ) and tsplit[ 0 ].startswith( b'1' ):
            mlines = tsplit[ 1:-2 ]
            for line in mlines:
                lsplit = line.strip( ).split( )
                db = lsplit[ 0 ]
                word = unquote( ' '.join( lsplit[ 1: ] ) )
                mlist.append( ( db, word ) )
        return mlist

    reEndResponse = re.compile( b'^[2-5][0-58][0-9] .*\r\n$', re.DOTALL + re.MULTILINE )
    reDefinition = re.compile( b'^151(.*?)^\.', re.DOTALL + re.MULTILINE )

    def getDefinition( self, database, word ):
        if database in [ '', 'all' ]:
            d = '*'
        else:
            d = database
        w = word.replace( '"', r'\"' )
        dsplit = self.runCommand( 'DEFINE %s "%s"' % ( d, w ) ).splitlines( True )
        # dsplit = self.getOnline(word).splitlines()

        dlist = list( )
        if  dsplit[ -1 ].startswith( b'250 ok' ) and dsplit[ 0 ].startswith( b'1' ):
            dlines = dsplit[ 1:-1 ]
            dtext = b''.join( dlines )
            dlist = self.reDefinition.findall( dtext )
            # print(dlist)
            dlist = [ dtext ]
        # dlist = dsplit # not using the localhost telnet connection
        return dlist

    def close( self ):
        t = self.runCommand( 'QUIT' )
        self.tn.close( )
        return t

    def parse_wordnet(self, response):
        # consisting of group (n,v,adj,adv)
        # number, description, examples, synonyms, antonyms
        capture = {}
        lines = response.splitlines()
        lines = lines[2:]
        lines = ' '.join(lines)
        lines = re.sub('\s+', ' ', lines).strip()
        lines = re.split(r'( adv | adj | n | v |^adv |^adj |^n |^v )', lines)
        res = []
        act_res = {'defs': [], 'class': 'none', 'num': 'None'}
        for l in lines:
            l = l.strip()
            if len(l) == 0:
                continue
            if l  in ['adv', 'adj', 'n', 'v']:
                if act_res:
                    res.append(act_res.copy())
                act_res = {}
                act_res['defs'] = []
                act_res['class'] = l
            else:
                ll = re.split('(?: |^)(\d): ', l)
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
                        if(llll.strip().startswith('"')):
                            act_def['examples'].append(llll)
                        else:
                            act_def['description'].append(llll)

                if act_def and 'description' in act_def:
                    act_res['defs'].append(act_def.copy())

        pprint(act_res)
        res.append(act_res.copy())
        return res

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

def get_dictionary(term):
    da = DictAccessor()
    output = da.getDefinition('wn', term)
    if(len(output)):
        output = output[0]
    else:
        return None
    return da.parse_wordnet(output.decode(encoding='UTF-8'))

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

def fill_lexikon_bubble(vocab, lexikon_dict):
    grid = Gtk.Grid.new()
    i = 0
    grid.set_name('LexikonBubble')
    grid.set_row_spacing(2)
    grid.set_column_spacing(4)
    if lexikon_dict:
        for entry in lexikon_dict:
            vocab_label = Gtk.Label.new(vocab + ' ~ ' + entry['class'])
            vocab_label.get_style_context().add_class('lexikon_heading')
            vocab_label.set_halign(Gtk.Align.START)
            vocab_label.set_justify(Gtk.Justification.LEFT)
            grid.attach(vocab_label, 0, i, 3, 1)

            for definition in entry['defs']:
                i = i + 1
                num_label = Gtk.Label.new(definition['num'])
                num_label.get_style_context().add_class('lexikon_num')
                num_label.set_justify(Gtk.Justification.RIGHT)
                grid.attach(num_label, 0, i, 1, 1)

                def_label = Gtk.Label.new(' '.join(definition['description']))
                def_label.set_halign(Gtk.Align.START)
                def_label.set_justify(Gtk.Justification.LEFT)
                def_label.get_style_context().add_class('lexikon_definition')
                def_label.props.wrap = True
                grid.attach(def_label, 1, i, 1, 1)
            i = i + 1
        grid.show_all()
        return grid
    else:
        return None



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
        self.popover = None

    def open_popover_with_widget(self, widget):
        a = self.TextBuffer.create_child_anchor(self.TextBuffer.get_iter_at_mark(self.ClickMark))
        lbl = Gtk.Label('')
        self.TextView.add_child_at_anchor(lbl, a)
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
        b = Gtk.Grid.new()
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
        self.popover.add(alignment)
        # a.add(alignment)
        dismiss, rect = self.popover.get_pointing_to()
        rect.y = rect.y - 20
        self.popover.set_pointing_to(rect)
        # widget = Gtk.Label.new("testasds a;12j3 21 lk3j213")
        widget.show_all()

        # b.attach(widget, 0, 1, 1, 1)
        self.popover.set_modal(True)
        self.popover.show_all()
        print(self.popover)
        self.popover.set_property('width-request', 50)

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
                    self.open_popover_with_widget(image)
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

        if not found_match:
            start_iter = self.TextBuffer.get_iter_at_mark(self.ClickMark)
            start_iter.backward_word_start()
            end_iter = start_iter.copy()
            end_iter.forward_word_end()
            word = self.TextBuffer.get_text(start_iter, end_iter, False)
            terms = get_dictionary(word)
            if terms:
                sc = Gtk.ScrolledWindow.new()
                sc.add(fill_lexikon_bubble(word, terms))
                sc.props.width_request = 500
                sc.props.height_request = 400
                sc.show_all()
                self.open_popover_with_widget(sc)

        return

    def move_popup(self):
        pass
