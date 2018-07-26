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
# with this program.  If not, see &lt;http://www.gnu.org/licenses/&gt;.

import sys
import argparse

import gettext
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, GdkPixbuf

from . helpers import get_builder, show_uri, get_help_uri, get_media_path
from uberwriter import UberwriterWindow
from uberwriter.Settings import Settings
from uberwriter_lib import set_up_logging
from uberwriter_lib.PreferencesDialog import PreferencesDialog

from gettext import gettext as _

class Window(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                           GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
                            lambda obj, pspec: max_action.set_state(
                                               GLib.Variant.new_boolean(obj.props.is_maximized)))
        
        self.set_default_size(850,500)
        
        icon_file = get_media_path("uberwriter.svg")
        self.set_icon_from_file(icon_file)
        
        builder = get_builder('UberwriterWindow')
        new_object = builder.get_object("FullscreenOverlay")
        
        self.contents = new_object
        self.add(self.contents)
    
        self.finish_initializing(builder)

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()
    
    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initializing should be called after parsing the UI definition
        and creating a UberwriterWindow object with it in order to finish
        initializing the start of the new UberwriterWindow instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self, True)
        self.PreferencesDialog = None # class
        self.preferences_dialog = None # instance
        self.AboutDialog = None # class

        
        # self.settings = Gio.Settings("net.launchpad.uberwriter")
        # self.settings.connect('changed', self.on_preferences_changed)

        # Optional application indicator support
        # Run 'quickly add indicator' to get started.
        # More information:
        #  http://owaislone.org/quickly-add-indicator/
        #  https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators
        try:
            from uberwriter import indicator
            # self is passed so methods of this class can be called from indicator.py
            # Comment this next line out to disable appindicator
            self.indicator = indicator.new_application_indicator(self)
        except ImportError:
            pass
            

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="de.wolfvollprecht.UberWriter",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None
        self.settings = Settings.new()
        
    def do_startup(self):
        Gtk.Application.do_startup(self)

        '''Actions'''

        action = Gio.SimpleAction.new("help", None)
        action.connect("activate", self.on_help)
        self.add_action(action)
        
        action = Gio.SimpleAction.new("shortcuts", None)
        action.connect("activate", self.on_shortcuts)
        self.add_action(action)
        
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("translate", None)
        action.connect("activate", self.on_translate)
        self.add_action(action)

        action = Gio.SimpleAction.new("donate", None)
        action.connect("activate", self.on_donate)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        set_dark_mode = self.settings.get_value("dark-mode")
        action = Gio.SimpleAction.new_stateful("dark_mode",
                                                None,
                                                GLib.Variant.new_boolean(set_dark_mode))
        action.connect("change-state", self.on_dark_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("focus_mode",
                                                None,
                                                GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_focus_mode)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("fullscreen",
                                                None,
                                                GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_fullscreen)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("preview",
                                                None,
                                                GLib.Variant.new_boolean(False))
        action.connect("change-state", self.on_preview)
        self.add_action(action)

        action = Gio.SimpleAction.new("search", None)
        action.connect("activate", self.on_search)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful("spellcheck",
                                                None,
                                                GLib.Variant.new_boolean(True))
        action.connect("change-state", self.on_spellcheck)
        self.add_action(action)

        '''Menu Actions'''

        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.on_new)
        self.add_action(action)

        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.on_open)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_recent", None)
        action.connect("activate", self.on_open_recent)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_examples", None)
        action.connect("activate", self.on_example)
        self.add_action(action)

        action = Gio.SimpleAction.new("save", None)
        action.connect("activate", self.on_save)
        self.add_action(action)

        action = Gio.SimpleAction.new("save_as", None)
        action.connect("activate", self.on_save_as)
        self.add_action(action)

        action = Gio.SimpleAction.new("export", None)
        action.connect("activate", self.on_export)
        self.add_action(action)

        action = Gio.SimpleAction.new("HTML_copy", None)
        action.connect("activate", self.on_html_copy)
        self.add_action(action)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_preferences)
        self.add_action(action)


        '''Shortcuts'''

        self.set_accels_for_action("app.focus_mode",["<Ctl>d"])
        self.set_accels_for_action("app.fullscreen",["F11"])
        self.set_accels_for_action("app.preview",["<Ctl>p"])
        self.set_accels_for_action("app.search",["<Ctl>f"])
        self.set_accels_for_action("app.spellcheck",["F7"])

        self.set_accels_for_action("app.new",["<Ctl>n"])
        self.set_accels_for_action("app.open",["<Ctl>o"])
        self.set_accels_for_action("app.save",["<Ctl>s"])
        self.set_accels_for_action("app.save_as",["<Ctl><shift>s"])


    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            # self.window = Window(application=self, title="UberWriter")
            self.window = UberwriterWindow.UberwriterWindow(application=self, title="UberWriter")
            if len(self.args) > 0:
              self.window.load_file(self.args[0])
            if self.options.experimental_features:
                self.window.use_experimental_features(True)
        

        self.window.present()

    def do_command_line(self, command_line):
      
        """Support for command line options"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v", "--verbose", action="count", dest="verbose",
            help=_("Show debug messages (-vv debugs uberwriter_lib also)"))
        parser.add_argument(
            "-e", "--experimental-features", help=_("Use experimental features"),
            action='store_true'
            )
        (self.options, self.args) = parser.parse_known_args()

        set_up_logging(self.options)
        
        self.activate()
        return 0

    
    def on_about(self, action, param):
        builder = get_builder('About')
        about_dialog = builder.get_object("AboutDialog")
        about_dialog.set_transient_for(self.window)

        logo_file = get_media_path("uberwriter.svg")
        logo = GdkPixbuf.Pixbuf.new_from_file(logo_file)
        
        about_dialog.set_logo(logo)
        
        about_dialog.present()
        
    def on_help(self, action, param):
        self.window.open_pandoc_markdown(self)

    def on_translate(self, action, param):
        self.window.open_translation()

    def on_donate(self, action, param):
        self.window.open_donation()
        
    def on_shortcuts(self, action, param):
        builder = get_builder('Shortcuts')
        builder.get_object("shortcuts").set_transient_for(self.window)
        builder.get_object("shortcuts").show()

    def on_dark_mode(self, action, value):
        action.set_state(value)
        self.settings.set_value("dark-mode",
                                 GLib.Variant("b", value))
        self.window.toggle_dark_mode(value)

        #this changes the headerbar theme accordingly
        self.dark_setting = Gtk.Settings.get_default()
        self.dark_setting.set_property("gtk-application-prefer-dark-theme", value)

    def on_focus_mode(self, action, value):
        action.set_state(value)
        self.window.set_focusmode(value)

    def on_fullscreen(self, action, value):
        action.set_state(value)
        self.window.toggle_fullscreen(value)

    def on_preview(self, action, value):
        action.set_state(value)
        self.window.toggle_preview(value)

    def on_search(self, action, value):
        self.window.open_search_and_replace()

    def on_spellcheck(self, action, value):
        action.set_state(value)
        self.window.toggle_spellcheck(value)

    def on_new(self, action, value):
        self.window.new_document()

    def on_open(self, action, value):
        self.window.open_document()
    
    def on_open_recent(self, action, value):
        pass
    
    def on_example(self, action, value):
        self.window.open_uberwriter_markdown()
    
    def on_save(self, action, value):
        self.window.save_document()
    
    def on_save_as(self, action, value):
        self.window.save_document_as()
    
    def on_export(self, action, value):
        self.window.open_advanced_export()
    
    def on_html_copy(self, action, value):
        self.window.copy_html_to_clipboard()

    def on_preferences(self, action, value):
        PreferencesWindow = PreferencesDialog()
        PreferencesWindow.set_application(self)
        PreferencesWindow.set_transient_for(self.window)
        PreferencesWindow.show()
   
    def on_quit(self, action, param):
        self.quit()

# ~ if __name__ == "__main__":
    # ~ app = Application()
    # ~ app.run(sys.argv)
