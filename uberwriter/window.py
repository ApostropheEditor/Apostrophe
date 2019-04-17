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

import codecs
import locale
import logging
import os
import re
import urllib
import webbrowser
from gettext import gettext as _

import gi

from uberwriter.export_dialog import Export
from uberwriter.stats_counter import StatsCounter
from uberwriter.text_view import TextView

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')  # pylint: disable=wrong-import-position
from gi.repository import Gtk, Gdk, GObject, GLib, Gio
from gi.repository import WebKit2 as WebKit

import cairo

from uberwriter import helpers
from uberwriter.theme import Theme
from uberwriter.helpers import get_builder
from uberwriter.gtkspellcheck import SpellChecker

from uberwriter.sidebar import Sidebar
from uberwriter.search_and_replace import SearchAndReplace
from uberwriter.settings import Settings

from . import headerbars

# Some Globals
# TODO move them somewhere for better
# accesibility from other files

LOGGER = logging.getLogger('uberwriter')

CONFIG_PATH = os.path.expanduser("~/.config/uberwriter/")


class Window(Gtk.ApplicationWindow):
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

        Gtk.ApplicationWindow.__init__(self,
                                       application=Gio.Application.get_default(),
                                       title="Uberwriter")

        # Set UI
        self.builder = get_builder('Window')
        root = self.builder.get_object("FullscreenOverlay")
        root.connect('style-updated', self.apply_current_theme)
        self.add(root)

        self.set_default_size(900, 500)

        self.connect('delete-event', self.on_destroy)

        # Preferences
        self.settings = Settings.new()

        # Headerbars
        self.headerbar = headerbars.MainHeaderbar(app)
        self.set_titlebar(self.headerbar.hb_container)
        self.fs_headerbar = headerbars.FullscreenHeaderbar(self.builder, app)

        self.title_end = "  –  UberWriter"
        self.set_headerbar_title("New File" + self.title_end)

        self.word_count = self.builder.get_object('word_count')
        self.char_count = self.builder.get_object('char_count')

        # Setup status bar hide after 3 seconds
        self.status_bar = self.builder.get_object('status_bar_box')
        self.statusbar_revealer = self.builder.get_object('status_bar_revealer')
        self.status_bar.get_style_context().add_class('status-bar-box')
        self.status_bar_visible = True
        self.was_motion = True
        self.buffer_modified_for_status_bar = False

        self.timestamp_last_mouse_motion = 0
        if self.settings.get_value("poll-motion"):
            self.connect("motion-notify-event", self.on_motion_notify)
            GObject.timeout_add(3000, self.poll_for_motion)

        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)

        # Setup text editor
        self.text_view = TextView()
        self.text_view.props.halign = Gtk.Align.CENTER
        self.text_view.connect('focus-out-event', self.focus_out)
        self.text_view.show()
        self.text_view.grab_focus()

        self.text_view.get_buffer().connect('changed', self.on_text_changed)

        # Setup preview webview
        self.preview_webview = None

        self.scrolled_window = self.builder.get_object('editor_scrolledwindow')
        self.scrolled_window.get_style_context().add_class('uberwriter-scrolled-window')
        self.scrolled_window.add(self.text_view)
        self.editor_viewport = self.builder.get_object('editor_viewport')

        # Stats counter
        self.stats_counter = StatsCounter()

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
        self.paned_window = self.builder.get_object("main_pained")
        self.sidebar_box = self.builder.get_object("sidebar_box")
        self.sidebar = Sidebar(self)
        self.sidebar_box.hide()

        ###
        #   Search and replace initialization
        #   Same interface as Sidebar ;)
        ###
        self.searchreplace = SearchAndReplace(self, self.text_view)

        # Window resize
        self.window_resize(self)
        self.connect("configure-event", self.window_resize)
        self.connect("delete-event", self.on_delete_called)

        # Set current theme
        self.apply_current_theme()
        self.get_style_context().add_class('uberwriter-window')

    def apply_current_theme(self, *_):
        """Adjusts the window, CSD and preview for the current theme.
        """
        # Get current theme
        theme, changed = Theme.get_current_changed()
        if changed:
            # Set theme variant (dark/light)
            Gtk.Settings.get_default().set_property(
                "gtk-application-prefer-dark-theme",
                GLib.Variant("b", theme.is_dark))

            # Set theme css
            style_provider = Gtk.CssProvider()
            style_provider.load_from_path(theme.gtk_css_path)
            Gtk.StyleContext.add_provider_for_screen(
                self.get_screen(), style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

            # Reload preview if it exists
            self.reload_preview()

            # Redraw contents of window
            self.queue_draw()

    def update_stats_counts(self, stats):
        """Updates line and character counts.
        """

        (characters, words, sentences, (hours, minutes, seconds)) = stats
        self.char_count.set_text(str(characters))
        self.word_count.set_text(str(words))

    def on_text_changed(self, *_args):
        """called when the text changes, sets the self.did_change to true and
           updates the title and the counters to reflect that
        """

        if self.did_change is False:
            self.did_change = True
            title = self.get_title()
            self.set_headerbar_title("* " + title)

        self.buffer_modified_for_status_bar = True

        if self.status_bar_visible:
            self.stats_counter.count_stats(self.text_view.get_text(), self.update_stats_counts)

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

        focus_mode = state.get_boolean()
        self.text_view.set_focus_mode(focus_mode)
        if self.spell_checker:
            self.spell_checker._misspelled.set_property('underline', 0 if focus_mode else 4)
        self.text_view.grab_focus()

    def set_hemingway_mode(self, state):
        """toggle hemingwaymode
        """

        self.text_view.set_hemingway_mode(state.get_boolean())
        self.text_view.grab_focus()

    def window_resize(self, window, event=None):
        """set paddings dependant of the window size
        """

        # Ensure the window receiving the event is the one we care about, ie. the main window.
        # On Wayland (bug?), sub-windows such as the recents popover will also trigger this.
        if event and event.window != window.get_window():
            return

        # Adjust text editor width depending on window width, so that:
        # - The number of characters per line is adequate (http://webtypography.net/2.1.2)
        # - The number of characters stays constant while resizing the window / font
        # - There is enough text margin for MarkupBuffer to apply indents / negative margins
        #
        # TODO: Avoid hard-coding. Font size is clearer than unclear dimensions, but not ideal.
        w_width = event.width if event else window.get_allocation().width
        if w_width < 900:
            font_size = 14
            self.get_style_context().add_class("small")
            self.get_style_context().remove_class("large")

        elif w_width < 1280:
            font_size = 16
            self.get_style_context().remove_class("small")
            self.get_style_context().remove_class("large")

        else:
            font_size = 18
            self.get_style_context().remove_class("small")
            self.get_style_context().add_class("large")

        font_width = int(font_size * 1/1.6)  # Ratio specific to Fira Mono
        width = 67 * font_width - 1  # 66 characters
        horizontal_margin = 8 * font_width  # 8 characters
        width_request = width + horizontal_margin * 2

        if self.text_view.props.width_request != width_request:
            self.text_view.props.width_request = width_request
            self.text_view.set_left_margin(horizontal_margin)
            self.text_view.set_right_margin(horizontal_margin)
            self.scrolled_window.props.width_request = width_request

    # TODO: refactorizable
    def save_document(self, _widget=None, _data=None):
        """provide to the user a filechooser and save the document
           where he wants. Call set_headbar_title after that
        """

        if self.filename:
            LOGGER.info("saving")
            filename = self.filename
            file_to_save = codecs.open(filename, encoding="utf-8", mode='w')
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

            file_to_save = codecs.open(filename, encoding="utf-8", mode='w')
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

            file_to_save = codecs.open(filename, encoding="utf-8", mode='w')
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

    def menu_toggle_sidebar(self, _widget=None):
        """WIP
        """
        self.sidebar.toggle_sidebar()

    def toggle_spellcheck(self, state):
        """Enable/disable the autospellchecking

        Arguments:
            status {gtk bool} -- Desired status of the spellchecking
        """

        if state.get_boolean():
            try:
                self.spell_checker.enable()
            except:
                try:
                    self.spell_checker = SpellChecker(
                      self.text_view, locale.getdefaultlocale()[0],
                      collapse=False)
                    if self.auto_correct:
                        self.auto_correct.set_language(self.spell_checker.language)
                        self.spell_checker.connect_language_change(  # pylint: disable=no-member
                            self.auto_correct.set_language)
                except:
                    self.spell_checker = None
                    dialog = Gtk.MessageDialog(self,
                                            Gtk.DialogFlags.MODAL \
                                            | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                            Gtk.MessageType.INFO,
                                            Gtk.ButtonsType.NONE,
                                            _("You can not enable the Spell Checker.")
                                            )
                    dialog.format_secondary_text(
                        _("Please install 'hunspell' or 'aspell' dictionaries"
                        + " for your language from the software center."))
                    _response = dialog.run()
                return
            return
        else:
            try:
                self.spell_checker.disable()
            except:
                pass
        return

    def toggle_gradient_overlay(self, state):
        """Toggle the gradient overlay

        Arguments:
            state {gtk bool} -- Desired state of the gradient overlay (enabled/disabled)
        """

        if state.get_boolean():
            self.overlay_id = self.scrolled_window.connect_after("draw", self.draw_gradient)
        elif self.overlay_id:
            self.scrolled_window.disconnect(self.overlay_id)

    def toggle_preview(self, state):
        """Toggle the preview mode

        Arguments:
            state {gtk bool} -- Desired state of the preview mode (enabled/disabled)
        """

        if state.get_boolean():
            self.show_preview()
        else:
            self.show_text_editor()

        return True

    def show_text_editor(self):
        self.scrolled_window.remove(self.scrolled_window.get_child())
        self.scrolled_window.add(self.text_view)
        self.text_view.show()
        self.preview_webview.destroy()
        self.preview_webview = None
        self.queue_draw()

    def show_preview(self, loaded=False):
        if loaded:
            self.scrolled_window.remove(self.scrolled_window.get_child())
            self.scrolled_window.add(self.preview_webview)
            self.preview_webview.show()
            self.queue_draw()
        else:
            args = ['--standalone',
                    '--mathjax',
                    '--css=' + Theme.get_current().web_css_path,
                    '--lua-filter=' + helpers.get_script_path('relative_to_absolute.lua'),
                    '--lua-filter=' + helpers.get_script_path('task-list.lua')]
            output = helpers.pandoc_convert(self.text_view.get_text(), to="html5", args=args)

            if self.preview_webview is None:
                self.preview_webview = WebKit.WebView()
                self.preview_webview.get_settings().set_allow_universal_access_from_file_urls(True)

                # Show preview once the load is finished
                self.preview_webview.connect("load-changed", self.on_preview_load_change)

                # This saying that all links will be opened in default browser, \
                # but local files are opened in appropriate apps:
                self.preview_webview.connect("decide-policy", self.on_click_link)

            self.preview_webview.load_html(output, 'file://localhost/')

    def reload_preview(self):
        if self.preview_webview:
            self.show_preview()

    def load_file(self, filename=None):
        """Open File from command line or open / open recent etc."""
        if self.check_change() == Gtk.ResponseType.CANCEL:
            return

        if filename:
            if filename.startswith('file://'):
                filename = filename[7:]
            filename = urllib.parse.unquote_plus(filename)
            self.text_view.clear()
            try:
                if os.path.exists(filename):
                    current_file = codecs.open(filename, encoding="utf-8", mode='r')
                    self.text_view.set_text(current_file.read())
                    current_file.close()

                self.set_headerbar_title(os.path.basename(filename) + self.title_end)
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
            self.export.export(bytes(self.text_view.get_text(), "utf-8"))

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
                and self.text_view.props.has_focus): # pylint: disable=no-member
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
                self.stats_counter.count_stats(self.text_view.get_text(), self.update_stats_counts)
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
            self.stats_counter.count_stats(self.text_view.get_text(), self.update_stats_counts)

    def draw_gradient(self, _widget, cr):
        """draw fading gradient over the top and the bottom of the
           TextWindow
        """
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.ACTIVE)

        lg_top = cairo.LinearGradient(0, 0, 0, 35)  # pylint: disable=no-member
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

        lg_btm = cairo.LinearGradient(0, height - 35, 0, height)  # pylint: disable=no-member
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
        self.settings.set_value("open-file-path", GLib.Variant("s", base_path))

    def on_preview_load_change(self, webview, event):
        """swaps text editor with preview once the load is complete
        """
        if event == WebKit.LoadEvent.FINISHED:
            self.show_preview(loaded=True)

    def on_click_link(self, web_view, decision, _decision_type):
        """provide ability for self.webview to open links in default browser
        """
        if web_view.get_uri().startswith(("http://", "https://", "www.")):
            webbrowser.open(web_view.get_uri())
            decision.ignore()
            return True  # Don't let the event "bubble up"

    def on_destroy(self, _widget, _data=None):
        """Called when the Window is closing.
        """
        self.stats_counter.stop()
