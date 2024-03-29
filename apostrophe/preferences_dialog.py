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

"""this dialog adjusts values in gsettings
"""
import webbrowser

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
logger = logging.getLogger('apostrophe')


class PreferencesDialog:

    __gtype_name__ = "PreferencesDialog"

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

    def __init__(self, settings):
        self.settings = settings
        self.builder = Gtk.Builder()
        self.builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/ui/Preferences.ui")

        self.autohide_headerbar_switch = self.builder.get_object(
            "autohide_headerbar_switch")
        self.autohide_headerbar_switch.set_active(
            self.settings.get_value("autohide-headerbar"))
        self.autohide_headerbar_switch.connect(
            "state-set", self.on_autohide_headerbar)

        self.spellcheck_switch = self.builder.get_object("spellcheck_switch")
        self.spellcheck_switch.set_active(
            self.settings.get_value("spellcheck"))
        self.spellcheck_switch.connect("state-set", self.on_spellcheck)

        input_format_store = Gtk.ListStore(int, str)
        input_format = self.settings.get_string("input-format")
        input_format_active = 0
        for i, fmt in enumerate(self.formats):
            input_format_store.append([i, fmt["name"]])
            if fmt["format"] == input_format:
                input_format_active = i
        self.input_format_combobox = self.builder.get_object(
            "input_format_combobox")
        self.input_format_combobox.set_model(input_format_store)
        input_format_renderer = Gtk.CellRendererText()
        self.input_format_combobox.pack_start(input_format_renderer, True)
        self.input_format_combobox.add_attribute(
            input_format_renderer, "text", 1)
        self.input_format_combobox.set_active(input_format_active)
        self.input_format_combobox.connect("changed", self.on_input_format)

        self.input_format_help_button = self.builder.get_object(
            "input_format_help_button")
        self.input_format_help_button.connect(
            'clicked', self.on_input_format_help)

    def show(self, window):
        preferences_window = self.builder.get_object("PreferencesWindow")
        preferences_window.set_application(window.get_application())
        preferences_window.set_transient_for(window)
        preferences_window.show()

    def on_autohide_headerbar(self, _, state):
        self.settings.set_boolean("autohide-headerbar", state)
        return False

    def on_spellcheck(self, _, state):
        self.settings.set_boolean("spellcheck", state)
        return False

    def on_input_format(self, combobox):
        fmt = self.formats[combobox.get_active()]
        self.settings.set_string("input-format", fmt["format"])

    def on_input_format_help(self, _):
        fmt = self.formats[self.input_format_combobox.get_active()]
        webbrowser.open(fmt["help"])
