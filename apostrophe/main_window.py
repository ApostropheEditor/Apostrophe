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
from dataclasses import dataclass
from gettext import gettext as _

import chardet
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Adw, Gdk, Gio, GLib, GObject, Gtk

from apostrophe import helpers
from apostrophe.export_dialog import ExportDialog, AdvancedExportDialog
from apostrophe.headerbars import BaseHeaderbar
from apostrophe.helpers import App
from apostrophe.search_and_replace import ApostropheSearchBar
from apostrophe.settings import Settings
# from apostrophe.preview_handler import PreviewHandler
from apostrophe.stats_handler import StatsHandler
from apostrophe.text_view import ApostropheTextView

LOGGER = logging.getLogger('apostrophe')


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/Window.ui')
class MainWindow(Adw.ApplicationWindow):

    __gtype_name__ = "ApostropheWindow"


    editor_scrolledwindow = Gtk.Template.Child()
    save_progressbar = Gtk.Template.Child()
    headerbar = Gtk.Template.Child()
    searchbar = Gtk.Template.Child()
    stats_revealer = Gtk.Template.Child()
    stats_button = Gtk.Template.Child()
    # flap = Gtk.Template.Child()
    # # TODO ??
    # preview_stack = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    textview = Gtk.Template.Child()

    subtitle = GObject.Property(type=str)
    is_fullscreen = GObject.Property(type=bool, default=False)

    preview = GObject.Property(type=bool, default=False)
    preview_layout = GObject.Property(type=int, default=1)

    did_change = GObject.Property(type=bool, default=False)

    close_anyway = False

    def __init__(self, app):
        """Set up the main window"""

        super().__init__(application=Gio.Application.get_default(),
                         title="Apostrophe")

        #TODO: size

        # Preferences
        self.settings = Settings.new()

        # Connect signals that we can't connect on the UI file
        self.connect("notify::is-fullscreen", self._on_fullscreen)
        # Create new, empty file
        # TODO: load last opened file?

        self.current = File()

        # Setup text editor
        self.textview.get_buffer().connect('changed', self.on_text_changed)

        # Setup save progressbar an its animator
        def hide_progressbar(animation, *args):
            self.save_progressbar.hide()

        fade_target = Adw.PropertyAnimationTarget.new(self.save_progressbar, "opacity")
        self.progressbar_fade_out = Adw.TimedAnimation.new(self.save_progressbar, 1, 0, 500, fade_target)
        self.progressbar_fade_out.set_easing(Adw.Easing.EASE_OUT_CUBIC)
        self.progressbar_fade_out.connect("done", hide_progressbar)

        def on_progressbar_value(animation, *args):
            if animation.get_value() > 0.3 and self.did_change:
                animation.pause()
            
        def fade_out_progressbar(animation, *args):
            self.progressbar_fade_out.play()

        fraction_target = Adw.PropertyAnimationTarget.new(self.save_progressbar, "fraction")
        self.progressbar_animation = Adw.TimedAnimation.new(self.save_progressbar, 0, 1, 300, fraction_target)
        self.progressbar_animation.connect("notify::value", on_progressbar_value)
        self.progressbar_animation.connect("done", fade_out_progressbar)

        # Setup stats counter
        self.stats_handler = StatsHandler(self.stats_button, self.textview)

        # Setup preview
        #self.preview_handler = PreviewHandler(self, self.textview, self.flap)

        # Setting up spellcheck
        #self.settings.bind("spellcheck", self.textview,
        #                   "spellcheck", Gio.SettingsBindFlags.GET)

        # Setting up text size
        self.settings.bind("bigger-text", self.textview,
                           "bigger_text", Gio.SettingsBindFlags.GET)

        self.settings.bind("characters-per-line", self.textview,
                           "line_chars", Gio.SettingsBindFlags.GET)

        # Search and replace initialization
        self.searchbar.attach(self.textview)

        # Hemingway Toast
        self.hemingway_toast = Adw.Toast.new(_("Text can't be deleted while on Hemingway mode"))
        self.hemingway_toast.set_timeout(3)
        self.hemingway_toast.set_action_name("win.show_hemingway_help")
        self.hemingway_toast.set_button_label(_("Tell me more"))

        # Actions
        action = Gio.PropertyAction.new("find", self.searchbar, "search-mode-enabled")
        self.add_action(action)

        action = Gio.PropertyAction.new("find_replace", self.searchbar, "replace-mode-enabled")
        self.add_action(action)

        action = Gio.PropertyAction.new("focus_mode", self.textview, "focus-mode")
        self.add_action(action)

        action = Gio.PropertyAction.new("hemingway_mode", self.textview, "hemingway-mode")
        self.add_action(action)
        self.textview.connect("notify::hemingway-mode", self.show_hemingway_toast)

        action = Gio.SimpleAction.new("show_hemingway_toast", None)
        action.connect("activate", self.show_hemingway_toast)
        self.add_action(action)

        action = Gio.SimpleAction.new("show_hemingway_help", None)
        action.connect("activate", self.show_hemingway_help)
        self.add_action(action)

        action = Gio.PropertyAction.new("fullscreen", self, "is-fullscreen")
        self.add_action(action)

        action = Gio.PropertyAction.new("preview", self, "preview")
        self.add_action(action)
        #self.connect("notify::preview", self.toggle_preview)

        # currently unused, we rather open a new window
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

        scrollbar = self.editor_scrolledwindow.get_vscrollbar()
        scrollbar.set_margin_top(54)
        scrollbar.set_margin_bottom(48)

        vadjustment = self.editor_scrolledwindow.get_vadjustment()
        vadjustment.connect("notify::value", self._on_scroll)

        # not really necessary but we'll keep a preview_layout property on the window
        # and bind it both to the switcher and the renderer
        self.preview_layout = self.settings.get_enum("preview-mode")
        # self.bind_property("preview_layout", self.headerbar.preview_layout_switcher, 
        #                    "preview_layout", GObject.BindingFlags.BIDIRECTIONAL|GObject.BindingFlags.SYNC_CREATE)

        # self.bind_property("preview_layout", self.preview_handler.preview_renderer, 
        #                    "preview_layout", GObject.BindingFlags.SYNC_CREATE)

        self.preview = self.settings.get_boolean("preview-active")

        self.textview.hemingway_mode = self.settings.get_boolean("hemingway-mode")

        self.new_document()

    def on_text_changed(self, *_args):
        """called when the text changes, sets the self.did_change to true and
           updates the title and the counters to reflect that
        """

        if self.did_change is False:
            self.did_change = True
        self.update_headerbar_title(True, True)
        if self.settings.get_value("autohide-headerbar"):
            self.hide_headerbar_bottombar()

    def _on_scroll(self, *args):
        """called when there's scroll. If value is 0 there's no scrolling and
           we add an inset shadow
        """
        if self.editor_scrolledwindow.get_vadjustment().get_value() != 0:
            self.add_css_class("scrolled")
        else:
            self.remove_css_class("scrolled")

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

        self.textview.grab_focus()

    def toggle_preview(self, *args, **kwargs):
        """Toggle the preview mode
        """

        if self.preview:
            self.textview.grab_focus()
            self.preview_handler.show()
        else:
            self.preview_handler.hide()
            self.textview.grab_focus()

    def save_document(self, _action=None, _value=None, sync: bool = False) -> bool:
        """Try to save buffer in the current gfile.
        If the file doesn't exist calls save_document_as

        Args:
            sync (bool, optional): Wheter the save operation should be done
            synchronously. Defaults to False.

        Returns:
            bool: True if the document was saved correctly
        """

        self.reveal_headerbar_bottombar()
        if self.current.gfile:
            LOGGER.info("saving")

            # We try to encode the file with the given encoding
            # if that doesn't work, we try with UTF-8
            # if that fails as well, we return False
            try:
                try:
                    encoded_text = self.textview.get_text()\
                        .encode(self.current.encoding)
                except UnicodeEncodeError:
                    encoded_text = self.textview.get_text()\
                        .encode("UTF-8")
                    self.current.encoding = "UTF-8"
            except UnicodeEncodeError as error:
                helpers.show_error(self, str(error.reason))
                LOGGER.warning(str(error.reason))
                return False
            else:
                self.save_progressbar.set_opacity(1)
                self.save_progressbar.set_visible(True)
                self.progressbar_animation.play()

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
                        LOGGER.warning(str(error.message))
                        self.did_change = True
                        self.progressbar_fade_out.play()
                        helpers.show_error(self, str(error.message))
                        return False

                    if res:
                        if self.progressbar_animation.get_state() == Adw.AnimationState.PAUSED:
                            self.progressbar_animation.resume()

                        self.update_headerbar_title()
                        self.did_change = False
                        return True

                    else:
                        self.progressbar_fade_out.play()
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

        def on_response(dialog, response):
            if response == Gtk.ResponseType.ACCEPT:

                file = dialog.get_file()

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
                dialog.destroy()
                return self.save_document()
            else:
                return False

        filefilter = Gtk.FileFilter.new()
        filefilter.add_mime_type('text/x-markdown')
        filefilter.add_mime_type('text/plain')
        filefilter.set_name('Markdown (.md)')
        self.filechooser = Gtk.FileChooserNative.new(
            _("Save your File"),
            self,
            Gtk.FileChooserAction.SAVE,
            _("Save"),
            _("Cancel")
        )
        self.filechooser.add_filter(filefilter)
        self.filechooser.set_modal(True)
        self.filechooser.set_transient_for(self)

        title = self.current.title
        if not title.endswith(".md"):
            title += ".md"
        self.filechooser.set_current_name(title)

        self.filechooser.connect("response", on_response)

        self.filechooser.show()

    def _replace_contents_cb(self, gfile, result, _user_data=None):
        try:
            success, _etag = gfile.replace_contents_finish(result)
        except GLib.GError as error:
            LOGGER.warning(str(error.message))
            self.did_change = True
            self.progressbar_fade_out.play()
            helpers.show_error(self, str(error.message))
            return False

        if success:
            if self.progressbar_animation.get_state() == Adw.AnimationState.PAUSED:
                self.progressbar_animation.resume()

            self.update_headerbar_title()
            self.did_change = False
        else:
            self.progressbar_fade_out.play()
            self.did_change = True

        return success

    def copy_html_to_clipboard(self, _widget=None, _date=None):
        """Copies only html without headers etc. to Clipboard
        """

        output = helpers.pandoc_convert(self.textview.get_text())
        clipboard = self.get_clipboard()
        clipboard.set(output)

    def open_document(self, _action, _value):
        """open the desired file
        """
        self.headerbar.open_menu.popdown()

        def on_response(dialog, response):
            if response == Gtk.ResponseType.ACCEPT:
                self.get_application().open([dialog.get_file()], "")

        markdown_filter = Gtk.FileFilter.new()
        markdown_filter.add_mime_type('text/markdown')
        markdown_filter.add_mime_type('text/x-markdown')
        markdown_filter.set_name(_('Markdown Files'))

        plaintext_filter = Gtk.FileFilter.new()
        plaintext_filter.add_mime_type('text/plain')
        plaintext_filter.set_name(_('Plain Text Files'))

        self.filechooser = Gtk.FileChooserNative.new(
            _("Open a .md file"),
            self,
            Gtk.FileChooserAction.OPEN,
            _("Open"),
            _("Cancel")
        )

        self.filechooser.set_modal(True)
        self.filechooser.set_transient_for(self)

        self.filechooser.add_filter(markdown_filter)
        self.filechooser.add_filter(plaintext_filter)

        self.filechooser.connect("response", on_response)
        self.filechooser.show()

    def open_from_gvariant(self, _action, gvariant):
        self.headerbar.open_menu.popdown()
        self.get_application().open([Gio.File.new_for_uri(gvariant.get_string())], "")

    def load_file(self, file=None):
        """Open File from command line or open / open recent etc."""
        LOGGER.info("trying to open %s", file.get_uri())

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
            self.textview.set_text(decoded)
            start_iter = self.textview.get_buffer().get_start_iter()
            GLib.idle_add(
                lambda: self.textview.get_buffer().place_cursor(start_iter))

            ## add file to recents manager once it's fully loaded,
            # unless it is an internal resource
            if not self.current.gfile.get_uri().startswith("resource:"):
                recents_manager = Gtk.RecentManager.get_default()
                recents_manager.add_item(self.current.gfile.get_uri())

            self.update_headerbar_title()

            self.did_change = False

    def check_change(self,
                     callback = None):
        """Show dialog to prevent loss of unsaved changes
        """

        if self.did_change:
            dialog = Adw.MessageDialog.new(self,
                                           _("Save changes?"),
                                           _("“%s” contains unsaved changes. " +
                                             "If you don’t save, " +
                                             "all your changes will be " +
                                             "permanently lost.") % self.current.title
                                           )
            dialog.add_response("cancel", _("Cancel"))
            dialog.add_response("close", _("Discard"))
            dialog.add_response("save", _("Save"))
            dialog.set_response_appearance("close", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
            dialog.set_default_response("save")
            dialog.set_close_response("cancel")

            def on_response(message_dialog, response):
                if response == "cancel":
                    return
                if response == "save":
                    # If the saving fails, retry
                    if self.save_document(sync=True) is False:
                        return
                if callback is not None:
                    callback(self)

            dialog.connect("response", on_response)

            dialog.present()
            return
        else:
            if callback is not None:
                callback(self)

    def new_document(self, *args, **kwargs):
        """create new document in the same window
        """
        def callback(self):
            self.textview.clear()

            self.did_change = False
            self.current.gfile = None
            self.update_headerbar_title(False, False)

        self.check_change(callback)

    def update_default_stat(self):
        self.stats_handler.update_default_stat()

    def reload_preview(self, reshow=False):
        self.preview_handler.reload(reshow=reshow)

    def open_export(self, _action, value):
        """open the export dialog
        """
        text = bytes(self.textview.get_text(), "utf-8")

        export_format = value.get_string()

        export_dialog = ExportDialog(self.current, export_format, text)
        export_dialog.dialog.set_transient_for(self)
        export_dialog.export()

    def open_advanced_export(self, *args, **kwargs):
        """open the advanced export dialog
        """
        text = bytes(self.textview.get_text(), "utf-8")

        export_dialog = AdvancedExportDialog(self.current, text)
        export_dialog.set_transient_for(self)
        export_dialog.show()

    def show_hemingway_toast(self, *args):
        if self.textview.hemingway_mode:
            # Only show the first three times
            count = self.settings.get_int("hemingway-toast-count")
            if count >= 3:
                return
            count += 1
            self.settings.set_int("hemingway-toast-count", count)

            self.toast_overlay.add_toast(self.hemingway_toast)

    def show_hemingway_help(self, *args):
        hemingway_dialog = Gtk.Builder.new_from_resource("/org/gnome/gitlab/somas/Apostrophe/ui/AboutHemingway.ui")\
                           .get_object("dialog")
        hemingway_dialog.set_transient_for(self)
        hemingway_dialog.present()

    @Gtk.Template.Callback()
    def reveal_headerbar_bottombar(self, *args):

        self.reveal_bottombar()

        if not self.headerbar.get_reveal_child():
            self.headerbar.set_reveal_child(True)

    @Gtk.Template.Callback()
    def reveal_bottombar(self, *args):
        if not self.stats_revealer.get_reveal_child():
            self.stats_revealer.set_reveal_child(True)
            self.stats_revealer.set_halign(Gtk.Align.END)
            self.stats_revealer.queue_resize()

    def hide_headerbar_bottombar(self):
        if self.searchbar.search_mode_enabled:
            return

        if self.headerbar.get_reveal_child():
            self.headerbar.set_reveal_child(False)

        if self.stats_revealer.get_reveal_child():
            self.stats_revealer.set_reveal_child(False)
            self.stats_revealer.set_halign(Gtk.Align.FILL)

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
        self.settings.set_boolean("hemingway-mode", self.textview.hemingway_mode)

    def do_close_request(self, *args):
        LOGGER.info('close request called')

        if self.close_anyway:
            self.get_application().windows.remove(self.get_group())
            self.destroy()
            return False

        # called if check_change decides we can throw away the contents of the textview
        def callback(window):
            # save state if we're the last window group left
            n_windows = len(window.get_application().windows)
            if n_windows == 1:
                window.save_state()
            window.close_anyway = True
            window.do_close_request()

        self.check_change(callback)
        return True

@dataclass
class File():
    """Class for keeping track of files, their attributes, and their methods"""

    def __init__(self, gfile=None, encoding="UTF-8"):
        self._settings = Settings.new()
        self.gfile = gfile
        self.encoding = encoding
        self.path = ""
        self.title = _("New File")
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
