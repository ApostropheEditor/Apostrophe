import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from . helpers import get_builder, show_uri, get_help_uri

class UberwriterWindow(Gtk.ApplicationWindow):

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
        
        self.default_width = 800
        self.defaul_height = 500
        self.set_icon_from_file("data/media/uberwriter.svg")
        
        builder = get_builder('UberwriterWindow')
        new_object = builder.get_object("grid1")
        
         
        self.builder = builder
        self.ui = builder.get_ui(self, True)
        self.PreferencesDialog = None # class
        self.preferences_dialog = None # instance
        self.AboutDialog = None # class
                
        self.contents = new_object
        self.add(self.contents)
        
        self.finish_initializing(self.builder)
       

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()

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

        # ~ action = Gio.SimpleAction.new("about", None)
        # ~ action.connect("activate", self.on_about)
        # ~ self.add_action(action)

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
            self.window = UberwriterWindow(application=self, title="UberWriter")

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")

        self.activate()
        return 0

    # TODO
    # ~ def on_about(self, action, param):
        # ~ about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        # ~ about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
