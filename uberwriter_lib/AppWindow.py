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

import locale
import os
from locale import gettext as _
locale.textdomain('uberwriter')

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, GdkPixbuf

from . helpers import get_builder, show_uri, get_help_uri, get_media_path
from uberwriter import UberwriterWindow

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
        
        self.set_default_size(800,500)
        
        icon_file = get_media_path("uberwriter.svg")
        self.set_icon_from_file(icon_file)
        
        builder = get_builder('UberwriterWindow')
        new_object = builder.get_object("grid1")
        
        self.contents = new_object
        self.add(self.contents)
    
        self.finish_initializing(builder)
        
        return super().__init__(*args, **kwargs)
 

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

        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("help", None)
        action.connect("activate", self.on_help)
        self.add_action(action)
        
        action = Gio.SimpleAction.new("shortcuts", None)
        action.connect("activate", self.on_shortcuts)
        self.add_action(action)
        
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = get_builder('App_menu')
        self.set_app_menu(builder.get_object("app-menu"))


    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            # self.window = Window(application=self, title="UberWriter")
            self.window = UberwriterWindow.UberwriterWindow(application=self, title="UberWriter")
            self.window.load_file(sys.argv[1])

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")

        self.activate()
        return 0

    
    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.set_program_name("Uberwriter")
        about_dialog.set_version("TODO.beta")
        about_dialog.set_copyright("Copyright (C) 2018, Wolf Vollprecht")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_website("http://uberwriter.wolfvollprecht.de")
        about_dialog.set_authors(["Wolf Vollprecht", "Manuel Genovés"])
        
        logo_file = get_media_path("uberwriter.svg")
        logo = GdkPixbuf.Pixbuf.new_from_file(logo_file)
        
        about_dialog.set_logo(logo)
        
        about_dialog.present()
        
    def on_help(self, action, param):
        self.window.open_pandoc_markdown(self)
        
    def on_shortcuts(self, action, param):
        builder = get_builder('Shortcuts')
        builder.get_object("shortcuts").set_transient_for(self.window)
        builder.get_object("shortcuts").show()
        
    def on_quit(self, action, param):
        self.quit()

# ~ if __name__ == "__main__":
    # ~ app = Application()
    # ~ app.run(sys.argv)
