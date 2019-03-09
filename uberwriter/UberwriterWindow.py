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

import locale
import subprocess
import os
import codecs
import webbrowser
import urllib
import logging

import mimetypes
import re

from gettext import gettext as _

import gi
gi.require_version('WebKit2', '4.0') # pylint: disable=wrong-import-position
from gi.repository import Gtk, Gdk, GObject, GLib, Gio  # pylint: disable=E0611
from gi.repository import WebKit2 as WebKit
from gi.repository import Pango  # pylint: disable=E0611

import cairo
# import cairo.Pattern, cairo.SolidPattern

from . import headerbars
from uberwriter_lib import helpers
from uberwriter_lib.helpers import get_builder
from uberwriter_lib.gtkspellcheck import SpellChecker

from .MarkupBuffer import MarkupBuffer
from .UberwriterTextEditor import TextEditor
from .UberwriterInlinePreview import UberwriterInlinePreview
from .UberwriterSidebar import UberwriterSidebar
from .UberwriterSearchAndReplace import UberwriterSearchAndReplace
from .Settings import Settings
# from .UberwriterAutoCorrect import UberwriterAutoCorrect

from .UberwriterExportDialog import Export
# from .plugins.bibtex import BibTex
# Some Globals
# TODO move them somewhere for better
# accesibility from other files

LOGGER = logging.getLogger('uberwriter')

CONFIG_PATH = os.path.expanduser("~/.config/uberwriter/")

# See texteditor_lib.Window.py for more details about how this class works

