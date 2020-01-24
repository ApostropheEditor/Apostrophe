# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
# Copyright (C) 2019, Wolf Vollprecht <w.vollprecht@gmail.com>
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

import io
import locale
import logging
import os
import urllib
from gettext import gettext as _

import gi

from uberwriter.export_dialog import Export
from uberwriter.preview_handler import PreviewHandler
from uberwriter.stats_handler import StatsHandler
from uberwriter.styled_window import StyledWindow
from uberwriter.text_view import TextView

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib, Gio

import cairo

from uberwriter import helpers
from uberwriter.theme import Theme

from uberwriter.sidebar import Sidebar
from uberwriter.search_and_replace import SearchAndReplace
from uberwriter.settings import Settings

from . import headerbars

# Some Globals
# TODO move them somewhere for better
# accesibility from other files

LOGGER = logging.getLogger('uberwriter')

CONFIG_PATH = os.path.expanduser("~/.config/uberwriter/")


class MainWindow(StyledWindow):
    __gsignals__ = {
        'save-file': (GObject.SIGNAL_ACTION, None, ()),
        'open-file': (GObject.SIGNAL_ACTION, None, ()),
        'save-file-as': (GObject.SIGNAL_ACTION, None, ()),
        'new-file': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-bibtex': (GObject.SIGNAL_ACTION, None, ()),
        'toggle-preview': (GObject.SIGNAL_ACTION, None, ()),
        'close-window': (GObject.SIGNAL_ACTION, None, ())
    }

    def __init__(self, app):
        """Set up the main window"""

        super().__init__(application=Gio.Application.get_default(), title="Uberwriter")

        self.get_style_context().add_class('uberwriter-window')

        # Set UI
        builder = Gtk.Builder()
        builder.add_from_resource(
            "/de/wolfvollprecht/UberWriter/ui/Window.ui")
        root = builder.get_object("FullscreenOverlay")
        self.connect("delete-event", self.on_delete_called)
        self.add(root)

        self.set_default_size(1000, 600)

        # Preferences
        self.settings = Settings.new()

        # Headerbars
        self.headerbar = headerbars.MainHeaderbar(app)
        self.set_titlebar(self.headerbar.hb_container)
        self.fs_headerbar = headerbars.FullscreenHeaderbar(builder, app)

        self.title_end = "  –  UberWriter"
        self.set_headerbar_title("New File" + self.title_end)

        self.timestamp_last_mouse_motion = 0
        if self.settings.get_value("poll-motion"):
            self.connect("motion-notify-event", self.on_motion_notify)
            GObject.timeout_add(3000, self.poll_for_motion)

        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)

        self.scrolled_window = builder.get_object('editor_scrolledwindow')

        # Setup text editor
        self.text_view = TextView(self.settings.get_int("characters-per-line"))
        self.text_view.connect('focus-out-event', self.focus_out)
        self.text_view.get_buffer().connect('changed', self.on_text_changed)
        self.text_view.show()
        self.text_view.grab_focus()
        self.scrolled_window.add(self.text_view)

        # Setup stats counter
        self.stats_revealer = builder.get_object('editor_stats_revealer')
        self.stats_button = builder.get_object('editor_stats_button')
        self.stats_handler = StatsHandler(self.stats_button, self.text_view)

        # Setup preview
        content = builder.get_object('content')
        editor = builder.get_object('editor')
        self.preview_handler = PreviewHandler(self, content, editor, self.text_view)

        # Setup header/stats bar hide after 3 seconds
        self.top_bottom_bars_visible = True
        self.was_motion = True
        self.buffer_modified_for_status_bar = False

        # some people seems to have performance problems with the overlay.
        # Let them disable it
        self.overlay_id = None
        self.toggle_gradient_overlay(self.settings.get_value("gradient-overlay"))

        # Init file name with None
        self.set_filename()

        # Setting up spellcheck
        self.auto_correct = None
        self.toggle_spellcheck(self.settings.get_value("spellcheck"))
        self.did_change = False

        ###
        #   Sidebar initialization test
        ###
        self.paned_window = builder.get_object("main_paned")
        self.sidebar_box = builder.get_object("sidebar_box")
        self.sidebar = Sidebar(self)
        self.sidebar_box.hide()

        ###
        #   Search and replace initialization
        #   Same interface as Sidebar ;)
        ###
        self.searchreplace = SearchAndReplace(self, self.text_view, builder)

    def on_text_changed(self, *_args):
        """called when the text changes, sets the self.did_change to true and
           updates the title and the counters to reflect that
        """

        if self.did_change is False:
            self.did_change = True
            title = self.get_title()
            self.set_headerbar_title("* " + title)

        self.buffer_modified_for_status_bar = True

    def set_fullscreen(self, state):
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
        self.text_view.grab_focus()

    def set_focus_mode(self, state):
        """toggle focusmode
        """

        self.text_view.set_focus_mode(state.get_boolean())
        self.text_view.grab_focus()

    def set_hemingway_mode(self, state):
        """toggle hemingwaymode
        """

        self.text_view.set_hemingway_mode(state.get_boolean())
        self.text_view.grab_focus()

    def toggle_preview(self, state):
        """Toggle the preview mode

        Arguments:
            state {gtk bool} -- Desired state of the preview mode (enabled/disabled)
        """

        if state.get_boolean():
            self.text_view.grab_focus()
            self.preview_handler.show()
        else:
            self.preview_handler.hide()
            self.text_view.grab_focus()

        return True

    # TODO: refactorizable
    def save_document(self, _widget=None, _data=None):
        """provide to the user a filechooser and save the document
           where he wants. Call set_headbar_title after that
        """

        if self.filename:
            LOGGER.info("saving")
            filename = self.filename
            file_to_save = io.open(filename, encoding="utf-8", mode='w')
            file_to_save.write(self.text_view.get_text())
            file_to_save.close()
            if self.did_change:
                self.did_change = False
                title = self.get_title()
                self.set_headerbar_title(title[2:])
            return Gtk.ResponseType.OK

        filefilter = Gtk.FileFilter.new()
        filefilter.add_mime_type('text/x-markdown')
        filefilter.add_mime_type('text/plain')
        filefilter.set_name('Markdown (.md)')
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

            file_to_save = io.open(filename, encoding="utf-8", mode='w')
            file_to_save.write(self.text_view.get_text())
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

            file_to_save = io.open(filename, encoding="utf-8", mode='w')
            file_to_save.write(self.text_view.get_text())
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

        output = helpers.pandoc_convert(self.text_view.get_text())
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(output, -1)
        clipboard.store()

    def open_document(self, _widget=None):
        """open the desired file
        """

        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        markdown_filter = Gtk.FileFilter.new()
        markdown_filter.add_mime_type('text/markdown')
        markdown_filter.add_mime_type('text/x-markdown')
        markdown_filter.set_name(_('Markdown Files'))

        plaintext_filter = Gtk.FileFilter.new()
        plaintext_filter.add_mime_type('text/plain')
        plaintext_filter.set_name(_('Plain Text Files'))

        filechooser = Gtk.FileChooserDialog(
            _("Open a .md file"),
            self,
            Gtk.FileChooserAction.OPEN,
            ("_Cancel", Gtk.ResponseType.CANCEL,
             "_Open", Gtk.ResponseType.OK)
        )
        filechooser.add_filter(markdown_filter)
        filechooser.add_filter(plaintext_filter)
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

        if self.did_change and self.text_view.get_text():
            dialog = Gtk.MessageDialog(self,
                                       Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.NONE,
                                       _("You have not saved your changes.")
                                       )
            dialog.add_button(_("Close without saving"), Gtk.ResponseType.NO)
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
        self.text_view.clear()

        self.did_change = False
        self.set_filename()
        self.set_headerbar_title(_("New File") + self.title_end)

    def update_default_stat(self):
        self.stats_handler.update_default_stat()

    def update_preview_mode(self):
        self.preview_handler.update_preview_mode()

    def menu_toggle_sidebar(self, _widget=None):
        """WIP
        """
        self.sidebar.toggle_sidebar()

    def toggle_spellcheck(self, state):
        """Enable/disable the autospellchecking

        Arguments:
            status {gtk bool} -- Desired status of the spellchecking
        """

        self.text_view.set_spellcheck(state.get_boolean())

    def toggle_gradient_overlay(self, state):
        """Toggle the gradient overlay

        Arguments:
            state {gtk bool} -- Desired state of the gradient overlay (enabled/disabled)
        """

        if state.get_boolean():
            self.overlay_id = self.scrolled_window.connect_after("draw", self.draw_gradient)
        elif self.overlay_id:
            self.scrolled_window.disconnect(self.overlay_id)

    def reload_preview(self, reshow=False):
        self.preview_handler.reload(reshow=reshow)

    def load_file(self, filename=None):
        """Open File from command line or open / open recent etc."""
        LOGGER.info("trying to open " + filename)
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        if filename:
            print(urllib.parse.unquote(filename))
            if filename.startswith('file://'):
                filename = urllib.parse.unquote(filename)[7:]
            self.text_view.clear()
            try:
                if os.path.exists(filename):
                    with io.open(filename, encoding="utf-8", mode='r') as current_file:
                        self.text_view.set_text(current_file.read())
                else:
                    dialog = Gtk.MessageDialog(self,
                                       Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.CLOSE,
                                       _("The file you tried to open doesn't exist.\
                                            \nA new file will be created in its place when you save the current one.")
                                       )
                    dialog.run()
                    dialog.destroy()

                self.set_headerbar_title(os.path.basename(filename) + self.title_end)
                self.set_filename(filename)

            except Exception as e:
                LOGGER.warning(_("Error Reading File: %r") % e)
                dialog = Gtk.MessageDialog(self,
                                    Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                    Gtk.MessageType.WARNING,
                                    Gtk.ButtonsType.CLOSE,
                                    _("Error reading file:\
                                         \n%r" %e)
                                    )
                dialog.run()
                dialog.destroy()
            self.did_change = False
        else:
            LOGGER.warning("No File arg")

    def open_uberwriter_markdown(self, _widget=None, _data=None):
        """open a markdown mini tutorial
        """
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        self.load_file(helpers.get_media_file('uberwriter_markdown.md'))

    def open_search(self, replace=False):
        """toggle the search box
        """

        self.searchreplace.toggle_search(replace=replace)

    def open_advanced_export(self, _widget=None, _data=None):
        """open the export and advanced export dialog
        """

        self.export = Export(self.filename)
        self.export.dialog.set_transient_for(self)

        response = self.export.dialog.run()
        if response == 1:
            try:
                self.export.export(bytes(self.text_view.get_text(), "utf-8"))
            except Exception as e:
                dialog = Gtk.MessageDialog(self,
                                       Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CLOSE,
                                       _("An error happened while trying to export:\n\n{err_msg}")
                                           .format(err_msg= str(e).encode().decode("unicode-escape"))
                                       )
                dialog.run()
                dialog.destroy()

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

        if (not self.was_motion
                and self.buffer_modified_for_status_bar
                and self.text_view.props.has_focus):
            self.reveal_top_bottom_bars(False)

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
            self.reveal_top_bottom_bars(True)
            self.was_motion = True

    def focus_out(self, _widget, _data=None):
        """events called when the window losses focus
        """
        self.reveal_top_bottom_bars(True)

    def reveal_top_bottom_bars(self, reveal):
        if self.top_bottom_bars_visible != reveal:
            self.headerbar.hb_revealer.set_reveal_child(reveal)
            self.stats_revealer.set_reveal_child(reveal)
            for revealer in self.preview_handler.get_top_bottom_bar_revealers():
                revealer.set_reveal_child(reveal)
            self.top_bottom_bars_visible = reveal
            self.buffer_modified_for_status_bar = reveal

    def draw_gradient(self, _widget, cr):
        """draw fading gradient over the top and the bottom of the
           TextWindow
        """
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.ACTIVE)

        lg_top = cairo.LinearGradient(0, 0, 0, 32)  # pylint: disable=no-member
        lg_top.add_color_stop_rgba(
            0, bg_color.red, bg_color.green, bg_color.blue, 1)
        lg_top.add_color_stop_rgba(
            1, bg_color.red, bg_color.green, bg_color.blue, 0)

        width = self.scrolled_window.get_allocation().width
        height = self.scrolled_window.get_allocation().height

        cr.rectangle(0, 0, width, 32)
        cr.set_source(lg_top)
        cr.fill()
        cr.rectangle(0, height - 32, width, height)

        lg_btm = cairo.LinearGradient(0, height - 32, 0, height)  # pylint: disable=no-member
        lg_btm.add_color_stop_rgba(
            1, bg_color.red, bg_color.green, bg_color.blue, 1)
        lg_btm.add_color_stop_rgba(
            0, bg_color.red, bg_color.green, bg_color.blue, 0)

        cr.set_source(lg_btm)
        cr.fill()

    def on_delete_called(self, _widget, _data=None):
        """Called when the TexteditorWindow is closed.
        """
        LOGGER.info('delete called')
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return True
        return False

    def on_mnu_close_activate(self, _widget, _data=None):
        """Signal handler for closing the Window.
           Overriden from parent Window Class
        """
        if self.on_delete_called(self):  # Really destroy?
            return
        self.destroy()
        return

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
        self.settings.set_string("open-file-path", base_path)
