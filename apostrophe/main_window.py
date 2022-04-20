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
import os
from gettext import gettext as _

from dataclasses import dataclass
import chardet

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib, Gio, Handy

from apostrophe.export_dialog import ExportDialog, AdvancedExportDialog
from apostrophe.preview_handler import PreviewHandler
from apostrophe.stats_handler import StatsHandler
from apostrophe.text_view import ApostropheTextView
from apostrophe.search_and_replace import ApostropheSearchBar
from apostrophe.insecure_file_warning import ApostropheInsecureFileWarning
from apostrophe.settings import Settings
from apostrophe.tweener import Tweener
from apostrophe.helpers import App
from apostrophe import helpers

from .headerbars import BaseHeaderbar

LOGGER = logging.getLogger('apostrophe')


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/Window.ui')
class MainWindow(Handy.ApplicationWindow):

    __gtype_name__ = "ApostropheWindow"


    editor_scrolledwindow = Gtk.Template.Child()
    save_progressbar = Gtk.Template.Child()
    headerbar = Gtk.Template.Child()
    headerbar_eventbox = Gtk.Template.Child()
    searchbar = Gtk.Template.Child()
    stats_revealer = Gtk.Template.Child()
    stats_button = Gtk.Template.Child()
    flap = Gtk.Template.Child()
    # TODO ??
    preview_stack = Gtk.Template.Child()
    text_view = Gtk.Template.Child()
    editor = Gtk.Template.Child()

    subtitle = GObject.Property(type=str)
    is_fullscreen = GObject.Property(type=bool, default=False)
    headerbar_visible = GObject.Property(type=bool, default=True)
    bottombar_visible = GObject.Property(type=bool, default=True)

    preview = GObject.Property(type=bool, default=False)
    preview_layout = GObject.Property(type=int, default=1)

    did_change = GObject.Property(type=bool, default=False)

    def __init__(self, app):
        """Set up the main window"""

        super().__init__(application=Gio.Application.get_default(),
                         title="Apostrophe")

        #TODO: size

        # Preferences
        self.settings = Settings.new()

        # Create new, empty file
        # TODO: load last opened file?

        self.current = File()

        # Setup text editor
        self.text_view.get_buffer().connect('changed', self.on_text_changed)
        self.text_view.grab_focus()

        # Setup save progressbar an its animator
        self.progressbar_initiate_tw = Tweener(self.save_progressbar,
                                               self.save_progressbar.set_fraction,
                                               0, 0.125, 40)
        self.progressbar_finalize_tw = Tweener(self.save_progressbar,
                                               self.save_progressbar.set_fraction,
                                               0.125, 1, 400)
        self.progressbar_opacity_tw = Tweener(self.save_progressbar,
                                              self.save_progressbar.set_opacity,
                                              1, 0, 300, 200,
                                              callback = self.save_progressbar.set_visible,
                                              callback_arg = False)

        # Setup stats counter
        self.stats_handler = StatsHandler(self.stats_button, self.text_view)

        # Setup preview
        self.preview_handler = PreviewHandler(self, self.text_view, self.flap)

        # Setting up spellcheck
        self.settings.bind("spellcheck", self.text_view,
                           "spellcheck", Gio.SettingsBindFlags.GET)

        # Setting up text size
        self.settings.bind("bigger-text", self.text_view,
                           "bigger_text", Gio.SettingsBindFlags.GET)

        self.settings.bind("characters-per-line", self.text_view,
                           "line_chars", Gio.SettingsBindFlags.GET)

        # Search and replace initialization
        self.searchbar.attach(self.text_view)

        # Actions
        action = Gio.PropertyAction.new("find", self.searchbar, "search-mode-enabled")
        self.add_action(action)

        action = Gio.PropertyAction.new("find_replace", self.searchbar, "replace-mode-enabled")
        self.add_action(action)

        action = Gio.PropertyAction.new("focus_mode", self.text_view, "focus-mode")
        self.add_action(action)

        action = Gio.PropertyAction.new("hemingway_mode", self.text_view, "hemingway-mode")
        self.add_action(action)

        action = Gio.PropertyAction.new("fullscreen", self, "is-fullscreen")
        self.add_action(action)

        action = Gio.PropertyAction.new("preview", self, "preview")
        self.add_action(action)
        self.connect("notify::preview", self.toggle_preview)


        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.new_document)
        self.add_action(action)

        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.open_document)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_file", GLib.VariantType("s"))
        action.connect("activate", self.open_from_gvariant)
        self.add_action(action)

        action = Gio.SimpleAction.new("save", None)
        action.connect("activate", self.save_document)
        self.add_action(action)

        action = Gio.SimpleAction.new("save_as", None)
        action.connect("activate", self.save_document_as)
        self.add_action(action)

        action = Gio.SimpleAction.new("export", GLib.VariantType("s"))
        action.connect("activate", self.open_export)
        self.add_action(action)

        action = Gio.SimpleAction.new("advanced_export", None)
        action.connect("activate", self.open_advanced_export)
        self.add_action(action)

        action = Gio.SimpleAction.new("copy_html", None)
        action.connect("activate", self.copy_html_to_clipboard)
        self.add_action(action)

        # not really necessary but we'll keep a preview_layout property on the window
        # and bind it both to the switcher and the renderer
        self.preview_layout = self.settings.get_enum("preview-mode")
        self.bind_property("preview_layout", self.headerbar.preview_layout_switcher, 
                           "preview_layout", GObject.BindingFlags.BIDIRECTIONAL|GObject.BindingFlags.SYNC_CREATE)

        self.bind_property("preview_layout", self.preview_handler.preview_renderer, 
                           "preview_layout", GObject.BindingFlags.SYNC_CREATE)

        self.preview = self.settings.get_boolean("preview-active")

        self.text_view.hemingway_mode = self.settings.get_boolean("hemingway-mode")

        self.new_document()

    # TODO: change to closures on GTK4
    # "Bind" scrolled window's scrollbar margin to headerbar visibility
    @Gtk.Template.Callback()
    def headerbar_revealed_cb(self, widget, *args):
        scrollbar = self.editor_scrolledwindow.get_vscrollbar()
        scrollbar.set_margin_top(46 if widget.get_reveal_child() else 0)

    def on_text_changed(self, *_args):
        """called when the text changes, sets the self.did_change to true and
           updates the title and the counters to reflect that
        """

        if self.did_change is False:
            self.did_change = True
        self.update_headerbar_title(True, True)
        if self.settings.get_value("autohide-headerbar"):
            self.hide_headerbar_bottombar()

    @Gtk.Template.Callback()
    def _on_fullscreen(self, *args, **kwargs):
        """Puts the application in fullscreen mode and show/hides
        the poller for motion in the top border
        """
        if self.is_fullscreen == True:
            self.fullscreen()
            self.hide_headerbar_bottombar()
        else:
            self.unfullscreen()
            self.reveal_headerbar_bottombar()

        self.text_view.grab_focus()

    def toggle_preview(self, *args, **kwargs):
        """Toggle the preview mode
        """

        if self.preview:
            self.text_view.grab_focus()
            self.preview_handler.show()
        else:
            self.preview_handler.hide()
            self.text_view.grab_focus()

    def save_document(self, _action=None, _value=None, sync: bool = False) -> bool:
        """Try to save buffer in the current gfile.
        If the file doesn't exist calls save_document_as

        Args:
            sync (bool, optional): Wheter the save operation should be done
            synchronously. Defaults to False.

        Returns:
            bool: True if the document was saved correctly
        """

        if self.current.gfile:
            LOGGER.info("saving")

            # We try to encode the file with the given encoding
            # if that doesn't work, we try with UTF-8
            # if that fails as well, we return False
            try:
                try:
                    encoded_text = self.text_view.get_text()\
                        .encode(self.current.encoding)
                except UnicodeEncodeError:
                    encoded_text = self.text_view.get_text()\
                        .encode("UTF-8")
                    self.current.encoding = "UTF-8"
            except UnicodeEncodeError as error:
                helpers.show_error(self, str(error.reason))
                LOGGER.warning(str(error.reason))
                return False
            else:
                self.save_progressbar.set_opacity(1)
                self.save_progressbar.set_visible(True)
                self.progressbar_initiate_tw.start()

                # we allow synchronously saving operations
                # for result-dependant code
                if sync:
                    try:
                        res = self.current.gfile.replace_contents(
                            encoded_text,
                            etag=None,
                            make_backup=False,
                            flags=Gio.FileCreateFlags.NONE,
                            cancellable=None)
                    except GLib.GError as error:
                        helpers.show_error(self, str(error.message))
                        LOGGER.warning(str(error.message))
                        self.progressbar_opacity_tw.start()
                        self.did_change = True
                        return False

                    if res:
                        self.progressbar_initiate_tw.stop()
                        self.progressbar_finalize_tw.start()
                        self.progressbar_opacity_tw.start()

                        self.update_headerbar_title()
                        self.did_change = False
                        return True

                    else:
                        self.progressbar_opacity_tw.start()
                        self.did_change = True
                        return False

                else:
                    self.current.gfile.replace_contents_bytes_async(
                        GLib.Bytes.new(encoded_text),
                        etag=None,
                        make_backup=False,
                        flags=Gio.FileCreateFlags.NONE,
                        cancellable=None,
                        callback=self._replace_contents_cb,
                        user_data=None)
                    return True
        # if there's no GFile we ask for one:
        else:
            return self.save_document_as(sync=sync)

    def save_document_as(self, _widget=None, _data=None,
                         sync: bool = False) -> bool:
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
        filechooser.set_modal(True)
        filechooser.set_transient_for(self)

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
                    return False

            self.current.gfile = file

            recents_manager = Gtk.RecentManager.get_default()
            recents_manager.add_item(self.current.gfile.get_uri())

            self.update_headerbar_title(False, True)
            filechooser.destroy()
            return self.save_document()
        else:
            return False

    def _replace_contents_cb(self, gfile, result, _user_data=None):
        try:
            success, _etag = gfile.replace_contents_finish(result)
        except GLib.GError as error:
            helpers.show_error(self, str(error.message))
            LOGGER.warning(str(error.message))
            self.progressbar_opacity_tw.start()
            self.did_change = True
            return False

        if success:
            self.progressbar_initiate_tw.stop()
            self.progressbar_finalize_tw.start()
            self.progressbar_opacity_tw.start()

            self.update_headerbar_title()
            self.did_change = False
        else:
            self.did_change = True
            self.progressbar_opacity_tw.start()

        return success

    def copy_html_to_clipboard(self, _widget=None, _date=None):
        """Copies only html without headers etc. to Clipboard
        """

        output = helpers.pandoc_convert(self.text_view.get_text())
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(output, -1)
        clipboard.store()

    def open_document(self, _action, _value):
        """open the desired file
        """

        response = self.check_change()
        if (response == Gtk.ResponseType.CANCEL or
            response == Gtk.ResponseType.DELETE_EVENT):
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

    def open_from_gvariant(self, _action, gvariant):
        self.load_file(Gio.File.new_for_uri(gvariant.get_string()))

    def load_file(self, file=None):
        """Open File from command line or open / open recent etc."""
        LOGGER.info("trying to open %s", file.get_path())

        response = self.check_change()
        if (response == Gtk.ResponseType.CANCEL or
            response == Gtk.ResponseType.DELETE_EVENT):
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
            GLib.idle_add(
                lambda: self.text_view.get_buffer().place_cursor(start_iter))

            ## add file to recents manager once it's fully loaded,
            # unless it is an internal resource
            if not self.current.gfile.get_uri().startswith("resource:"):
                recents_manager = Gtk.RecentManager.get_default()
                recents_manager.add_item(self.current.gfile.get_uri())

            self.update_headerbar_title()

            self.did_change = False

    def check_change(self) -> Gtk.ResponseType:
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
            dialog.set_default_response(Gtk.ResponseType.YES)
            response = dialog.run()

            dialog.destroy()

            if response == Gtk.ResponseType.YES:
                # If the saving fails, retry
                if self.save_document(sync=True) is False:
                    return self.check_change()

            return response

    def new_document(self, *args, **kwargs):
        """create new document
        """

        response = self.check_change()
        if (response == Gtk.ResponseType.CANCEL or
            response == Gtk.ResponseType.DELETE_EVENT):
            return
        self.text_view.clear()

        self.did_change = False
        self.current.gfile = None
        self.update_headerbar_title(False, False)

    def update_default_stat(self):
        self.stats_handler.update_default_stat()

    def reload_preview(self, reshow=False):
        self.preview_handler.reload(reshow=reshow)

    def open_export(self, _action, value):
        """open the export dialog
        """
        text = bytes(self.text_view.get_text(), "utf-8")

        export_format = value.get_string()

        export_dialog = ExportDialog(self.current, export_format, text)
        export_dialog.dialog.set_transient_for(self)
        export_dialog.export()

    def open_advanced_export(self, *args, **kwargs):
        """open the advanced export dialog
        """
        text = bytes(self.text_view.get_text(), "utf-8")

        export_dialog = AdvancedExportDialog(self.current, text)
        export_dialog.set_transient_for(self)
        export_dialog.show()

    @Gtk.Template.Callback()
    def reveal_headerbar_bottombar(self, _widget=None, _data=None):

        self.reveal_bottombar()

        if not self.headerbar_visible:
            self.headerbar_eventbox.hide()
            self.headerbar.set_visible(True)
            self.headerbar.set_reveal_child(True)
            self.get_style_context().remove_class("focus")
            self.headerbar_visible = True

    @Gtk.Template.Callback()
    def reveal_bottombar(self, _widget=None, _data=None):

        if not self.bottombar_visible:
            self.stats_revealer.set_reveal_child(True)
            self.stats_revealer.set_halign(Gtk.Align.END)
            self.stats_revealer.queue_resize()

            self.bottombar_visible = True

    def hide_headerbar_bottombar(self):

        if self.searchbar.get_search_mode():
            return

        if self.headerbar_visible:
            self.headerbar.set_reveal_child(False)
            self.get_style_context().add_class("focus")

            self.headerbar_visible = False

        if self.bottombar_visible:
            self.stats_revealer.set_reveal_child(False)
            self.stats_revealer.set_halign(Gtk.Align.FILL)

            self.bottombar_visible = False

        self.headerbar_eventbox.show()

    # TODO: this has to go
    def update_headerbar_title(self,
                               is_unsaved: bool = False,
                               has_subtitle: bool = True):
        """update headerbar title and subtitle
        """

        if is_unsaved:
            prefix = "• "
            # TODO: this doesn't really belong here
            App().inhibitor.inhibit(Gtk.ApplicationInhibitFlags.LOGOUT)
        else:
            prefix = ""
            App().inhibitor.uninhibit()

        title = prefix + self.current.title

        if has_subtitle:
            subtitle = self.current.path
        else:
            subtitle = ""

        self.set_title(title)
        self.subtitle = subtitle
        self.headerbar.set_tooltip_text(subtitle)

    def save_state(self):
        self.settings.set_enum("preview-mode", self.preview_layout)
        self.settings.set_boolean("preview-active", self.preview)
        self.settings.set_boolean("hemingway-mode", self.text_view.hemingway_mode)

    @Gtk.Template.Callback()
    def on_delete_called(self, _widget, _data=None):
        """Called when the ApostropheWindow is closed.
        """
        LOGGER.info('delete called')
        response = self.check_change()
        if (response == Gtk.ResponseType.CANCEL or
            response == Gtk.ResponseType.DELETE_EVENT):
            return True

        # save state if we're the last window OR if only the preview window is left
        n_windows = len(self.get_application().get_windows())
        if n_windows == 1 or \
           (n_windows == 2 and self.preview_handler.preview_renderer.window):
            self.save_state()
        return False

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
        self.trusted = False

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
