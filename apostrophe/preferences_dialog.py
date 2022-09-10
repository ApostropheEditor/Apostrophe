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

"""this dialog adjusts values in gsettings
"""
import webbrowser

import gi

from apostrophe import helpers

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Adw, Gio, GObject
import logging
logger = logging.getLogger('apostrophe')

from apostrophe.settings import Settings

class InputFormat(GObject.Object):
    __gtype_name__ = "InputFormat"

    name = GObject.Property(type=str)
    format = GObject.Property(type=str)
    help = GObject.Property(type=str)

    def __init__(self, name, format, help, **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.format: str = format
        self.help: str = help

@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/Preferences.ui')
class ApostrophePreferencesDialog(Adw.PreferencesWindow):

    __gtype_name__ = "ApostrophePreferencesDialog"

    formats = [
        {
            "name": "Pandoc's Markdown",
            "format": "markdown",
            "help": "https://pandoc.org/MANUAL.html#pandocs-markdown"
        },
        {
            "name": "CommonMark",
            "format": "commonmark",
            "help": "https://commonmark.org"
        },
        {
            "name": "GitHub Flavored Markdown",
            "format": "gfm",
            "help": "https://help.github.com/en/categories/writing-on-github"
        },
        {
            "name": "MultiMarkdown",
            "format": "markdown_mmd",
            "help": "https://fletcherpenney.net/multimarkdown"
        },
        {
            "name": "Plain Markdown",
            "format": "markdown_strict",
            "help": "https://daringfireball.net/projects/markdown"
        }
    ]

    autohide_headerbar_switch = Gtk.Template.Child()
    spellcheck_switch = Gtk.Template.Child()
    input_format_comborow = Gtk.Template.Child()
    bigger_text_switch = Gtk.Template.Child()

    settings = Settings.new()

    def __init__(self):
        super().__init__()
        input_formats = Gio.ListStore.new(InputFormat)

        for i, format in enumerate(self.formats):
            input_formats.append(InputFormat(format["name"],
                                             format["format"],
                                             format["help"]))
            if (format["format"] == self.settings.get_string("input-format")):
                current_format = i

        self.input_format_comborow.set_model(input_formats)

        if current_format:
            self.input_format_comborow.set_selected_index(current_format)

        self.settings.bind("autohide-headerbar",
                           self.autohide_headerbar_switch,
                           "active",
                           Gio.SettingsBindFlags.DEFAULT)

        self.settings.bind("spellcheck",
                           self.spellcheck_switch,
                           "active",
                           Gio.SettingsBindFlags.DEFAULT)

        self.settings.bind("bigger-text",
                           self.bigger_text_switch,
                           "active",
                           Gio.SettingsBindFlags.DEFAULT)

    @Gtk.Template.Callback()
    def on_input_format(self, _widget, _index):
        fmt = self.input_format_comborow.get_selected_item()
        self.settings.set_string("input-format", fmt.format)

    @Gtk.Template.Callback()
    def on_input_format_help(self, _):
        fmt = self.input_format_comborow.get_selected_item()
        webbrowser.open(fmt.help)
