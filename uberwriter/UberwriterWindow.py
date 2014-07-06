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

from gi.repository import Gtk, Gdk, GObject, WebKit # pylint: disable=E0611
from gi.repository import Pango # pylint: disable=E0611

import cairo

import re


from .MarkupBuffer import MarkupBuffer
from .FormatShortcuts import FormatShortcuts
from .UberwriterTextEditor import TextEditor
from .UberwriterInlinePreview import UberwriterInlinePreview

import logging
logger = logging.getLogger('uberwriter')

# Spellcheck

import locale
try:
    from gtkspellcheck import SpellChecker
except ImportError:
    from uberwriter_lib.gtkspellcheck import SpellChecker

try:
    import apt
    APT_ENABLED = True
except:
    APT_ENABLED = False

from uberwriter_lib import Window
from uberwriter_lib import helpers
from .AboutUberwriterDialog import AboutUberwriterDialog
from .UberwriterAdvancedExportDialog import UberwriterAdvancedExportDialog

# Some Globals 
# TODO move them somewhere for better 
# accesibility from other files

CONFIG_PATH = os.path.expanduser("~/.config/uberwriter/")



# gtk_text_view_forward_display_line_end () !! !
# move-viewport signal
# See texteditor_lib.Window.py for more details about how this class works
class UberwriterWindow(Window):

    __gtype_name__ = "UberwriterWindow"

    def scrolled(self, widget):
        """if window scrolled + focusmode make font black again"""
        if self.focusmode:
            if self.textchange == False:
                if self.scroll_count >= 1:
                    self.TextBuffer.apply_tag(
                        self.MarkupBuffer.blackfont, 
                        self.TextBuffer.get_start_iter(), 
                        self.TextBuffer.get_end_iter())
                else:
                    self.scroll_count += 1
            else: 
                self.scroll_count = 0
                self.typewriter()
                self.textchange = False

    def after_modify_text(self, *arg):
        if self.focusmode:
            self.typewriter()

    def after_insert_at_cursor(self, *arg):
        if self.focusmode:
            self.typewriter()

    def paste_done(self, *args):
        self.MarkupBuffer.markup_buffer(0)

    def init_typewriter(self):

        self.TextBuffer.disconnect(self.TextEditor.delete_event)
        self.TextBuffer.disconnect(self.TextEditor.insert_event)
        self.TextBuffer.disconnect(self.text_change_event)

        ci = self.TextBuffer.get_iter_at_mark(self.TextBuffer.get_mark('insert'))
        co = ci.get_offset()

        fflines = int(round((self.window_height-55)/(2*30)))
        self.fflines = fflines
        self.TextEditor.fflines = fflines

        s = '\n'*fflines

        start_iter =  self.TextBuffer.get_iter_at_offset(0)
        self.TextBuffer.insert(start_iter, s)
        
        end_iter =  self.TextBuffer.get_iter_at_offset(-1)
        self.TextBuffer.insert(end_iter, s)

        ne_ci = self.TextBuffer.get_iter_at_offset(co + fflines)
        self.TextBuffer.place_cursor(ne_ci)

        # Scroll it to the center
        self.TextEditor.scroll_to_mark(self.TextBuffer.get_mark('insert'), 0.0, True, 0.0, 0.5)

        self.TextEditor.insert_event = self.TextBuffer.connect("insert-text",self.TextEditor._on_insert)
        self.TextEditor.delete_event = self.TextBuffer.connect("delete-range",self.TextEditor._on_delete)
        self.text_change_event = self.TextBuffer.connect('changed', self.text_changed)

        self.typewriter_initiated = True

    def typewriter(self):
        cursor = self.TextBuffer.get_mark("insert")
        cursor_iter = self.TextBuffer.get_iter_at_mark(cursor)
        self.TextEditor.scroll_to_iter(cursor_iter, 0.0, True, 0.0, 0.5)

    def remove_typewriter(self):
        self.TextBuffer.disconnect(self.TextEditor.delete_event)
        self.TextBuffer.disconnect(self.TextEditor.insert_event)
        self.TextBuffer.disconnect(self.text_change_event)

        startIter = self.TextBuffer.get_start_iter()
        endLineIter = startIter.copy()
        endLineIter.forward_lines(self.fflines)
        self.TextBuffer.delete(startIter, endLineIter)
        startIter = self.TextBuffer.get_end_iter()
        endLineIter = startIter.copy()
        
        # Move to line before last line
        endLineIter.backward_lines(self.fflines - 1)
        
        # Move to last char in last line
        endLineIter.backward_char()
        self.TextBuffer.delete(startIter, endLineIter)

        self.fflines = 0
        self.TextEditor.fflines = 0

        self.TextEditor.insert_event = self.TextBuffer.connect("insert-text",self.TextEditor._on_insert)
        self.TextEditor.delete_event = self.TextBuffer.connect("delete-range",self.TextEditor._on_delete)
        self.text_change_event = self.TextBuffer.connect('changed', self.text_changed)


    WORDCOUNT = re.compile(r"[\s#*\+\-]+", re.UNICODE)
    def update_line_and_char_count(self):
        if self.status_bar_visible == False:
            return

        self.char_count.set_text(str(self.TextBuffer.get_char_count() - 
                (2 * self.fflines)))

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

        # TODO rename line_count to word_count

    def get_text(self):
        if self.focusmode == False:
            start_iter = self.TextBuffer.get_start_iter()
            end_iter = self.TextBuffer.get_end_iter()

        else:
            start_iter = self.TextBuffer.get_iter_at_line(self.fflines)
            rbline =  self.TextBuffer.get_line_count() - self.fflines
            end_iter = self.TextBuffer.get_iter_at_line(rbline)

        return self.TextBuffer.get_text(start_iter, end_iter, False)

    def mark_set(self, buffer, location, mark, data=None):
        if self.focusmode and (mark.get_name() == 'insert' or
            mark.get_name() == 'selection_bound'):
            akt_lines = self.TextBuffer.get_line_count()
            lb = self.fflines
            rb = akt_lines - self.fflines
            #print "a %d, lb %d, rb %d" % (akt_lines, lb, rb)
            #lb = self.TextBuffer.get_iter_at_line(self.fflines)
            #rbline =  self.TextBuffer.get_line_count() - self.fflines
            #rb = self.TextBuffer.get_iter_at_line(
            #   rbline)
            #rb.backward_line()
            

            linecount = location.get_line()
            #print "a %d, lb %d, rb %d, lc %d" % (akt_lines, lb, rb, linecount)

            if linecount < lb:
                move_to_line = self.TextBuffer.get_iter_at_line(lb)
                self.TextBuffer.move_mark(mark, move_to_line)
            elif linecount >= rb:
                move_to_line = self.TextBuffer.get_iter_at_line(rb)
                move_to_line.backward_char()
                self.TextBuffer.move_mark(mark, move_to_line)

    def after_mark_set(self, buffer, location, mark, data=None):
        if self.focusmode and mark.get_name() == 'insert':
            self.typewriter()


    def delete_from_cursor(self, editor, typ, count, Data=None):
        if not self.focusmode:
            return
        cursor = self.TextBuffer.get_mark("insert")
        cursor_iter = self.TextBuffer.get_iter_at_mark(cursor)
        if count < 0 and cursor_iter.starts_line():
            lb = self.fflines
            linecount = cursor_iter.get_line()
            #print "lb %d, lc %d" % (lb, linecount)
            if linecount <= lb:
                self.TextEditor.emit_stop_by_name('delete-from-cursor')
        elif count > 0 and cursor_iter.ends_line():
            akt_lines = self.TextBuffer.get_line_count()
            rb = akt_lines - self.fflines
            linecount = cursor_iter.get_line() + 1
            #print "rb %d, lc %d" % (rb, linecount)
            if linecount >= rb:
                self.TextEditor.emit_stop_by_name('delete-from-cursor')

    def backspace(self, data=None):
        if not self.focusmode:
            return

        cursor = self.TextBuffer.get_mark("insert")
        cursor_iter = self.TextBuffer.get_iter_at_mark(cursor)
        if cursor_iter.starts_line():
            lb = self.fflines
            linecount = cursor_iter.get_line()
            #print "lb %d, lc %d" % (lb, linecount)

            if linecount <= lb:
                self.TextEditor.emit_stop_by_name('backspace')


    def cursor_moved(self, widget, a, b, data=None):
        pass

    def after_cursor_moved(self, widget, step, count, extend_selection, data=None):
        if self.focusmode:
            self.typewriter()

    def text_changed(self, widget, data=None):
        if self.did_change == False:
            self.did_change = True
            title = self.get_title()
            self.set_title("* " + title)

        self.MarkupBuffer.markup_buffer(1)
        self.textchange = True

        self.buffer_modified_for_status_bar = True
        self.update_line_and_char_count()

    def toggle_fullscreen(self, widget, data=None):
        if widget.get_active():
            self.fullscreen()
            key, mod = Gtk.accelerator_parse("Escape")
            self.fullscreen_button.add_accelerator("activate", 
            self.accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
            
            # Hide Menu
            self.menubar.hide()

        else:
            self.unfullscreen()
            key, mod = Gtk.accelerator_parse("Escape")
            self.fullscreen_button.remove_accelerator(
                self.accel_group, key, mod)
            self.menubar.show()

        self.TextEditor.grab_focus()

    def delete_text(self, widget):
        pass

    def cut_text(self, widget, data=None):
        self.TextEditor.cut()

    def paste_text(self, widget, data=None):
        self.TextEditor.paste()

    def copy_text(self, widget, data=None):
        self.TextEditor.copy()

    def undo(self, widget, data=None):
        self.TextEditor.undo()

    def redo(self, widget, data=None):
        self.TextEditor.redo()

    def set_italic(self, widget, data=None):
        """Ctrl + I"""
        self.FormatShortcuts.italic()

    def set_bold(self, widget, data=None):
        """Ctrl + B"""
        self.FormatShortcuts.bold()

    def insert_horizontal_rule(self, widget, data=None):
        """Ctrl + R"""
        self.FormatShortcuts.rule()

    def insert_unordered_list_item(self, widget, data=None):
        """Ctrl + U"""
        self.FormatShortcuts.unordered_list_item()

    def insert_ordered_list(self, widget, data=None):
        """CTRL + O"""
        self.FormatShortcuts.ordered_list_item()

    def insert_heading(self, widget, data=None):
        """CTRL + H"""
        self.FormatShortcuts.heading()

    def set_focusmode(self, widget, data=None):
        if widget.get_active():
            self.init_typewriter()
            self.MarkupBuffer.focusmode_highlight()
            self.focusmode = True
            self.TextEditor.grab_focus()
            
            if self.spellcheck != False:
                self.SpellChecker._misspelled.set_property('underline', 0)
            
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
            
            if self.spellcheck != False:
                self.SpellChecker._misspelled.set_property('underline', 4)

    def window_resize(self, widget, data=None):
        # To calc padding top / bottom
        self.window_height = widget.get_size()[1]

        # Calculate left / right margin
        lm = (widget.get_size()[0] - 600) / 2
            
        self.TextEditor.set_left_margin(lm)
        self.TextEditor.set_right_margin(lm)

        self.MarkupBuffer.recalculate(lm)

        if self.focusmode:
            self.remove_typewriter()
            self.init_typewriter()

    def window_close(self, widget, data=None):
        return True


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
                self.set_title(title[2:])
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
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
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
                self.set_title(os.path.basename(filename) + self.title_end)
                
                self.did_change = False
                filechooser.destroy()
                return response

            elif response == Gtk.ResponseType.CANCEL:
                filechooser.destroy()
                return response

    def save_document_as(self, widget, data=None):
        filechooser = Gtk.FileChooserDialog(
            "Save your File",
            self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
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
            self.set_title(os.path.basename(filename) + self.title_end)

            try:
                self.recent_manager.add_item(filename)
            except:
                pass
                
            filechooser.destroy()
            self.did_change = False

        elif response == Gtk.ResponseType.CANCEL:
            filechooser.destroy()

    def export(self, export_type="html"):
        filechooser = Gtk.FileChooserDialog(
            "Export as %s" % export_type.upper(),
            self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
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

        args = ['pandoc', '--from=markdown', '--smart']
        
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
                    None, 
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

        args = ['pandoc', '--from=markdown', '--smart', '-thtml']
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        text = bytes(self.get_text(), "utf-8")
        output = p.communicate(text)[0]
                
        cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        cb.set_text(output.decode("utf-8"), -1)
        cb.store()

    def open_document(self, widget):
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        filefilter = Gtk.FileFilter.new()
        filefilter.add_mime_type('text/x-markdown')
        filefilter.add_mime_type('text/plain')
        filefilter.set_name(_('MarkDown or Plain Text'))

        filechooser = Gtk.FileChooserDialog(
            _("Open a .md-File"),
            self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
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
                None, 
                _("You have not saved your changes.")
                )
            dialog.add_button(_("Close without Saving"), Gtk.ResponseType.NO)
            dialog.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("Save now"), Gtk.ResponseType.YES).grab_focus()
            dialog.set_title(_('Unsaved changes'))
            dialog.set_default_size(200, 150)
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                title = self.get_title()
                if self.save_document(widget = None) == Gtk.ResponseType.CANCEL:
                    dialog.destroy()
                    return self.check_change()
                else:                    
                    dialog.destroy()
                    return response
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                return response
            elif response == Gtk.ResponseType.NO:
                dialog.destroy()
                return response

    def new_document(self, widget):
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return
        else:
            self.TextBuffer.set_text('')
            self.TextEditor.undos = []
            self.TextEditor.redos = []

            self.did_change = False
            self.filename = None
            self.set_title("New File" + self.title_end)

    def menu_activate_focusmode(self, widget):
        self.focusmode_button.emit('activate')

    def menu_activate_fullscreen(self, widget):
        self.fullscreen_button.emit('activate')

    def menu_activate_preview(self, widget):
        self.preview_button.emit('activate')

    # Not added as menu button as of now. Standard is typewriter active.
    def toggle_typewriter(self, widget, data=None):
        self.typewriter_active = widget.get_active()

    def toggle_spellcheck(self, widget, data=None):
        if self.spellcheck:
            if widget.get_active():
                self.SpellChecker.enable()
            else:
                self.SpellChecker.disable()
        elif widget.get_active(): 
            try:
                self.SpellChecker = SpellChecker(self.TextEditor, locale.getdefaultlocale()[0], collapse=False)
                self.spellcheck = True
            except:
                self.SpellChecker = None
                self.spellcheck = False
                dialog = Gtk.MessageDialog(self,
                    Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                    Gtk.MessageType.INFO,
                    None, 
                    _("You can not enable the Spell Checker.")
                )
                dialog.format_secondary_text(_("Please install 'hunspell' or 'aspell' dictionarys for your language from the software center."))
                response = dialog.run()
                return
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
                    text = "![Insert image title here](%s)" % uri
                    ll = 2
                    lr = 23
                else:
                    text = "[Insert link title here](%s)" % uri
                    ll = 1
                    lr = 22

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
            self.TextBuffer.insert_at_cursor(data.get_text())

        self.present()

    def toggle_preview(self, widget, data=None):
        if widget.get_active():
            # Insert a tag with ID to scroll to
            self.TextBuffer.insert_at_cursor('<span id="scroll_mark"></span>')

            args = ['pandoc', 
                    '--from=markdown', 
                    '--smart', 
                    '-thtml', 
                    '--mathjax', 
                    '-c', helpers.get_media_file('uberwriter.css')]
            
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            
            text = bytes(self.get_text(), "utf-8")
            output = p.communicate(text)[0]

            # Load in Webview and scroll to #ID
            self.webview = WebKit.WebView()
            self.webview.load_html_string(output.decode("utf-8"), 'file://localhost/' + '#scroll_mark')

            # Delete the cursor-scroll mark again
            cursor_iter = self.TextBuffer.get_iter_at_mark(self.TextBuffer.get_insert())
            begin_del = cursor_iter.copy()
            begin_del.backward_chars(30)
            self.TextBuffer.delete(begin_del, cursor_iter)

            self.ScrolledWindow.remove(self.TextEditor)
            self.ScrolledWindow.add(self.webview)
            self.webview.show()

            # Making the background white

            white_background = helpers.get_media_path('white.png')
            surface = cairo.ImageSurface.create_from_png(white_background)
            self.background_pattern = cairo.SurfacePattern(surface)
            self.background_pattern.set_extend(cairo.EXTEND_REPEAT)
            # This saying that all links will be opened in default browser, but local files are opened in appropriate apps:
            
            self.webview.connect("navigation-requested", self.on_click_link)
        else:
            self.ScrolledWindow.remove(self.webview)
            self.webview.destroy()
            self.ScrolledWindow.add(self.TextEditor)
            self.TextEditor.show()
            surface = cairo.ImageSurface.create_from_png(self.background_image)            
            self.background_pattern = cairo.SurfacePattern(surface)
            self.background_pattern.set_extend(cairo.EXTEND_REPEAT)
        self.queue_draw()

    def on_click_link(self, view, frame, req, data=None):
        # This provide ability for self.webview to open links in default browser
        webbrowser.open(req.get_uri())
        return True # that string is god-damn-important: without it link will be opened in default browser AND also in self.webview

    def dark_mode_toggled(self, widget, data=None):
        # Save state for saving settings later
        self.dark_mode = widget.get_active()
        if self.dark_mode:
            # Dark Mode is on
            css = open(helpers.get_media_path('style_dark.css'), 'rb')
            css_data = css.read()
            css.close()
            self.style_provider.load_from_data(css_data)
            self.background_image = helpers.get_media_path('bg_dark.png')
            self.MarkupBuffer.dark_mode(True)

        else: 
            # Dark mode off
            css = open(helpers.get_media_path('style.css'), 'rb')
            css_data = css.read()
            css.close()
            self.style_provider.load_from_data(css_data)
            self.background_image = helpers.get_media_path('bg_light.png')
            self.MarkupBuffer.dark_mode(False)

        surface = cairo.ImageSurface.create_from_png(self.background_image)
        self.background_pattern = cairo.SurfacePattern(surface)
        self.background_pattern.set_extend(cairo.EXTEND_REPEAT)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        # Redraw contents of window (self)
        self.queue_draw()

    def load_file(self, filename = None):
        """Open File from command line or open / open recent etc."""
        if filename:
            if filename.startswith('file://'):
                filename = filename[7:]
            filename = urllib.parse.unquote_plus(filename)
            try:
                self.preview_button.set_active(False)
                self.filename = filename
                f = codecs.open(filename, encoding="utf-8", mode='r')
                self.TextBuffer.set_text(f.read())
                f.close()
                self.MarkupBuffer.markup_buffer(0)
                self.set_title(os.path.basename(filename) + self.title_end)
                self.TextEditor.undos = []
                self.TextEditor.redos = []
            
            except Exception as e:
                logger.warning("Error Reading File: %r" % e)
            self.did_change = False
        else:
            logger.warning("No File arg")

    def draw_bg(self, widget, context):
        context.set_source(self.background_pattern)
        context.paint()

    # Help Menu
    def open_launchpad_translation(self, widget, data = None):
        webbrowser.open("https://translations.launchpad.net/uberwriter")

    def open_launchpad_help(self, widget, data = None):
        webbrowser.open("https://answers.launchpad.net/uberwriter")

    def open_pandoc_markdown(self, widget, data=None):
        webbrowser.open("http://johnmacfarlane.net/pandoc/README.html#pandocs-markdown")

    def open_uberwriter_markdown(self, widget, data=None):
        self.load_file(helpers.get_media_file('uberwriter_markdown.md'))

    def open_advanced_export(self, widget, data=None):
        if self.UberwriterAdvancedExportDialog is not None:
            advexp = self.UberwriterAdvancedExportDialog() # pylint: disable=

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
                and self.buffer_modified_for_status_bar):
            self.status_bar.set_state_flags(Gtk.StateFlags.INSENSITIVE, True)
            self.status_bar_visible = False
            self.buffer_modified_for_status_bar = False
            return False

        self.was_motion = False
        return True

    def on_motion_notify(self, widget, data=None):
        self.was_motion = True
        if self.status_bar_visible == False:
            self.status_bar_visible = True
            self.buffer_modified_for_status_bar = False
            self.update_line_and_char_count()
            self.status_bar.set_state_flags(Gtk.StateFlags.NORMAL, True)
            GObject.timeout_add(3000, self.poll_for_motion)

    def move_popup(self, widget, data=None):
        pass
        
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(UberwriterWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutUberwriterDialog
        self.UberwriterAdvancedExportDialog = UberwriterAdvancedExportDialog

        # Code for other initialization actions should be added here.
        
        # Texlive checker

        self.texlive_installed = False

        # Draw background
        self.background_image = helpers.get_media_path('bg_light.png')
        self.connect('draw', self.draw_bg)

        self.set_name('UberwriterWindow')

        self.title_end = "  –  UberWriter"
        self.set_title("New File" + self.title_end)

        # Drag and drop
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        
        self.target_list = Gtk.TargetList.new([])
        self.target_list.add_uri_targets(1)
        self.target_list.add_text_targets(2)

        self.drag_dest_set_target_list(self.target_list)

        self.focusmode = False

        self.word_count = builder.get_object('word_count')
        self.char_count = builder.get_object('char_count')
        self.menubar = builder.get_object('menubar1')
        
        # Wire up buttons
        self.fullscreen_button = builder.get_object('fullscreen_toggle')
        self.focusmode_button = builder.get_object('focus_toggle')
        self.preview_button = builder.get_object('preview_toggle')

        self.fullscreen_button.set_name('fullscreen_toggle')
        self.focusmode_button.set_name('focus_toggle')
        self.preview_button.set_name('preview_toggle')
        
        # Setup status bar hide after 3 seconds

        self.status_bar = builder.get_object('status_bar_box')
        self.status_bar.set_name('status_bar_box')
        self.status_bar_visible = True
        self.was_motion = True
        self.buffer_modified_for_status_bar = False
        self.connect("motion-notify-event", self.on_motion_notify)
        GObject.timeout_add(3000, self.poll_for_motion)

        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)

        # Setup light background

        surface = cairo.ImageSurface.create_from_png(self.background_image)
        self.background_pattern = cairo.SurfacePattern(surface)
        self.background_pattern.set_extend(cairo.EXTEND_REPEAT)

        self.TextEditor = TextEditor()

        base_leftmargin = 100
        self.TextEditor.set_left_margin(base_leftmargin)
        self.TextEditor.set_left_margin(40)

        self.TextEditor.set_wrap_mode(Gtk.WrapMode.WORD)

        self.TextEditor.show()

        self.ScrolledWindow = builder.get_object('editor_scrolledwindow')
        self.ScrolledWindow.add(self.TextEditor)
        
        self.PreviewPane = builder.get_object('preview_scrolledwindow')

        pangoFont = Pango.FontDescription("Ubuntu Mono 15px")

        self.TextEditor.modify_font(pangoFont)

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
        
        self.TextEditor.connect('move-cursor', self.cursor_moved)

        # Init file name with None
        self.filename = None

        self.generate_recent_files_menu(self.builder.get_object('recent'))

        self.style_provider = Gtk.CssProvider()

        css = open(helpers.get_media_path('style.css'), 'rb')
        css_data = css.read()
        css.close()

        self.style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
 
        # Still needed.
        self.fflines = 0

        # Markup and Shortcuts for the TextBuffer
        self.MarkupBuffer = MarkupBuffer(self, self.TextBuffer, base_leftmargin)
        self.MarkupBuffer.markup_buffer()
        self.FormatShortcuts = FormatShortcuts(self.TextBuffer, self.TextEditor)

        # Scrolling -> Dark or not?
        self.textchange = False
        self.scroll_count = 0

        self.TextBuffer.connect('mark-set', self.mark_set)
        
        self.TextEditor.drag_dest_unset()

        # Events to preserve margin. (To be deleted.)
        self.TextEditor.connect('delete-from-cursor', self.delete_from_cursor)
        self.TextEditor.connect('backspace', self.backspace)

        self.TextBuffer.connect('paste-done', self.paste_done)
        # self.connect('key-press-event', self.alt_mod)

        # Events for Typewriter mode
        self.TextBuffer.connect_after('mark-set', self.after_mark_set)
        self.TextBuffer.connect_after('changed', self.after_modify_text)
        self.TextEditor.connect_after('move-cursor', self.after_cursor_moved)
        self.TextEditor.connect_after('insert-at-cursor', self.after_insert_at_cursor)

        # Setting up inline preview
        self.InlinePreview = UberwriterInlinePreview(self.TextEditor, self.TextBuffer)

        # Vertical scrolling
        self.vadjustment = self.TextEditor.get_vadjustment()
        self.vadjustment.connect('value-changed', self.scrolled)

        # Setting up spellcheck
        try:
            self.SpellChecker = SpellChecker(self.TextEditor, locale.getdefaultlocale()[0], collapse=False)
            self.spellcheck = True
        except:
            self.SpellChecker = None
            self.spellcheck = False
            builder.get_object("disable_spellcheck").set_active(False)

        if self.spellcheck:
            self.SpellChecker.append_filter('[#*]+', SpellChecker.FILTER_WORD)

        self.did_change = False

        # Window resize
        self.connect("configure-event", self.window_resize)
        self.connect("delete-event", self.on_delete_called)
        self.load_settings(builder)

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
        if self.on_delete_called(self): #Really destroy?
            return 
        else: 
            self.destroy()        
        return 

    def on_destroy(self, widget, data=None):
        """Called when the TexteditorWindow is closed."""
        # Clean up code for saving application state should be added here.
        self.window_close(widget)        
        self.save_settings()
        Gtk.main_quit()

    def save_settings(self):
        
        if not os.path.exists(CONFIG_PATH):
            try:
                os.makedirs(CONFIG_PATH)
            except Exception as e:
                log.debug("Failed to make uberwriter config path in ~/.config/uberwriter. Error: %r" % e)
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
            logger.debug("(First Run?) Error loading settings from home dir. Error: %r", e)
        return 1