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

import locale
import subprocess
import os
import codecs
import webbrowser
import urllib
import pickle

from locale import gettext as _
locale.textdomain('uberwriter')

import mimetypes

from gi.repository import Gtk, Gdk, GObject, Gio  # pylint: disable=E0611
from gi.repository import WebKit2 as WebKit
from gi.repository import Pango  # pylint: disable=E0611

import cairo
# import cairo.Pattern, cairo.SolidPattern

import re

from .MarkupBuffer import MarkupBuffer
from .UberwriterTextEditor import TextEditor
from .UberwriterInlinePreview import UberwriterInlinePreview
from .UberwriterSidebar import UberwriterSidebar
from .UberwriterSearchAndReplace import UberwriterSearchAndReplace
# from .UberwriterAutoCorrect import UberwriterAutoCorrect

import logging
logger = logging.getLogger('uberwriter')

# Spellcheck

import locale

from uberwriter_lib.gtkspellcheck import SpellChecker

try:
    import apt
    APT_ENABLED = True
except:
    APT_ENABLED = False

#from uberwriter_lib import Window
from uberwriter_lib.AppWindow import Window
from uberwriter_lib import helpers
from .UberwriterAdvancedExportDialog import UberwriterAdvancedExportDialog
# from .plugins.bibtex import BibTex
# Some Globals
# TODO move them somewhere for better
# accesibility from other files

CONFIG_PATH = os.path.expanduser("~/.config/uberwriter/")

