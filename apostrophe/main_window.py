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

import logging
import os
from gettext import gettext as _

from dataclasses import dataclass
import chardet

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib, Gio

from apostrophe.export_dialog import ExportDialog, AdvancedExportDialog
from apostrophe.preview_handler import PreviewHandler
from apostrophe.stats_handler import StatsHandler
from apostrophe.styled_window import StyledWindow
from apostrophe.text_view import TextView
from apostrophe.search_and_replace import SearchAndReplace
from apostrophe.settings import Settings
from apostrophe.tweener import Tweener
from apostrophe import helpers
# from apostrophe.sidebar import Sidebar

from . import headerbars

LOGGER = logging.getLogger('apostrophe')


class MainWindow(StyledWindow):

    def __init__(self, app):
        """Set up the main window"""

        super().__init__(application=Gio.Application.get_default(),
                         title="Apostrophe")

        self.get_style_context().add_class('apostrophe-window')

        # Set UI
        builder = Gtk.Builder()
        builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/ui/Window.ui")
        root = builder.get_object("AppOverlay")
        self.connect("delete-event", self.on_delete_called)
        self.add(root)

        self.set_default_size(1000, 600)

        # Preferences
        self.settings = Settings.new()

        # Create new, empty file
        # TODO: load last opened file?

        self.current = File()

        # Headerbars
        self.last_height = 0
        self.headerbar = headerbars.MainHeaderbar(app)
        self.headerbar.hb_revealer.connect(
            "size_allocate", self.header_size_allocate)
        self.set_titlebar(self.headerbar.hb_revealer)

        # remove .titlebar class from hb_revealer
        # to don't mess things up on Elementary OS
        self.headerbar.hb_revealer.get_style_context().remove_class("titlebar")

        self.fs_headerbar = headerbars.FullscreenHeaderbar(builder, app)

        # Bind properties between normal and fs headerbar
        self.headerbar.light_button.bind_property(
            "active", self.fs_headerbar.light_button, "active",
            GObject.BindingFlags.BIDIRECTIONAL
            | GObject.BindingFlags.SYNC_CREATE)

        self.headerbar.dark_button.bind_property(
            "active", self.fs_headerbar.dark_button, "active",
            GObject.BindingFlags.BIDIRECTIONAL |
            GObject.BindingFlags.SYNC_CREATE)

        # The dummy headerbar is a cosmetic hack to be able to
        # crossfade the hb on top of the window
        self.dm_headerbar = headerbars.DummyHeaderbar(app)
        root.add_overlay(self.dm_headerbar.hb_revealer)
        root.reorder_overlay(self.dm_headerbar.hb_revealer, 0)
        root.set_overlay_pass_through(self.dm_headerbar.hb_revealer, True)

        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)

        scrolled_window = builder.get_object('editor_scrolledwindow')

        # Setup text editor
        self.text_view = TextView(self.settings.get_int("characters-per-line"))
        self.text_view.set_top_margin(80)
        self.text_view.connect('focus-out-event', self.focus_out)
        self.text_view.get_buffer().connect('changed', self.on_text_changed)
        self.text_view.show()
        scrolled_window.add(self.text_view)
        self.text_view.grab_focus()

        # Setup save progressbar an its animator

        self.progressbar = builder.get_object("save_progressbar")
        self.progressbar_initiate_tw = Tweener(self.progressbar,
                                               self.progressbar.set_fraction,
                                               0, 0.125, 40)
        self.progressbar_finalize_tw = Tweener(self.progressbar,
                                               self.progressbar.set_fraction,
                                               0.125, 1, 400)
        self.progressbar_opacity_tw = Tweener(self.progressbar,
                                              self.progressbar.set_opacity,
                                              1, 0, 300, 200)

        # Setup stats counter
        self.stats_revealer = builder.get_object('editor_stats_revealer')
        self.stats_button = builder.get_object('editor_stats_button')
        self.stats_handler = StatsHandler(self.stats_button, self.text_view)

        # Setup preview
        content = builder.get_object('content')
        editor = builder.get_object('editor')
        self.preview_handler = PreviewHandler(self, content,
                                              editor, self.text_view)

        # Setup header/stats bar
        self.headerbar_visible = True
        self.bottombar_visible = True
        self.buffer_modified_for_status_bar = False

        # Setting up spellcheck
        self.toggle_spellcheck(self.settings.get_value("spellcheck"))
        self.did_change = False

        ###
        #   Sidebar initialization test
        ###
        # self.paned_window = builder.get_object("main_paned")
        # self.sidebar_box = builder.get_object("sidebar_box")
        # self.sidebar = Sidebar(self)
        # self.sidebar_box.hide()

        ###
        #   Search and replace initialization
        ###
        self.searchreplace = SearchAndReplace(self, self.text_view, builder)

        # EventBoxes

        self.headerbar_eventbox = builder.get_object("HeaderbarEventbox")
        self.headerbar_eventbox.connect('enter_notify_event',
                                        self.reveal_headerbar_bottombar)

        self.stats_revealer.connect('enter_notify_event',
                                    self.reveal_bottombar)

        self.new_document()

    def header_size_allocate(self, widget, allocation):
        """ When the main hb starts to shrink its size, add that size
            to the textview margin, so it stays in place
        """

        # prevent 1px jumps
        if not widget.get_child_revealed():
            allocation.height = 0

        height = self.headerbar.hb.get_allocated_height() - allocation.height
        if height == self.last_height:
            return

        self.last_height = height

        self.text_view.update_vertical_margin(height)
        self.text_view.queue_draw()

    def on_text_changed(self, *_args):
        """called when the text changes, sets the self.did_change to true and
           updates the title and the counters to reflect that
        """

        if self.did_change is False:
            self.did_change = True

        self.update_headerbar_title(True, True)
        self.buffer_modified_for_status_bar = True
        if self.settings.get_value("autohide-headerbar"):
            self.hide_headerbar_bottombar()

    def set_fullscreen(self, state):
        """Puts the application in fullscreen mode and show/hides
        the poller for motion in the top border

        Arguments:
            state {almost bool} -- The desired fullscreen state of the window
        """

        if state.get_boolean():
            self.fullscreen()
            self.fs_headerbar.events.show()
            self.fs_headerbar.hide_fs_hb()
            self.headerbar_eventbox.hide()
        else:
            self.unfullscreen()
            self.fs_headerbar.events.hide()
            self.headerbar_eventbox.show()
        self.text_view.grab_focus()

    def set_focus_mode(self, state):
        """toggle focusmode
        """

        self.text_view.set_focus_mode(state.get_boolean(),
                                      self.headerbar.hb.get_allocated_height())
        self.text_view.grab_focus()

    def set_hemingway_mode(self, state):
        """toggle hemingwaymode
        """

        self.text_view.set_hemingway_mode(state.get_boolean())
        self.text_view.grab_focus()

    def toggle_preview(self, state):
        """Toggle the preview mode

        Arguments:
            state {gtk bool} -- Desired state of the preview mode
        """

        if state.get_boolean():
            self.text_view.grab_focus()
            self.preview_handler.show()
            self.headerbar.preview_toggle_revealer.set_reveal_child(True)
            self.fs_headerbar.preview_toggle_revealer.set_reveal_child(True)
            self.dm_headerbar.preview_toggle_revealer.set_reveal_child(True)
        else:
            self.preview_handler.hide()
            self.text_view.grab_focus()
            self.headerbar.preview_toggle_revealer.set_reveal_child(False)
            self.fs_headerbar.preview_toggle_revealer.set_reveal_child(False)
            self.dm_headerbar.preview_toggle_revealer.set_reveal_child(False)

        return True

    def save_document(self, try_backup: bool = True):
        """Try to save buffer in the current gfile.
           If the file doesn't exist calls save_document_as
        """

        if self.current.gfile:
            LOGGER.info("saving")

            try:
                try:
                    encoded_text = GLib.Bytes.new(
                                   self.text_view.get_text()
                                   .encode(self.current.encoding))
                except UnicodeEncodeError:
                    encoded_text = self.text_view.get_text()\
                                    .encode("UTF-8")
                    self.current.encoding = "UTF-8"
            except UnicodeEncodeError as error:
                helpers.show_error(self, str(error.message))
                LOGGER.warning(str(error.message))
            else:
                self.progressbar.set_opacity(1)
                self.progressbar_initiate_tw.start()
                self.current.gfile.replace_contents_bytes_async(
                    encoded_text,
                    etag=None,
                    make_backup=try_backup,
                    flags=Gio.FileCreateFlags.NONE,
                    cancellable=None,
                    callback=self._replace_contents_cb,
                    user_data=None)

        else:
            self.save_document_as()

    def save_document_as(self, _widget=None, _data=None):
        """provide to the user a filechooser and save the document
           where they want. Call set_headbar_title after that
        """
        filefilter = Gtk.FileFilter.new()
        filefilter.add_mime_type('text/x-markdown')
        filefilter.add_mime_type('text/plain')
        filefilter.set_name('Markdown (.md)')
        filechooser = Gtk.FileChooserNative.new(
            _("Save your File"),
            self,
            Gtk.FileChooserAction.SAVE,
            _("Save"),
            _("Cancel")
        )
        filechooser.set_do_overwrite_confirmation(True)
        filechooser.set_local_only(False)
        filechooser.add_filter(filefilter)

        title = self.current.title
        if not title.endswith(".md"):
            title += ".md"
        filechooser.set_current_name(title)

        response = filechooser.run()

        if response == Gtk.ResponseType.ACCEPT:

            file = filechooser.get_file()

            if not file.query_exists():
                try:
                    file.create(Gio.FileCreateFlags.NONE)
                except GLib.GError as error:
                    helpers.show_error(self, str(error.message))
                    LOGGER.warning(str(error.message))
                    return

            self.current.gfile = file

            self.update_headerbar_title(False, True)
            filechooser.destroy()
            self.save_document()

        return response

    def _replace_contents_cb(self, gfile, result, _user_data=None):
        try:
            success, _etag = gfile.replace_contents_finish(result)
        except GLib.GError as error:
            if error.matches(Gio.io_error_quark(),
                             Gio.IOErrorEnum.CANT_CREATE_BACKUP):
                # some GVFS (i.e, google drive) don't allow backups
                # try again without attempting to make one
                self.save_document(try_backup=False)
            else:
                helpers.show_error(self, str(error.message))
                LOGGER.warning(str(error.message))
                self.progressbar_opacity_tw.start()
            return

        if success:
            recents_manager = Gtk.RecentManager.get_default()
            recents_manager.add_item(self.current.gfile.get_uri())

            self.progressbar_initiate_tw.stop()
            self.progressbar_finalize_tw.start()
            self.progressbar_opacity_tw.start()

            self.update_headerbar_title()
            self.did_change = False
        else:
            self.progressbar_opacity_tw.start()

        return success

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

        filechooser = Gtk.FileChooserNative.new(
            _("Open a .md file"),
            self,
            Gtk.FileChooserAction.OPEN,
            _("Open"),
            _("Cancel")
        )

        filechooser.set_local_only(False)
        filechooser.add_filter(markdown_filter)
        filechooser.add_filter(plaintext_filter)
        response = filechooser.run()
        if response == Gtk.ResponseType.ACCEPT:
            self.load_file(filechooser.get_file())
            filechooser.destroy()

        elif response == Gtk.ResponseType.CANCEL:
            filechooser.destroy()

    def load_file(self, file=None):
        """Open File from command line or open / open recent etc."""
        LOGGER.info("trying to open %s", file.get_path())

        if self.check_change() == Gtk.ResponseType.CANCEL:
            return
        self.current.gfile = file

        self.current.gfile.load_contents_async(None,
                                               self._load_contents_cb, None)

    def _load_contents_cb(self, gfile, result, user_data=None):
        try:
            _success, contents, _etag = gfile.load_contents_finish(result)
        except GLib.GError as error:
            helpers.show_error(self, str(error.message))
            LOGGER.warning(str(error.message))
            return

        try:
            try:
                self.current.encoding = 'UTF-8'
                decoded = contents.decode(self.current.encoding)
            except UnicodeDecodeError:
                self.current.encoding = chardet.detect(contents)['encoding']
                decoded = contents.decode(self.current.encoding)
        except UnicodeDecodeError as error:
            helpers.show_error(self, str(error.message))
            LOGGER.warning(str(error.message))
            return
        else:
            self.text_view.set_text(decoded)
            start_iter = self.text_view.get_buffer().get_start_iter()
            GLib.idle_add(lambda: self.text_view.get_buffer().place_cursor(start_iter))

            self.update_headerbar_title()
            self.did_change = False

    def check_change(self):
        """Show dialog to prevent loss of unsaved changes
        """

        if self.did_change and self.text_view.get_text():
            dialog = Gtk.MessageDialog(self,
                                       Gtk.DialogFlags.MODAL |
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.NONE,
                                       _("Save changes to document " +
                                         "“%s” before closing?") %
                                       self.current.title
                                       )

            dialog.props.secondary_text = _("If you don’t save, " +
                                            "all your changes will be " +
                                            "permanently lost.")
            close_button = dialog.add_button(_("Close without saving"),
                                             Gtk.ResponseType.NO)
            dialog.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("Save now"), Gtk.ResponseType.YES)

            close_button.get_style_context().add_class("destructive-action")
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
        self.current.gfile = None
        self.update_headerbar_title(False, False)

    def update_default_stat(self):
        self.stats_handler.update_default_stat()

    def update_preview_mode(self):
        self.preview_handler.update_preview_mode()
        self.headerbar.update_preview_layout_icon()
        self.headerbar.select_preview_layout_row()
        self.fs_headerbar.update_preview_layout_icon()
        self.fs_headerbar.select_preview_layout_row()

    def menu_toggle_sidebar(self, _widget=None):
        """WIP
        """
        # self.sidebar.toggle_sidebar()

    def toggle_spellcheck(self, state):
        """Enable/disable the autospellchecking

        Arguments:
            status {gtk bool} -- Desired status of the spellchecking
        """
        self.text_view.set_spellcheck(state.get_boolean())

    def reload_preview(self, reshow=False):
        self.preview_handler.reload(reshow=reshow)

    def open_search(self, replace=False):
        """toggle the search box
        """
        self.searchreplace.toggle_search(replace=replace)

    def open_export(self, export_format):
        """open the export dialog
        """
        text = bytes(self.text_view.get_text(), "utf-8")

        export_dialog = ExportDialog(self.current, export_format, text)
        export_dialog.dialog.set_transient_for(self)
        export_dialog.export()

    def open_advanced_export(self):
        """open the advanced export dialog
        """
        text = bytes(self.text_view.get_text(), "utf-8")

        export_dialog = AdvancedExportDialog(self.current, text)
        export_dialog.set_transient_for(self)
        export_dialog.show()

    def focus_out(self, _widget, _data=None):
        """events called when the window losses focus
        """
        self.reveal_headerbar_bottombar()

    def reveal_headerbar_bottombar(self, _widget=None, _data=None):

        def __reveal_hb():
            self.headerbar_eventbox.hide()
            self.headerbar.hb_revealer.set_reveal_child(True)
            self.get_style_context().remove_class("focus")
            return False

        self.reveal_bottombar()

        if not self.headerbar_visible:
            self.dm_headerbar.hide_dm_hb()
            GLib.timeout_add(400, __reveal_hb)

            self.headerbar_visible = True

    def reveal_bottombar(self, _widget=None, _data=None):

        if not self.bottombar_visible:
            self.stats_revealer.set_reveal_child(True)
            self.stats_revealer.set_halign(Gtk.Align.END)
            self.stats_revealer.queue_resize()

            self.bottombar_visible = True

        self.buffer_modified_for_status_bar = True

    def hide_headerbar_bottombar(self):

        if self.headerbar_visible:
            self.headerbar.hb_revealer.set_reveal_child(False)
            self.dm_headerbar.show_dm_hb()
            self.get_style_context().add_class("focus")

            self.headerbar_visible = False

        if self.bottombar_visible:
            self.stats_revealer.set_reveal_child(False)
            self.stats_revealer.set_halign(Gtk.Align.FILL)

            self.bottombar_visible = False

        self.headerbar_eventbox.show()
        self.buffer_modified_for_status_bar = False

    def on_delete_called(self, _widget, _data=None):
        """Called when the TexteditorWindow is closed.
        """
        LOGGER.info('delete called')
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return True
        return False

    def update_headerbar_title(self,
                               is_unsaved: bool = False,
                               has_subtitle: bool = True):
        """update headerbar title and subtitle
        """

        if is_unsaved:
            prefix = "* "
        else:
            prefix = ""

        suffix = " - Apostrophe"

        title = prefix + self.current.title + suffix

        if has_subtitle:
            subtitle = self.current.path
        else:
            subtitle = ""

        self.headerbar.hb.set_title(title)
        self.dm_headerbar.hb.set_title(title)
        self.fs_headerbar.hb.set_title(title)

        self.headerbar.hb.set_subtitle(subtitle)
        self.dm_headerbar.hb.set_subtitle(subtitle)
        self.fs_headerbar.hb.set_subtitle(subtitle)

        self.headerbar.hb.set_tooltip_text(subtitle)
        self.fs_headerbar.hb.set_tooltip_text(subtitle)

        self.set_title(title)


@dataclass
class File():
    """Class for keeping track of files, their attributes, and their methods"""

    def __init__(self, gfile=None, encoding="UTF-8"):
        self._settings = Settings.new()
        self.gfile = gfile
        self.encoding = encoding
        self.path = ""
        self.title = ""
        self.name = ""

    @property
    def gfile(self):
        return self._gfile

    @gfile.setter
    def gfile(self, file):
        if file:
            if file.is_native():
                self.path = file.get_parent().get_path()
                base_path = file.get_parent().get_path()
                os.chdir(base_path)
            else:
                self.path = file.get_parent().get_uri()
                base_path = "/"

            file_info = file.query_info("standard",
                                        Gio.FileQueryInfoFlags.NONE,
                                        None)
            self.title = file_info.get_attribute_as_string(
                         "standard::display-name")
        else:
            self.title = _("New File")
            base_path = "/"
        self.name = self.title
        if self.name.endswith(".md"):
            self.name = self.name[:-3]
        # TODO: remove path in favor of gfile
        self._settings.set_string("open-file-path", base_path)
        self._gfile = file