class UberwriterWindow(Gtk.ApplicationWindow):

    #__gtype_name__ = "UberwriterWindow"
    WORDCOUNT = re.compile(r"(?!\-\w)[\s#*\+\-]+", re.UNICODE)

    def __init__(self, app):
        """Set up the main window"""

        Gtk.ApplicationWindow.__init__(self,
                                       application=Gio.Application.get_default(),
                                       title="Uberwriter")

        self.builder = get_builder('UberwriterWindow')
        self.add(self.builder.get_object("FullscreenOverlay"))

        self.set_default_size(850, 500)

        # preferences
        self.settings = Settings.new()

        self.set_name('UberwriterWindow')

        # Headerbars
        self.headerbar = headerbars.MainHeaderbar(app)
        self.set_titlebar(self.headerbar.hb_container)
        self.fs_headerbar = headerbars.FsHeaderbar(self.builder, app)

        self.title_end = "  –  UberWriter"
        self.set_headerbar_title("New File" + self.title_end)

        self.focusmode = False

        self.word_count = self.builder.get_object('word_count')
        self.char_count = self.builder.get_object('char_count')

        # Setup status bar hide after 3 seconds

        self.status_bar = self.builder.get_object('status_bar_box')
        self.statusbar_revealer = self.builder.get_object('status_bar_revealer')
        self.status_bar.get_style_context().add_class('status_bar_box')
        self.status_bar_visible = True
        self.was_motion = True
        self.buffer_modified_for_status_bar = False

        if self.settings.get_value("poll-motion"):
            self.connect("motion-notify-event", self.on_motion_notify)
            GObject.timeout_add(3000, self.poll_for_motion)

        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)

        # Setup light background
        self.text_editor = TextEditor()
        self.text_editor.set_name('UberwriterEditor')
        self.get_style_context().add_class('uberwriter_window')

        base_leftmargin = 100
        self.text_editor.set_left_margin(base_leftmargin)
        self.text_editor.set_left_margin(40)
        self.text_editor.set_top_margin(80)
        self.text_editor.props.width_request = 600
        self.text_editor.props.halign = Gtk.Align.CENTER
        self.text_editor.set_vadjustment(self.builder.get_object('vadjustment1'))
        self.text_editor.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_editor.connect('focus-out-event', self.focus_out)
        self.text_editor.get_style_context().connect('changed', self.style_changed)

        self.text_editor.set_top_margin(80)
        self.text_editor.set_bottom_margin(16)

        self.text_editor.set_pixels_above_lines(4)
        self.text_editor.set_pixels_below_lines(4)
        self.text_editor.set_pixels_inside_wrap(8)

        tab_array = Pango.TabArray.new(1, True)
        tab_array.set_tab(0, Pango.TabAlign.LEFT, 20)
        self.text_editor.set_tabs(tab_array)

        self.text_editor.show()
        self.text_editor.grab_focus()

        self.editor_alignment = self.builder.get_object('editor_alignment')
        self.scrolled_window = self.builder.get_object('editor_scrolledwindow')
        self.scrolled_window.props.width_request = 600
        self.scrolled_window.add(self.text_editor)
        self.alignment_padding = 40
        self.editor_viewport = self.builder.get_object('editor_viewport')

        # some people seems to have performance problems with the overlay. 
        # Let them disable it

        if self.settings.get_value("gradient-overlay"):
            self.overlay = self.scrolled_window.connect_after("draw", self.draw_gradient)

        self.smooth_scroll_starttime = 0
        self.smooth_scroll_endtime = 0
        self.smooth_scroll_acttarget = 0
        self.smooth_scroll_data = {
            'target_pos': -1,
            'source_pos': -1,
            'duration': 0
        }
        self.smooth_scroll_tickid = -1

        self.text_buffer = self.text_editor.get_buffer()
        self.text_buffer.set_text('')

        # Init Window height for top/bottom padding
        self.window_height = self.get_size()[1]

        self.text_change_event = self.text_buffer.connect(
            'changed', self.text_changed)

        # Init file name with None
        self.set_filename()

        # self.style_provider = Gtk.CssProvider()
        # self.style_provider.load_from_path(helpers.get_media_path('arc_style.css'))

        # Gtk.StyleContext.add_provider_for_screen(
        #     Gdk.Screen.get_default(), self.style_provider,
        #     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        # )

        # Markup and Shortcuts for the TextBuffer
        self.markup_buffer = MarkupBuffer(
            self, self.text_buffer, base_leftmargin)
        self.markup_buffer.markup_buffer()

        # Setup dark mode if so
        self.toggle_dark_mode(self.settings.get_value("dark-mode"))

        # Scrolling -> Dark or not?
        self.textchange = False
        self.scroll_count = 0
        self.timestamp_last_mouse_motion = 0
        self.text_buffer.connect_after('mark-set', self.mark_set)

        # Drag and drop

        # self.TextEditor.drag_dest_unset()
        # self.TextEditor.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.target_list = Gtk.TargetList.new([])
        self.target_list.add_uri_targets(1)
        self.target_list.add_text_targets(2)

        self.text_editor.drag_dest_set_target_list(self.target_list)
        self.text_editor.connect_after(
            'drag-data-received', self.on_drag_data_received)

        def on_drop(_widget, *_args):
            print("drop")
        self.text_editor.connect('drag-drop', on_drop)

        self.text_buffer.connect('paste-done', self.paste_done)
        # self.connect('key-press-event', self.alt_mod)

        # Events for Typewriter mode

        # Setting up inline preview
        self.inline_preview = UberwriterInlinePreview(
            self.text_editor, self.text_buffer)

        # Vertical scrolling
        self.vadjustment = self.scrolled_window.get_vadjustment()
        self.vadjustment.connect('value-changed', self.scrolled)

        # Setting up spellcheck
        self.auto_correct = None
        try:
            self.spell_checker = SpellChecker(
                self.text_editor, locale.getdefaultlocale()[0],
                collapse=False)
            if self.auto_correct:
                self.auto_correct.set_language(self.spell_checker.language)
                self.spell_checker.connect_language_change( #pylint: disable=no-member
                    self.auto_correct.set_language)

            self.spellcheck = True
        except:
            self.spell_checker = None
            self.spellcheck = False

        if self.spellcheck:
            self.spell_checker.append_filter('[#*]+', SpellChecker.FILTER_WORD)

        self.did_change = False

        ###
        #   Sidebar initialization test
        ###
        self.paned_window = self.builder.get_object("main_pained")
        self.sidebar_box = self.builder.get_object("sidebar_box")
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

    __gsignals__ = {
        'save-file': (GObject.SIGNAL_ACTION, None, ()),
        'open-file': (GObject.SIGNAL_ACTION, None, ()),
        'save-file-as': (GObject.SIGNAL_ACTION, None, ()),
        'new-file': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-bibtex': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-preview': (GObject.SIGNAL_ACTION, None, ()),
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

    def paste_done(self, *_):
        self.markup_buffer.markup_buffer(0)

    def init_typewriter(self):
        """put the cursor at the center of the screen by setting top and
        bottom margins to height/2
        """

        editor_height = self.text_editor.get_allocation().height
        self.text_editor.props.top_margin = editor_height / 2
        self.text_editor.props.bottom_margin = editor_height / 2

    def remove_typewriter(self):
        """set margins to default values
        """

        self.text_editor.props.top_margin = 80
        self.text_editor.props.bottom_margin = 16
        self.text_change_event = self.text_buffer.connect(
            'changed', self.text_changed)

    def get_text(self):
        """get text from self.text_buffer
        """

        start_iter = self.text_buffer.get_start_iter()
        end_iter = self.text_buffer.get_end_iter()
        return self.text_buffer.get_text(start_iter, end_iter, False)

    def update_line_and_char_count(self):
        """it... it updates line and characters count
        """

        if self.status_bar_visible is False:
            return
        self.char_count.set_text(str(self.text_buffer.get_char_count()))
        text = self.get_text()
        words = re.split(self.WORDCOUNT, text)
        length = len(words)
        # Last word a "space"
        if not words[-1]:
            length = length - 1
        # First word a "space" (happens in focus mode...)
        if not words[0]:
            length = length - 1
        if length == -1:
            length = 0
        self.word_count.set_text(str(length))

    def mark_set(self, _buffer, _location, mark, _data=None):
        if mark.get_name() in ['insert', 'gtk_drag_target']:
            self.check_scroll(mark)
        return True

    def text_changed(self, *_args):
        """called when the text changes, sets the self.did_change to true and
           updates the title and the counters to reflect that
        """

        if self.did_change is False:
            self.did_change = True
            title = self.get_title()
            self.set_headerbar_title("* " + title)

        self.markup_buffer.markup_buffer(1)
        self.textchange = True

        self.buffer_modified_for_status_bar = True
        self.update_line_and_char_count()
        self.check_scroll(self.text_buffer.get_insert())

    def toggle_fullscreen(self, state):
        """Puts the application in fullscreen mode and show/hides
        the poller for motion in the top border

        Arguments:
            state {almost bool} -- The desired fullscreen state of the window
        """

        if state.get_boolean():
            self.fullscreen()
            self.fs_headerbar.events.show()

        else:
            self.unfullscreen()
            self.fs_headerbar.events.hide()

        self.text_editor.grab_focus()

    def set_focusmode(self, state):
        """toggle focusmode
        """

        if state.get_boolean():
            self.init_typewriter()
            self.markup_buffer.focusmode_highlight()
            self.focusmode = True
            self.text_editor.grab_focus()
            self.check_scroll(self.text_buffer.get_insert())
            if self.spellcheck:
                self.spell_checker._misspelled.set_property('underline', 0)
            self.click_event = self.text_editor.connect("button-release-event",
                                                        self.on_focusmode_click)
        else:
            self.remove_typewriter()
            self.focusmode = False
            self.text_buffer.remove_tag(self.markup_buffer.grayfont,
                                        self.text_buffer.get_start_iter(),
                                        self.text_buffer.get_end_iter())
            self.text_buffer.remove_tag(self.markup_buffer.blackfont,
                                        self.text_buffer.get_start_iter(),
                                        self.text_buffer.get_end_iter())

            self.markup_buffer.markup_buffer(1)
            self.text_editor.grab_focus()
            self.update_line_and_char_count()
            self.check_scroll()
            if self.spellcheck:
                self.spell_checker._misspelled.set_property('underline', 4)
            _click_event = self.text_editor.disconnect(self.click_event)

    def on_focusmode_click(self, *_args):
        """call MarkupBuffer to mark as bold the line where the cursor is
        """

        self.markup_buffer.markup_buffer(1)

    def scroll_smoothly(self, widget, frame_clock, _data=None):
        if self.smooth_scroll_data['target_pos'] == -1:
            return True

        def ease_out_cubic(time):
            time = time - 1
            return pow(time, 3) + 1

        now = frame_clock.get_frame_time()
        if self.smooth_scroll_acttarget != self.smooth_scroll_data['target_pos']:
            self.smooth_scroll_starttime = now
            self.smooth_scroll_endtime = now + \
                self.smooth_scroll_data['duration'] * 100
            self.smooth_scroll_acttarget = self.smooth_scroll_data['target_pos']

        if now < self.smooth_scroll_endtime:
            time = float(now - self.smooth_scroll_starttime) / float(
                self.smooth_scroll_endtime - self.smooth_scroll_starttime)
        else:
            time = 1
            pos = self.smooth_scroll_data['source_pos'] \
                + (time * (self.smooth_scroll_data['target_pos']
                           - self.smooth_scroll_data['source_pos']))
            widget.get_vadjustment().props.value = pos
            self.smooth_scroll_data['target_pos'] = -1
            return True

        time = ease_out_cubic(time)
        pos = self.smooth_scroll_data['source_pos'] \
            + (time * (self.smooth_scroll_data['target_pos']
                       - self.smooth_scroll_data['source_pos']))
        widget.get_vadjustment().props.value = pos
        return True  # continue ticking

    def check_scroll(self, mark=None):
        gradient_offset = 80
        buf = self.text_editor.get_buffer()
        if mark:
            ins_it = buf.get_iter_at_mark(mark)
        else:
            ins_it = buf.get_iter_at_mark(buf.get_insert())
        loc_rect = self.text_editor.get_iter_location(ins_it)

        # alignment offset added from top
        pos_y = loc_rect.y + loc_rect.height + self.text_editor.props.top_margin # pylint: disable=no-member

        ha = self.scrolled_window.get_vadjustment()
        if ha.props.page_size < gradient_offset:
            return
        pos = pos_y - ha.props.value
        # print("pos: %i, pos_y %i, page_sz: %i, val: %i" % (pos, pos_y, ha.props.page_size
        #                                                    - gradient_offset, ha.props.value))
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
            self.smooth_scroll_tickid = self.scrolled_window.add_tick_callback(
                self.scroll_smoothly)

    def window_resize(self, widget, _data=None):
        """set paddings dependant of the window size
        """

        # To calc padding top / bottom
        self.window_height = widget.get_allocation().height
        w_width = widget.get_allocation().width
        # Calculate left / right margin
        width_request = 600
        if w_width < 900:
            self.markup_buffer.set_multiplier(8)
            self.current_font_size = 12
            self.alignment_padding = 30
            lm = 7 * 8
            self.get_style_context().remove_class("medium")
            self.get_style_context().remove_class("large")
            self.get_style_context().add_class("small")

        elif w_width < 1400:
            self.markup_buffer.set_multiplier(10)
            width_request = 800
            self.current_font_size = 15
            self.alignment_padding = 40
            lm = 7 * 10
            self.get_style_context().remove_class("small")
            self.get_style_context().remove_class("large")
            self.get_style_context().add_class("medium")

        else:
            self.markup_buffer.set_multiplier(13)
            self.current_font_size = 17
            width_request = 1000
            self.alignment_padding = 60
            lm = 7 * 13
            self.get_style_context().remove_class("medium")
            self.get_style_context().remove_class("small")
            self.get_style_context().add_class("large")

        self.editor_alignment.props.margin_bottom = 0
        self.editor_alignment.props.margin_top = 0
        self.text_editor.set_left_margin(lm)
        self.text_editor.set_right_margin(lm)

        self.markup_buffer.recalculate(lm)

        if self.focusmode:
            self.remove_typewriter()
            self.init_typewriter()

        if self.text_editor.props.width_request != width_request: # pylint: disable=no-member
            self.text_editor.props.width_request = width_request
            self.scrolled_window.props.width_request = width_request
            alloc = self.text_editor.get_allocation()
            alloc.width = width_request
            self.text_editor.size_allocate(alloc)

    def style_changed(self, _widget, _data=None):
        pgc = self.text_editor.get_pango_context()
        mets = pgc.get_metrics()
        self.markup_buffer.set_multiplier(
            Pango.units_to_double(mets.get_approximate_char_width()) + 1)

    # TODO: refactorizable
    def save_document(self, _widget=None, _data=None):
        """provide to the user a filechooser and save the document
           where he wants. Call set_headbar_title after that
        """

        if self.filename:
            LOGGER.info("saving")
            filename = self.filename
            file_to_save = codecs.open(filename, encoding="utf-8", mode='w')
            file_to_save.write(self.get_text())
            file_to_save.close()
            if self.did_change:
                self.did_change = False
                title = self.get_title()
                self.set_headerbar_title(title[2:])
            return Gtk.ResponseType.OK

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

            file_to_save = codecs.open(filename, encoding="utf-8", mode='w')
            file_to_save.write(self.get_text())
            file_to_save.close()

            self.set_filename(filename)
            self.set_headerbar_title(
                os.path.basename(filename) + self.title_end)

            self.did_change = False
            filechooser.destroy()
            return response

        filechooser.destroy()
        return Gtk.ResponseType.CANCEL

    def save_document_as(self, _widget=None, _data=None):
        """provide to the user a filechooser and save the document
           where he wants. Call set_headbar_title after that
        """
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

            file_to_save = codecs.open(filename, encoding="utf-8", mode='w')
            file_to_save.write(self.get_text())
            file_to_save.close()

            self.set_filename(filename)
            self.set_headerbar_title(
                os.path.basename(filename) + self.title_end)

            try:
                self.recent_manager.add_item(filename)
            except:
                pass

            filechooser.destroy()
            self.did_change = False

        else:
            filechooser.destroy()
            return Gtk.ResponseType.CANCEL

    def copy_html_to_clipboard(self, _widget=None, _date=None):
        """Copies only html without headers etc. to Clipboard
        """

        args = ['pandoc', '--from=markdown', '--to=html5']
        proc = subprocess.Popen(args, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)

        text = bytes(self.get_text(), "utf-8")
        output = proc.communicate(text)[0]

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(output.decode("utf-8"), -1)
        clipboard.store()

    def open_document(self, _widget=None):
        """open the desired file
        """

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
        """Show dialog to prevent loss of unsaved changes
        """

        if self.did_change and self.get_text():
            dialog = Gtk.MessageDialog(self,
                                       Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.NONE,
                                       _("You have not saved your changes.")
                                       )
            dialog.add_button(_("Close without Saving"), Gtk.ResponseType.NO)
            dialog.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("Save now"), Gtk.ResponseType.YES)
            # dialog.set_default_size(200, 60)
            dialog.set_default_response(Gtk.ResponseType.YES)
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                if self.save_document() == Gtk.ResponseType.CANCEL:
                    dialog.destroy()
                    return self.check_change()

                dialog.destroy()
                return response
            if response == Gtk.ResponseType.NO:
                dialog.destroy()
                return response

            dialog.destroy()
            return Gtk.ResponseType.CANCEL

    def new_document(self, _widget=None):
        """create new document
        """

        if self.check_change() == Gtk.ResponseType.CANCEL:
            return
        self.text_buffer.set_text('')
        self.text_editor.undos = []
        self.text_editor.redos = []

        self.did_change = False
        self.set_filename()
        self.set_headerbar_title(_("New File") + self.title_end)

    def menu_toggle_sidebar(self, _widget=None):
        """WIP
        """
        self.sidebar.toggle_sidebar()

    def toggle_spellcheck(self, status):
        """Enable/disable the autospellchecking

        Arguments:
            status {gtk bool} -- Desired status of the spellchecking
        """

        if self.spellcheck:
            if status.get_boolean():
                self.spell_checker.enable()
            else:
                self.spell_checker.disable()

        elif status.get_boolean():
            self.spell_checker = SpellChecker(
                self.text_editor, self, locale.getdefaultlocale()[0],
                collapse=False)
            if self.auto_correct:
                self.auto_correct.set_language(self.spell_checker.language)
                self.spell_checker.connect_language_change( # pylint: disable=no-member
                    self.auto_correct.set_language)
            try:
                self.spellcheck = True
            except:
                self.spell_checker = None
                self.spellcheck = False
                dialog = Gtk.MessageDialog(self,
                                           Gtk.DialogFlags.MODAL \
                                           | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                           Gtk.MessageType.INFO,
                                           Gtk.ButtonsType.NONE,
                                           _("You can not enable the Spell Checker.")
                                           )
                dialog.format_secondary_text(
                    _("Please install 'hunspell' or 'aspell' dictionarys"
                      + " for your language from the software center."))
                _response = dialog.run()
                return
        return

    def on_drag_data_received(self, _widget, drag_context, _x, _y,
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
                    limit_left = 2
                    limit_right = 23
                else:
                    text = "[Insert link title here](%s)" % uri
                    limit_left = 1
                    limit_right = 22
                self.text_buffer.place_cursor(self.text_buffer.get_iter_at_mark(
                    self.text_buffer.get_mark('gtk_drag_target')))
                self.text_buffer.insert_at_cursor(text)
                insert_mark = self.text_buffer.get_insert()
                selection_bound = self.text_buffer.get_selection_bound()
                cursor_iter = self.text_buffer.get_iter_at_mark(insert_mark)
                cursor_iter.backward_chars(len(text) - limit_left)
                self.text_buffer.move_mark(insert_mark, cursor_iter)
                cursor_iter.forward_chars(limit_right)
                self.text_buffer.move_mark(selection_bound, cursor_iter)

        elif info == 2:
            # Text target
            self.text_buffer.place_cursor(self.text_buffer.get_iter_at_mark(
                self.text_buffer.get_mark('gtk_drag_target')))
            self.text_buffer.insert_at_cursor(data.get_text())
        Gtk.drag_finish(drag_context, True, True, time)
        self.present()
        return False

    def toggle_preview(self, state):
        """Toggle the preview mode

        Arguments:
            state {gtk bool} -- Desired state of the preview mode (enabled/disabled)
        """


        if state.get_boolean():

            # Insert a tag with ID to scroll to
            # self.TextBuffer.insert_at_cursor('<span id="scroll_mark"></span>')
            # TODO
            # Find a way to find the next header, scroll to the next header.
            # TODO: provide a local version of mathjax

            # We need to convert relative routes to absolute ones
            # For that first we need to know if the file is saved:
            if self.filename:
                base_path = os.path.dirname(self.filename)
            else:
                base_path = ''
            os.environ['PANDOC_PREFIX'] = base_path + '/'

            # Set the styles according the color theme
            if self.settings.get_value("dark-mode"):
                stylesheet = helpers.get_media_path('github-md-dark.css')
            else:
                stylesheet = helpers.get_media_path('github-md.css')

            args = ['pandoc',
                    '-s',
                    '--from=markdown',
                    '--to=html5',
                    '--mathjax',
                    '--css=' + stylesheet,
                    '--lua-filter=' +
                    helpers.get_script_path('relative_to_absolute.lua'),
                    '--lua-filter=' + helpers.get_script_path('task-list.lua')]

            proc = subprocess.Popen(
                args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

            text = bytes(self.get_text(), "utf-8")
            output = proc.communicate(text)[0]

            # Load in Webview and scroll to #ID
            self.preview_webview = WebKit.WebView()
            webview_settings = self.preview_webview.get_settings()
            webview_settings.set_allow_universal_access_from_file_urls(
                True)
            self.preview_webview.load_html(output.decode("utf-8"), 'file://localhost/')

            # Delete the cursor-scroll mark again
            # cursor_iter = self.TextBuffer.get_iter_at_mark(self.TextBuffer.get_insert())
            # begin_del = cursor_iter.copy()
            # begin_del.backward_chars(30)
            # self.TextBuffer.delete(begin_del, cursor_iter)

            self.scrolled_window.remove(self.text_editor)
            self.scrolled_window.add(self.preview_webview)
            self.preview_webview.show()

            # This saying that all links will be opened in default browser, \
            # but local files are opened in appropriate apps:
            self.preview_webview.connect("decide-policy", self.on_click_link)
        else:
            self.scrolled_window.remove(self.preview_webview)
            self.preview_webview.destroy()
            self.scrolled_window.add(self.text_editor)
            self.text_editor.show()

        self.queue_draw()
        return True

    def toggle_dark_mode(self, state):
        """Toggle the dark mode, both for the window and for the CSD

        Arguments:
            state {gtk bool} -- Desired state of the dark mode (enabled/disabled)
        """

        # Save state for saving settings later

        if state:
            # Dark Mode is on
            self.get_style_context().add_class("dark_mode")
            self.headerbar.hb_container.get_style_context().add_class("dark_mode")
            self.markup_buffer.dark_mode(True)
        else:
            # Dark mode off
            self.get_style_context().remove_class("dark_mode")
            self.headerbar.hb_container.get_style_context().remove_class("dark_mode")
            self.markup_buffer.dark_mode(False)

        # Redraw contents of window (self)
        self.queue_draw()

    def load_file(self, filename=None):
        """Open File from command line or open / open recent etc."""
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        if filename:
            if filename.startswith('file://'):
                filename = filename[7:]
            filename = urllib.parse.unquote_plus(filename)
            try:
                if not os.path.exists(filename):
                    self.text_buffer.set_text("")
                else:
                    current_file = codecs.open(filename, encoding="utf-8", mode='r')
                    self.text_buffer.set_text(current_file.read())
                    current_file.close()
                    self.markup_buffer.markup_buffer(0)

                self.set_headerbar_title(
                    os.path.basename(filename) + self.title_end)
                self.text_editor.undo_stack = []
                self.text_editor.redo_stack = []
                self.set_filename(filename)

            except Exception:
                LOGGER.warning("Error Reading File: %r" % Exception)
            self.did_change = False
        else:
            LOGGER.warning("No File arg")

    def open_uberwriter_markdown(self, _widget=None, _data=None):
        """open a markdown mini tutorial
        """
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        self.load_file(helpers.get_media_file('uberwriter_markdown.md'))

    def open_search_and_replace(self):
        """toggle the search box
        """

        self.searchreplace.toggle_search()

    def open_advanced_export(self, _widget=None, _data=None):
        """open the export and advanced export dialog
        """

        self.export = Export(self.filename)
        self.export.dialog.set_transient_for(self)

        response = self.export.dialog.run()
        if response == 1:
            self.export.export(bytes(self.get_text(), "utf-8"))

        self.export.dialog.destroy()

    def open_recent(self, _widget, data=None):
        """open the given recent document
        """
        print("open")

        if data:
            if self.check_change() == Gtk.ResponseType.CANCEL:
                return
            self.load_file(data)

    def poll_for_motion(self):
        """check if the user has moved the cursor to show the headerbar

        Returns:
            True -- Gtk things
        """

        if (self.was_motion is False
                and self.status_bar_visible
                and self.buffer_modified_for_status_bar
                and self.text_editor.props.has_focus): #pylint: disable=no-member
            # self.status_bar.set_state_flags(Gtk.StateFlags.INSENSITIVE, True)
            self.statusbar_revealer.set_reveal_child(False)
            self.headerbar.hb_revealer.set_reveal_child(False)
            self.status_bar_visible = False
            self.buffer_modified_for_status_bar = False

        self.was_motion = False
        return True

    def on_motion_notify(self, _widget, event, _data=None):
        """check the motion of the mouse to fade in the headerbar
        """
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
            if self.status_bar_visible is False:
                self.statusbar_revealer.set_reveal_child(True)
                self.headerbar.hb_revealer.set_reveal_child(True)
                self.headerbar.hb.props.opacity = 1
                self.status_bar_visible = True
                self.buffer_modified_for_status_bar = False
                self.update_line_and_char_count()
                # self.status_bar.set_state_flags(Gtk.StateFlags.NORMAL, True)
            self.was_motion = True

    def focus_out(self, _widget, _data=None):
        """events called when the window losses focus
        """
        if self.status_bar_visible is False:
            self.statusbar_revealer.set_reveal_child(True)
            self.headerbar.hb_revealer.set_reveal_child(True)
            self.headerbar.hb.props.opacity = 1
            self.status_bar_visible = True
            self.buffer_modified_for_status_bar = False
            self.update_line_and_char_count()

    def draw_gradient(self, _widget, cr):
        """draw fading gradient over the top and the bottom of the
           TextWindow
        """
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.ACTIVE)

        lg_top = cairo.LinearGradient(0, 0, 0, 35) #pylint: disable=no-member
        lg_top.add_color_stop_rgba(
            0, bg_color.red, bg_color.green, bg_color.blue, 1)
        lg_top.add_color_stop_rgba(
            1, bg_color.red, bg_color.green, bg_color.blue, 0)

        width = self.scrolled_window.get_allocation().width
        height = self.scrolled_window.get_allocation().height

        cr.rectangle(0, 0, width, 35)
        cr.set_source(lg_top)
        cr.fill()
        cr.rectangle(0, height - 35, width, height)

        lg_btm = cairo.LinearGradient(0, height - 35, 0, height) # pylint: disable=no-member
        lg_btm.add_color_stop_rgba(
            1, bg_color.red, bg_color.green, bg_color.blue, 1)
        lg_btm.add_color_stop_rgba(
            0, bg_color.red, bg_color.green, bg_color.blue, 0)

        cr.set_source(lg_btm)
        cr.fill()

    def use_experimental_features(self, _val):
        """use experimental features
        """
        pass
        # try:
        #     self.auto_correct = UberwriterAutoCorrect(
        #         self.text_editor, self.text_buffer)
        # except:
        #     LOGGER.debug("Couldn't install autocorrect.")

        # self.plugins = [BibTex(self)]

    # def alt_mod(self, _widget, event, _data=None):
    #     # TODO: Click and open when alt is pressed
    #     if event.state & Gdk.ModifierType.MOD2_MASK:
    #         LOGGER.info("Alt pressed")
    #     return

    def on_delete_called(self, _widget, _data=None):
        """Called when the TexteditorWindow is closed.
        """
        LOGGER.info('delete called')
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return True
        return False

    def on_mnu_close_activate(self, _widget, _data=None):
        """Signal handler for closing the UberwriterWindow.
           Overriden from parent Window Class
        """
        if self.on_delete_called(self):  # Really destroy?
            return
        self.destroy()
        return

    def on_destroy(self, _widget, _data=None):
        """Called when the TexteditorWindow is closed.
        """
        # Clean up code for saving application state should be added here.
        Gtk.main_quit()

    def set_headerbar_title(self, title):
        """set the desired headerbar title
        """
        self.headerbar.hb.props.title = title
        self.fs_headerbar.hb.props.title = title
        self.set_title(title)

    def set_filename(self, filename=None):
        """set filename
        """
        if filename:
            self.filename = filename
            base_path = os.path.dirname(self.filename)
        else:
            self.filename = None
            base_path = "/"
        self.settings.set_value("open-file-path", GLib.Variant("s", base_path))

    def on_click_link(self, web_view, decision, _decision_type):
        """provide ability for self.webview to open links in default browser
        """
        if web_view.get_uri().startswith(("http://", "https://", "www.")):
            webbrowser.open(web_view.get_uri())
            decision.ignore()
            return True  # Don't let the event "bubble up"