# See texteditor_lib.Window.py for more details about how this class works
class UberwriterWindow(Window):

    #__gtype_name__ = "UberwriterWindow"
    
    __gsignals__ = {
        'save-file': (GObject.SIGNAL_ACTION, None, ()),
        'open-file': (GObject.SIGNAL_ACTION, None, ()),
        'save-file-as': (GObject.SIGNAL_ACTION, None, ()),
        'new-file': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-focusmode': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-bibtex': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-fullscreen': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-spellcheck': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-preview': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-search': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-search-replace': (GObject.SIGNAL_ACTION, None, ()),
        'close-window': (GObject.SIGNAL_ACTION, None, ())
    }

    def scrolled(self, widget):
        """if window scrolled + focusmode make font black again"""
        # if self.focusmode:
            # if self.textchange == False:
            #     if self.scroll_count >= 4:
            #         self.TextBuffer.apply_tag(
            #             self.MarkupBuffer.blackfont,
            #             self.TextBuffer.get_start_iter(),
            #             self.TextBuffer.get_end_iter())
            #     else:
            #         self.scroll_count += 1
            # else:
            #     self.scroll_count = 0
            #     self.textchange = False

    def paste_done(self, *args):
        self.MarkupBuffer.markup_buffer(0)

    def init_typewriter(self):
        self.EditorAlignment.props.margin_top = self.window_height / 2
        self.EditorAlignment.props.margin_bottom = self.window_height / 2
        self.typewriter_initiated = True

    def remove_typewriter(self):
        self.EditorAlignment.props.margin_top = self.alignment_padding
        self.EditorAlignment.props.margin_bottom = 250
        self.text_change_event = self.TextBuffer.connect('changed', self.text_changed)

    def get_text(self):
        start_iter = self.TextBuffer.get_start_iter()
        end_iter = self.TextBuffer.get_end_iter()
        return self.TextBuffer.get_text(start_iter, end_iter, False)

    WORDCOUNT = re.compile(r"(?!\-\w)[\s#*\+\-]+", re.UNICODE)
    def update_line_and_char_count(self):
        if self.status_bar_visible == False:
            return
        self.char_count.set_text(str(self.TextBuffer.get_char_count()))
        text = self.get_text()
        words = re.split(self.WORDCOUNT, text)
        length = len(words)
        # Last word a "space"
        if len(words[-1]) == 0:
            length = length - 1
        # First word a "space" (happens in focus mode...)
        if len(words[0]) == 0:
            length = length - 1
        if length == -1:
            length = 0
        self.word_count.set_text(str(length))

    def mark_set(self, buffer, location, mark, data=None):
        if mark.get_name() in ['insert', 'gtk_drag_target']:
            self.check_scroll(mark)
        return True

    def text_changed(self, widget, data=None):
        if self.did_change == False:
            self.did_change = True
            title = self.get_title()
            self.set_headerbar_title("* " + title)

        self.MarkupBuffer.markup_buffer(1)
        self.textchange = True

        self.buffer_modified_for_status_bar = True
        self.update_line_and_char_count()
        self.check_scroll(self.TextBuffer.get_insert())

    def toggle_fullscreen(self, widget, data=None):
        if widget.get_active():
            self.fullscreen()
            key, mod = Gtk.accelerator_parse("Escape")
            self.fullscreen_button.add_accelerator("activate",
                self.accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
            self.fullscreen_button.set_active(True)
            self.fullscreen_menu_button.set_active(True)
            # Hide Menu
            self.menubar.hide()
        else:
            self.unfullscreen()
            key, mod = Gtk.accelerator_parse("Escape")
            self.fullscreen_button.remove_accelerator(
                self.accel_group, key, mod)
            self.fullscreen_button.set_active(False)
            self.fullscreen_menu_button.set_active(False)
            self.menubar.hide()

        self.TextEditor.grab_focus()

    def set_focusmode(self, widget, data=None):
        if widget.get_active():
            self.init_typewriter()
            self.MarkupBuffer.focusmode_highlight()
            self.focusmode = True
            self.TextEditor.grab_focus()
            self.check_scroll(self.TextBuffer.get_insert())
            if self.spellcheck != False:
                self.SpellChecker._misspelled.set_property('underline', 0)
            self.focusmode_menu_button.set_active(True)
            self.focusmode_button.set_active(True)
        else:
            self.remove_typewriter()
            self.focusmode = False
            self.TextBuffer.remove_tag(self.MarkupBuffer.grayfont,
                self.TextBuffer.get_start_iter(),
                self.TextBuffer.get_end_iter())
            self.TextBuffer.remove_tag(self.MarkupBuffer.blackfont,
                self.TextBuffer.get_start_iter(),
                self.TextBuffer.get_end_iter())

            self.MarkupBuffer.markup_buffer(1)
            self.TextEditor.grab_focus()
            self.update_line_and_char_count()
            self.check_scroll()
            if self.spellcheck != False:
                self.SpellChecker._misspelled.set_property('underline', 4)
            self.focusmode_menu_button.set_active(False)
            self.focusmode_button.set_active(False)

    def scroll_smoothly(self, widget, frame_clock, data = None):
        if self.smooth_scroll_data['target_pos'] == -1:
            return True
        def ease_out_cubic(t):
          p = t - 1;
          return p * p * p + 1;
        
        now = frame_clock.get_frame_time()
        if self.smooth_scroll_acttarget != self.smooth_scroll_data['target_pos']:
            self.smooth_scroll_starttime = now
            self.smooth_scroll_endtime = now + self.smooth_scroll_data['duration'] * 100
            self.smooth_scroll_acttarget = self.smooth_scroll_data['target_pos']

        if(now < self.smooth_scroll_endtime):
            t = float(now - self.smooth_scroll_starttime) / float(self.smooth_scroll_endtime - self.smooth_scroll_starttime)
        else:
            t = 1
            pos = self.smooth_scroll_data['source_pos'] + (t * (self.smooth_scroll_data['target_pos'] - self.smooth_scroll_data['source_pos']))
            widget.get_vadjustment().props.value = pos
            self.smooth_scroll_data['target_pos'] = -1
            return True

        t = ease_out_cubic(t)
        pos = self.smooth_scroll_data['source_pos'] + (t * (self.smooth_scroll_data['target_pos'] - self.smooth_scroll_data['source_pos']))
        widget.get_vadjustment().props.value = pos
        return True # continue ticking

    def check_scroll(self, mark=None):
        gradient_offset = 80
        buf = self.TextEditor.get_buffer()
        if mark:
            ins_it = buf.get_iter_at_mark(mark)
        else:
            ins_it = buf.get_iter_at_mark(buf.get_insert())
        loc_rect = self.TextEditor.get_iter_location(ins_it)

        # alignment offset added from top
        pos_y = loc_rect.y + loc_rect.height + self.EditorAlignment.props.margin_top 
        
        ha = self.ScrolledWindow.get_vadjustment()
        if ha.props.page_size < gradient_offset:
            return
        pos = pos_y - ha.props.value
        # print("pos: %i, pos_y %i, page_sz: %i, val: %i" % (pos, pos_y, ha.props.page_size - gradient_offset, ha.props.value))
        # global t, amount, initvadjustment
        target_pos = -1
        if self.focusmode:
            # print("pos: %i > %i" % (pos, ha.props.page_size * 0.5))
            if pos != (ha.props.page_size * 0.5):
                target_pos = pos_y - (ha.props.page_size * 0.5)
        elif pos > ha.props.page_size - gradient_offset - 60:
            target_pos = pos_y - ha.props.page_size + gradient_offset + 40
        elif pos < gradient_offset:
            target_pos = pos_y - gradient_offset
        self.smooth_scroll_data = {
            'target_pos': target_pos,
            'source_pos': ha.props.value, 
            'duration': 2000
        }
        if self.smooth_scroll_tickid == -1:
            self.smooth_scroll_tickid = self.ScrolledWindow.add_tick_callback(self.scroll_smoothly)

    def window_resize(self, widget, data=None):
        # To calc padding top / bottom
        self.window_height = widget.get_allocation().height
        w_width = widget.get_allocation().width
        # Calculate left / right margin
        width_request = 600
        if(w_width < 900):
            # self.MarkupBuffer.set_multiplier(8)
            self.current_font_size = 12
            self.alignment_padding = 30
            lm = 7 * 8
            self.get_style_context().remove_class("medium")
            self.get_style_context().remove_class("large")
            self.get_style_context().add_class("small")

        elif(w_width < 1400):
            # self.MarkupBuffer.set_multiplier(10)
            width_request = 800
            self.current_font_size = 15
            self.alignment_padding = 40
            lm = 7 * 10
            self.get_style_context().remove_class("small")
            self.get_style_context().remove_class("large")
            self.get_style_context().add_class("medium")

        else:
            # self.MarkupBuffer.set_multiplier(13)
            self.current_font_size = 17
            width_request = 1000
            self.alignment_padding = 60
            lm = 7 * 13
            self.get_style_context().remove_class("medium")
            self.get_style_context().remove_class("small")
            self.get_style_context().add_class("large")


        self.EditorAlignment.props.margin_bottom = self.alignment_padding + 30
        self.EditorAlignment.props.margin_top = self.alignment_padding
        #self.TextEditor.set_left_margin(lm)
        #self.TextEditor.set_right_margin(lm)

        self.MarkupBuffer.recalculate(lm)

        if self.focusmode:
            self.remove_typewriter()
            self.init_typewriter()

        if self.TextEditor.props.width_request != width_request:
            self.TextEditor.props.width_request = width_request
            alloc = self.TextEditor.get_allocation()
            alloc.width = width_request
            self.TextEditor.size_allocate(alloc)

    def style_changed(self, widget, data=None):
        pgc = self.TextEditor.get_pango_context()
        mets = pgc.get_metrics()
        self.MarkupBuffer.set_multiplier(Pango.units_to_double(mets.get_approximate_char_width()) + 1)


    def save_document(self, widget, data=None):
        if self.filename:
            logger.info("saving")
            filename = self.filename
            f = codecs.open(filename, encoding="utf-8", mode='w')
            f.write(self.get_text())
            f.close()
            if self.did_change:
                self.did_change = False
                title = self.get_title()
                self.set_headerbar_title(title[2:])
            return Gtk.ResponseType.OK

        else:
           
            filefilter = Gtk.FileFilter.new()
            filefilter.add_mime_type('text/x-markdown')
            filefilter.add_mime_type('text/plain')
            filefilter.set_name('MarkDown (.md)')
            filechooser = Gtk.FileChooserDialog(
                _("Save your File"),
                self,
                Gtk.FileChooserAction.SAVE,
                ("_Cancel", Gtk.ResponseType.CANCEL,
                 "_Save", Gtk.ResponseType.OK)
                )

            filechooser.set_do_overwrite_confirmation(True)
            filechooser.add_filter(filefilter)
            response = filechooser.run()
            if response == Gtk.ResponseType.OK:
                filename = filechooser.get_filename()
               
                if filename[-3:] != ".md":
                    filename = filename + ".md"
                    try:
                        self.recent_manager.add_item("file:/ " + filename)
                    except:
                        pass

                f = codecs.open(filename, encoding="utf-8", mode='w')

                f.write(self.get_text())
                f.close()
               
                self.filename = filename
                self.set_headerbar_title(os.path.basename(filename) + self.title_end)
               
                self.did_change = False
                filechooser.destroy()
                return response

            else:
                filechooser.destroy()
                return Gtk.ResponseType.CANCEL

    def save_document_as(self, widget, data=None):
        filechooser = Gtk.FileChooserDialog(
            "Save your File",
            self,
            Gtk.FileChooserAction.SAVE,
            ("_Cancel", Gtk.ResponseType.CANCEL,
             "_Save", Gtk.ResponseType.OK)
            )
        filechooser.set_do_overwrite_confirmation(True)
        if self.filename:
            filechooser.set_filename(self.filename)
        response = filechooser.run()
        if response == Gtk.ResponseType.OK:

            filename = filechooser.get_filename()
            if filename[-3:] != ".md":
                filename = filename + ".md"
                try:
                    self.recent_manager.remove_item("file:/" + filename)       
                    self.recent_manager.add_item("file:/ " + filename)
                except:
                    pass

            f = codecs.open(filename, encoding="utf-8", mode='w')
            f.write(self.get_text())
            f.close()
           
            self.filename = filename
            self.set_headerbar_title(os.path.basename(filename) + self.title_end)

            try:
                self.recent_manager.add_item(filename)
            except:
                pass
               
            filechooser.destroy()
            self.did_change = False

        else:
            filechooser.destroy()
            return Gtk.ResponseType.CANCEL

    def export(self, export_type="html"):
        filechooser = Gtk.FileChooserDialog(
            "Export as %s" % export_type.upper(),
            self,
            Gtk.FileChooserAction.SAVE,
            ("_Cancel", Gtk.ResponseType.CANCEL,
             "_Save", Gtk.ResponseType.OK)
            )

        filechooser.set_do_overwrite_confirmation(True)
        if self.filename:
            filechooser.set_filename(self.filename[:-2] + export_type.lower())
       
        response = filechooser.run()
        if response == Gtk.ResponseType.OK:
            filename = filechooser.get_filename()
            if filename.endswith("." + export_type):
                filename = filename[:-len(export_type)-1]
            filechooser.destroy()
        else:
            filechooser.destroy()
            return

        # Converting text to bytes for python 3
        text = bytes(self.get_text(), "utf-8")

        output_dir = os.path.abspath(os.path.join(filename, os.path.pardir))
       
        basename = os.path.basename(filename)

        args = ['pandoc', '--from=markdown', '-smart']
       
        if export_type == "pdf":
            args.append("-o%s.pdf" % basename)
       
        elif export_type == "odt":
            args.append("-o%s.odt" % basename)
       
        elif export_type == "html":
            css = helpers.get_media_file('uberwriter.css')
            args.append("-c%s" % css)
            args.append("-o%s.html" % basename)
            args.append("--mathjax")

        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=output_dir)
        output = p.communicate(text)[0]
       
        return filename
           
    def export_as_odt(self, widget, data=None):
        self.export("odt")

    def export_as_html(self, widget, data=None):
        self.export("html")

    def export_as_pdf(self, widget, data=None):
        if self.texlive_installed == False and APT_ENABLED:
            try:
                cache = apt.Cache()
                inst = cache["texlive"].is_installed
            except:
                inst = True

            if inst == False:
                dialog = Gtk.MessageDialog(self,
                    Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                    Gtk.MessageType.INFO,
                    Gtk.ButtonsType.NONE,
                    _("You can not export to PDF.")
                )
                dialog.format_secondary_markup(_("Please install <a href=\"apt:texlive\">texlive</a> from the software center."))
                response = dialog.run()
                return
            else:
                self.texlive_installed = True
        self.export("pdf")

    def copy_html_to_clipboard(self, widget, date=None):
        """Copies only html without headers etc. to Clipboard"""

        args = ['pandoc', '--from=markdown', '-smart', '-thtml']
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        text = bytes(self.get_text(), "utf-8")
        output = p.communicate(text)[0]
               
        cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        cb.set_text(output.decode("utf-8"), -1)
        cb.store()

    def open_document(self, widget):
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        if self.focusmode:
            self.focusmode_button.set_active(False)

        filefilter = Gtk.FileFilter.new()
        filefilter.add_mime_type('text/x-markdown')
        filefilter.add_mime_type('text/plain')
        filefilter.set_name(_('MarkDown or Plain Text'))

        filechooser = Gtk.FileChooserDialog(
            _("Open a .md-File"),
            self,
            Gtk.FileChooserAction.OPEN,
            ("_Cancel", Gtk.ResponseType.CANCEL,
             "_Open", Gtk.ResponseType.OK)
            )
        filechooser.add_filter(filefilter)
        response = filechooser.run()
        if response == Gtk.ResponseType.OK:
            filename = filechooser.get_filename()
            self.load_file(filename)
            filechooser.destroy()

        elif response == Gtk.ResponseType.CANCEL:
            filechooser.destroy()

    def check_change(self):
        if self.did_change and len(self.get_text()):
            dialog = Gtk.MessageDialog(self,
                Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                Gtk.MessageType.WARNING,
                Gtk.ButtonsType.NONE,
                _("You have not saved your changes.")
                )
            dialog.add_button(_("Close without Saving"), Gtk.ResponseType.NO)
            dialog.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("Save now"), Gtk.ResponseType.YES)
            dialog.set_title(_('Unsaved changes'))
            dialog.set_default_size(200, 150)
            dialog.set_default_response(Gtk.ResponseType.YES)
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                title = self.get_title()
                if self.save_document(widget = None) == Gtk.ResponseType.CANCEL:
                    dialog.destroy()
                    return self.check_change()
                else:                   
                    dialog.destroy()
                    return response
            elif response == Gtk.ResponseType.NO:
                dialog.destroy()
                return response
            else:
                dialog.destroy()
                return Gtk.ResponseType.CANCEL

    def new_document(self, widget):
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return
        else:
            self.TextBuffer.set_text('')
            self.TextEditor.undos = []
            self.TextEditor.redos = []

            self.did_change = False
            self.filename = None
            self.set_headerbar_title("New File" + self.title_end)

    def menu_activate_focusmode(self, widget=None):
        self.focusmode_button.emit('activate')

    def menu_activate_fullscreen(self, widget=None):
        self.fullscreen_button.emit('activate')

    def menu_toggle_sidebar(self, widget=None):
        self.sidebar.toggle_sidebar()

#    def menu_activate_preview(self, widget=None):
#        self.preview_button.emit('activate')

    def toggle_spellcheck(self, widget=None, data=None):
        if widget:
            if self.spellcheck:
                if widget.get_active():
                    self.SpellChecker.enable()
                else:
                    self.SpellChecker.disable()

            elif widget.get_active():
                self.SpellChecker = SpellChecker(self.TextEditor, self, locale.getdefaultlocale()[0], collapse=False)
                if self.auto_correct:
                    self.auto_correct.set_language(self.SpellChecker.language)
                    self.SpellChecker.connect_language_change(self.auto_correct.set_language)
                try:
                    self.spellcheck = True
                except:
                    self.SpellChecker = None
                    self.spellcheck = False
                    dialog = Gtk.MessageDialog(self,
                        Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                        Gtk.MessageType.INFO,
                        Gtk.ButtonsType.NONE,
                        _("You can not enable the Spell Checker.")
                    )
                    dialog.format_secondary_text(_("Please install 'hunspell' or 'aspell' dictionarys for your language from the software center."))
                    response = dialog.run()
                    return
        else:
            widget = self.spellcheck_button
            if self.spellcheck and self.SpellChecker.enabled():
                self.SpellChecker.disable()
                widget.set_active(False)
            else:
                self.SpellChecker.enable()
                widget.set_active(True)

        return

    def on_drag_data_received(self, widget, drag_context, x, y,
                              data, info, time):
        """Handle drag and drop events"""
        if info == 1:
            # uri target
            uris = data.get_uris()
            for uri in uris:
                uri = urllib.parse.unquote_plus(uri)
                mime = mimetypes.guess_type(uri)

                if mime[0] is not None and mime[0].startswith('image'):
                    if uri.startswith("file://"):
                        uri = uri[7:]
                    text = "![Insert image title here](%s)" % uri
                    ll = 2
                    lr = 23
                else:
                    text = "[Insert link title here](%s)" % uri
                    ll = 1
                    lr = 22
                self.TextBuffer.place_cursor(self.TextBuffer.get_iter_at_mark(
                    self.TextBuffer.get_mark('gtk_drag_target')))
                self.TextBuffer.insert_at_cursor(text)
                insert_mark = self.TextBuffer.get_insert()
                selection_bound = self.TextBuffer.get_selection_bound()
                cursor_iter = self.TextBuffer.get_iter_at_mark(insert_mark)
                cursor_iter.backward_chars(len(text) - ll)
                self.TextBuffer.move_mark(insert_mark, cursor_iter)
                cursor_iter.forward_chars(lr)
                self.TextBuffer.move_mark(selection_bound, cursor_iter)
       
        elif info == 2:
            # Text target
            self.TextBuffer.place_cursor(self.TextBuffer.get_iter_at_mark(
                self.TextBuffer.get_mark('gtk_drag_target')))
            self.TextBuffer.insert_at_cursor(data.get_text())
        Gtk.drag_finish(drag_context, True, True, time)
        self.present()
        return False

    def toggle_preview(self, widget, data=None):
        if widget.get_active():

            # Toggle buttons

            # self.preview_button.set_active(True)
            # self.preview_mnu_button.set_active(True)
            # Insert a tag with ID to scroll to
            # self.TextBuffer.insert_at_cursor('<span id="scroll_mark"></span>')
            # TODO
            # Find a way to find the next header, scroll to the next header.

            args = ['pandoc',
                    '--from=markdown',
                    '-smart',
                    '-thtml',
                    '--mathjax',
                    '-c', helpers.get_media_file('uberwriter.css')]

            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

            text = bytes(self.get_text(), "utf-8")
            output = p.communicate(text)[0]

            # Load in Webview and scroll to #ID
            self.webview = WebKit.WebView()
            self.webview_settings = self.webview.get_settings()
            self.webview_settings.set_allow_universal_access_from_file_urls(True)
            self.webview.load_html(output.decode("utf-8"), 'file://localhost/')

            # Delete the cursor-scroll mark again
            # cursor_iter = self.TextBuffer.get_iter_at_mark(self.TextBuffer.get_insert())
            # begin_del = cursor_iter.copy()
            # begin_del.backward_chars(30)
            # self.TextBuffer.delete(begin_del, cursor_iter)

            self.ScrolledWindow.remove(self.EditorViewport)
            self.ScrolledWindow.add(self.webview)
            self.webview.show()

            # This saying that all links will be opened in default browser, \
            # but local files are opened in appropriate apps:
            self.webview.connect("navigation-requested", self.on_click_link)
        else:
            self.ScrolledWindow.remove(self.webview)
            self.webview.destroy()
            self.ScrolledWindow.add(self.EditorViewport)
            self.TextEditor.show()
            
            # self.preview_button.set_active(False)
            # self.preview_mnu_button.set_active(False)

        self.queue_draw()
        return True

    def on_click_link(self, view, frame, req, data=None):
        # This provide ability for self.webview to open links in default browser
        if(req.get_uri().startswith("http://")):
            webbrowser.open(req.get_uri())
            return True # Don't let the event "bubble up"

    def dark_mode_toggled(self, widget, data=None):
        # Save state for saving settings later
        self.dark_mode = widget.get_active()
        if self.dark_mode:
            # Dark Mode is on
            self.gtk_settings.set_property('gtk-application-prefer-dark-theme', True)
            self.get_style_context().add_class("dark_mode")
            self.hb_container.get_style_context().add_class("dark_mode")
            self.MarkupBuffer.dark_mode(True)
        else:
            # Dark mode off
            self.gtk_settings.set_property('gtk-application-prefer-dark-theme', False)
            self.get_style_context().remove_class("dark_mode")
            self.hb_container.get_style_context().remove_class("dark_mode")
            self.MarkupBuffer.dark_mode(False)

        # Redraw contents of window (self)
        self.queue_draw()

    def load_file(self, filename=None):
        """Open File from command line or open / open recent etc."""
        if filename:
            if filename.startswith('file://'):
                filename = filename[7:]
            filename = urllib.parse.unquote_plus(filename)
            try:
                self.preview_button.set_active(False)
                if not os.path.exists(filename):
                    self.TextBuffer.set_text("")
                else:
                    f = codecs.open(filename, encoding="utf-8", mode='r')
                    self.TextBuffer.set_text(f.read())
                    f.close()
                    self.MarkupBuffer.markup_buffer(0)

                self.set_headerbar_title(os.path.basename(filename) + self.title_end)
                self.TextEditor.undo_stack = []
                self.TextEditor.redo_stack = []
                self.filename = filename

            except Exception as e:
                logger.warning("Error Reading File: %r" % e)
            self.did_change = False
        else:
            logger.warning("No File arg")

    # Help Menu
    def open_launchpad_translation(self, widget, data=None):
        webbrowser.open("https://translations.launchpad.net/uberwriter")

    def open_pandoc_markdown(self, widget, data=None):
        webbrowser.open("http://johnmacfarlane.net/pandoc/README.html#pandocs-markdown")

    def open_uberwriter_markdown(self, widget, data=None):
        self.load_file(helpers.get_media_file('uberwriter_markdown.md'))

    def open_search_and_replace(self, widget, data=None):
        self.searchreplace.toggle_search()

    def open_advanced_export(self, widget, data=None):
        if self.UberwriterAdvancedExportDialog is not None:
            advexp = self.UberwriterAdvancedExportDialog()  # pylint: disable=

            response = advexp.run()
            if response == 1:
                advexp.advanced_export(bytes(self.get_text(), "utf-8"))

            advexp.destroy()

    def open_recent(self, widget, data=None):
        if data:
            if self.check_change() == Gtk.ResponseType.CANCEL:
                return
            else:
                self.load_file(data)

    def generate_recent_files_menu(self, parent_menu):
        # Recent file filter
        self.recent_manager = Gtk.RecentManager.get_default()

        self.recent_files_menu = Gtk.RecentChooserMenu.new_for_manager(self.recent_manager)
        self.recent_files_menu.set_sort_type(Gtk.RecentSortType.MRU)

        recent_filter = Gtk.RecentFilter.new()
        recent_filter.add_mime_type('text/x-markdown')
        self.recent_files_menu.set_filter(recent_filter)
        menu = Gtk.Menu.new()

        for entry in self.recent_files_menu.get_items():
            if entry.exists():
                item = Gtk.MenuItem.new_with_label(entry.get_display_name())
                item.connect('activate', self.open_recent, entry.get_uri())
                menu.append(item)
                item.show()

        menu.show()
        parent_menu.set_submenu(menu)
        parent_menu.show()

    def poll_for_motion(self):
        if (self.was_motion == False
                and self.status_bar_visible
                and self.buffer_modified_for_status_bar
                and self.TextEditor.props.has_focus):
            # self.status_bar.set_state_flags(Gtk.StateFlags.INSENSITIVE, True)
            self.statusbar_revealer.set_reveal_child(False)
            self.hb_revealer.set_reveal_child(False)
            self.status_bar_visible = False
            self.buffer_modified_for_status_bar = False

        self.was_motion = False
        return True

    def on_motion_notify(self, widget, event, data=None):
        now = event.get_time()
        if now - self.timestamp_last_mouse_motion > 150:
            # filter out accidental motions
            self.timestamp_last_mouse_motion = now
            return
        if now - self.timestamp_last_mouse_motion < 100:
            # filter out accidental motion
            return
        if now - self.timestamp_last_mouse_motion > 100:
            # react on motion by fading in headerbar and statusbar
            if self.status_bar_visible == False:
                self.statusbar_revealer.set_reveal_child(True)
                self.hb_revealer.set_reveal_child(True)
                self.hb.props.opacity = 1
                self.status_bar_visible = True
                self.buffer_modified_for_status_bar = False
                self.update_line_and_char_count()
                # self.status_bar.set_state_flags(Gtk.StateFlags.NORMAL, True)
            self.was_motion = True

    def focus_out(self, widget, data=None):
        if self.status_bar_visible == False:
            self.statusbar_revealer.set_reveal_child(True)
            self.hb_revealer.set_reveal_child(True)
            self.hb.props.opacity = 1
            self.status_bar_visible = True
            self.buffer_modified_for_status_bar = False
            self.update_line_and_char_count()



    def draw_gradient(self, widget, cr):
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.ACTIVE)

        lg_top = cairo.LinearGradient(0, 0, 0, 80)
        lg_top.add_color_stop_rgba(0, bg_color.red, bg_color.green, bg_color.blue, 1)
        lg_top.add_color_stop_rgba(1, bg_color.red, bg_color.green, bg_color.blue, 0)

        width = widget.get_allocation().width
        height = widget.get_allocation().height

        cr.rectangle(0, 0, width, 80)
        cr.set_source(lg_top)
        cr.fill()
        cr.rectangle(0, height - 80, width, height)
        
        lg_btm = cairo.LinearGradient(0, height - 80, 0, height)
        lg_btm.add_color_stop_rgba(1, bg_color.red, bg_color.green, bg_color.blue, 1)
        lg_btm.add_color_stop_rgba(0, bg_color.red, bg_color.green, bg_color.blue, 0)

        cr.set_source(lg_btm)
        cr.fill()

    def use_experimental_features(self, val):
        try:
            self.auto_correct = UberwriterAutoCorrect(self.TextEditor, self.TextBuffer)
        except:
            logger.debug("Couldn't install autocorrect.")


    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the main window"""
        
        super(UberwriterWindow, self).finish_initializing(builder)
        

        self.UberwriterAdvancedExportDialog = UberwriterAdvancedExportDialog
        self.builder = builder
        

        self.connect('save-file', self.save_document)
        self.connect('save-file-as', self.save_document_as)
        self.connect('new-file', self.new_document)
        self.connect('open-file', self.open_document)
        self.connect('toggle-fullscreen', self.menu_activate_fullscreen)
        self.connect('toggle-focusmode', self.menu_activate_focusmode)
        #self.connect('toggle-preview', self.menu_activate_preview)
        self.connect('toggle-spellcheck', self.toggle_spellcheck)
        self.connect('close-window', self.on_mnu_close_activate)
        self.connect('toggle-search', self.open_search_and_replace)
        self.scroll_adjusted = False

        # Code for other initialization actions should be added here.

        # Texlive checker
        self.texlive_installed = False

        self.set_name('UberwriterWindow')
        

        self.use_headerbar = True
        if self.use_headerbar == True:
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

            bbtn = Gtk.MenuButton()
            btn_settings = Gtk.MenuButton()
            btn_settings.props.image = Gtk.Image.new_from_icon_name('emblem-system-symbolic', Gtk.IconSize.BUTTON)
            self.builder.get_object("menu4").detach()
            btn_settings.set_popup(self.builder.get_object("menu4"))

            self.builder.get_object("menu1").detach()
            bbtn.set_popup(self.builder.get_object("menu1"))
            self.hb.pack_start(bbtn)
            self.hb.pack_end(btn_settings)
            self.hb.show_all()
            self.testbits = Gdk.WindowState.MAXIMIZED
            #self.connect('draw', self.override_headerbar_background)

        self.title_end = "  –  UberWriter"
        self.set_headerbar_title("New File" + self.title_end)

        self.focusmode = False

        self.word_count = builder.get_object('word_count')
        self.char_count = builder.get_object('char_count')
        self.menubar = builder.get_object('menubar1')
        self.menubar.hide()
        

        # Wire up buttons
        self.fullscreen_button = builder.get_object('fullscreen_toggle')
        self.fullscreen_menu_button = builder.get_object('mnu_fullscreen')
        self.focusmode_button = builder.get_object('focus_toggle')
        self.focusmode_menu_button = builder.get_object('mnu_focusmode')
        self.preview_button = builder.get_object('preview_toggle')
        self.preview_mnu_button = builder.get_object('mnu_preview')

        self.fullscreen_button.set_name('fullscreen_toggle')
        self.focusmode_button.set_name('focus_toggle')
        self.preview_button.set_name('preview_toggle')

        # Setup status bar hide after 3 seconds

        self.status_bar = builder.get_object('status_bar_box')
        self.statusbar_revealer = builder.get_object('status_bar_revealer')
        self.status_bar.get_style_context().add_class('status_bar_box')
        self.status_bar_visible = True
        self.was_motion = True
        self.buffer_modified_for_status_bar = False
        self.connect("motion-notify-event", self.on_motion_notify)
        GObject.timeout_add(3000, self.poll_for_motion)

        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)

        # Setup light background
        self.TextEditor = TextEditor()
        self.TextEditor.set_name('UberwriterEditor')
        self.get_style_context().add_class('uberwriter_window')

        base_leftmargin = 40
        # self.TextEditor.set_left_margin(base_leftmargin)
        #self.TextEditor.set_left_margin(40)
        self.TextEditor.props.width_request = 600
        self.TextEditor.props.halign = Gtk.Align.CENTER
        self.TextEditor.set_vadjustment(builder.get_object('vadjustment1'))
        self.TextEditor.set_wrap_mode(Gtk.WrapMode.WORD)
        self.TextEditor.connect('focus-out-event', self.focus_out)
        self.TextEditor.get_style_context().connect('changed', self.style_changed)

        # self.TextEditor.install_style_property_parser

        self.TextEditor.show()
        self.TextEditor.grab_focus()

        self.ScrolledWindow = builder.get_object('editor_scrolledwindow')
        self.EditorAlignment = builder.get_object('editor_alignment')
        self.EditorAlignment.add(self.TextEditor)
        self.alignment_padding = 40
        self.EditorViewport = builder.get_object('editor_viewport')
        self.EditorViewport.connect_after("draw", self.draw_gradient)

        self.smooth_scroll_starttime = 0
        self.smooth_scroll_endtime = 0
        self.smooth_scroll_acttarget = 0
        self.smooth_scroll_data = {
            'target_pos': -1,
            'source_pos': -1, 
            'duration': 0
        }
        self.smooth_scroll_tickid = -1

        self.PreviewPane = builder.get_object('preview_scrolledwindow')

        self.TextEditor.set_margin_top(38)
        self.TextEditor.set_margin_bottom(16)

        self.TextEditor.set_pixels_above_lines(4)
        self.TextEditor.set_pixels_below_lines(4)
        self.TextEditor.set_pixels_inside_wrap(8)

        tab_array = Pango.TabArray.new(1, True)
        tab_array.set_tab(0, Pango.TabAlign.LEFT, 20)
        self.TextEditor.set_tabs(tab_array)

        self.TextBuffer = self.TextEditor.get_buffer()
        self.TextBuffer.set_text('')

        # Init Window height for top/bottom padding
        self.window_height = self.get_size()[1]

        self.text_change_event = self.TextBuffer.connect('changed', self.text_changed)

        # Init file name with None
        self.filename = None

        self.generate_recent_files_menu(self.builder.get_object('recent'))

        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_path(helpers.get_media_path('style.css'))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Markup and Shortcuts for the TextBuffer
        self.MarkupBuffer = MarkupBuffer(self, self.TextBuffer, base_leftmargin)
        self.MarkupBuffer.markup_buffer()

        # Scrolling -> Dark or not?
        self.textchange = False
        self.scroll_count = 0
        self.timestamp_last_mouse_motion = 0
        self.TextBuffer.connect_after('mark-set', self.mark_set)

        # Drag and drop

        # self.TextEditor.drag_dest_unset()
        # self.TextEditor.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.target_list = Gtk.TargetList.new([])
        self.target_list.add_uri_targets(1)
        self.target_list.add_text_targets(2)

        self.TextEditor.drag_dest_set_target_list(self.target_list)
        self.TextEditor.connect_after('drag-data-received', self.on_drag_data_received)
        def on_drop(widget, *args):
            print("drop")
        self.TextEditor.connect('drag-drop', on_drop)


        self.TextBuffer.connect('paste-done', self.paste_done)
        # self.connect('key-press-event', self.alt_mod)

        # Events for Typewriter mode

        # Setting up inline preview
        self.InlinePreview = UberwriterInlinePreview(self.TextEditor, self.TextBuffer)

        # Vertical scrolling
        self.vadjustment = self.ScrolledWindow.get_vadjustment()
        self.vadjustment.connect('value-changed', self.scrolled)


        self.spellcheck_button = builder.get_object("disable_spellcheck")
        # Setting up spellcheck
        self.auto_correct = None
        try:
            self.SpellChecker = SpellChecker(self.TextEditor,
                locale.getdefaultlocale()[0], collapse=False)
            if self.auto_correct:
                self.auto_correct.set_language(self.SpellChecker.language)
                self.SpellChecker.connect_language_change(self.auto_correct.set_language)

            self.spellcheck = True
        except:
            self.SpellChecker = None
            self.spellcheck = False
            builder.get_object("disable_spellcheck").set_active(False)

        if self.spellcheck:
            self.SpellChecker.append_filter('[#*]+', SpellChecker.FILTER_WORD)

        self.did_change = False

        ###
        #   Sidebar initialization test
        ###
        self.paned_window = builder.get_object("main_pained")
        self.sidebar_box = builder.get_object("sidebar_box")
        self.sidebar = UberwriterSidebar(self)
        self.sidebar_box.hide()

        ###
        #   Search and replace initialization
        #   Same interface as Sidebar ;)
        ###
        self.searchreplace = UberwriterSearchAndReplace(self)


        # Window resize
        self.window_resize(self)
        self.connect("configure-event", self.window_resize)
        self.connect("delete-event", self.on_delete_called)

        self.gtk_settings = Gtk.Settings.get_default()
        self.load_settings(builder)

        # self.plugins = [BibTex(self)]

        # self.connect_after('realize', self.color_window)

    # def color_window(self, widget, data=None):
    #   window_gdk = self.get_window()
    #   window_gdk.set_background(Gdk.Color(0, 1, 0))

    def alt_mod(self, widget, event, data=None):
        # TODO: Click and open when alt is pressed
        if event.state & Gdk.ModifierType.MOD2_MASK:
            logger.info("Alt pressed")
        return

    def on_delete_called(self, widget, data=None):
        """Called when the TexteditorWindow is closed."""
        logger.info('delete called')
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return True
        return False

    def on_mnu_close_activate(self, widget, data=None):
        """
            Signal handler for closing the UberwriterWindow.
            Overriden from parent Window Class
        """
        if self.on_delete_called(self):  # Really destroy?
            return
        else:
            self.destroy()
        return

    def on_destroy(self, widget, data=None):
        """Called when the TexteditorWindow is closed."""
        # Clean up code for saving application state should be added here.
        self.save_settings()
        Gtk.main_quit()

    def set_headerbar_title(self, title):
        if self.use_headerbar:
            self.hb.props.title = title
        self.set_title(title)

    def save_settings(self):
        if not os.path.exists(CONFIG_PATH):
            try:
                os.makedirs(CONFIG_PATH)
            except Exception as e:
                logger.debug("Failed to make uberwriter config path in\
                     ~/.config/uberwriter. Error: %r" % e)
        try:
            settings = dict()
            settings["dark_mode"] = self.dark_mode
            settings["spellcheck"] = self.SpellChecker.enabled
            f = open(CONFIG_PATH + "settings.pickle", "wb+")
            pickle.dump(settings, f)
            f.close()
            logger.debug("Saved settings: %r" % settings)
        except Exception as e:
            logger.debug("Error writing settings file to disk. Error: %r" % e)

    def load_settings(self, builder):
        dark_mode_button = builder.get_object("dark_mode")
        spellcheck_button = builder.get_object("disable_spellcheck")
        try:
            f = open(CONFIG_PATH + "settings.pickle", "rb")
            settings = pickle.load(f)
            f.close()
            self.dark_mode = settings['dark_mode']
            dark_mode_button.set_active(settings['dark_mode'])
            spellcheck_button.set_active(settings['spellcheck'])
            logger.debug("loaded settings: %r" % settings)
        except Exception as e:
            logger.debug("(First Run?) Error loading settings from home dir. \
                Error: %r", e)
        return True
