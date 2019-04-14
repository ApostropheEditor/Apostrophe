# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
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
### END LICENSE
"""Manages all the export operations and dialogs
"""


import logging
import os
from gettext import gettext as _

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from uberwriter import helpers
from uberwriter.theme import Theme
from uberwriter.helpers import get_builder

LOGGER = logging.getLogger('uberwriter')


class Export:
    """
    Manages all the export operations and dialogs
    """

    __gtype_name__ = "export_dialog"

    formats = [
        {
            "name": "LaTeX Source",
            "ext": "tex",
            "to": "latex"
        },
        {
            "name": "LaTeX PDF",
            "ext": "pdf",
            "to": "pdf"
        },
        {
            "name": "LaTeX beamer slide show Source .tex",
            "ext": "tex",
            "to": "beamer"
        },
        {
            "name": "LaTeX beamer slide show PDF",
            "ext": "pdf",
            "to": "beamer"
        },
        {
            "name": "HTML",
            "ext": "html",
            "to": "html5"
        },
        {
            "name": "Textile",
            "ext": "txt",
            "to": "textile"
        },
        {
            "name": "OpenOffice text document",
            "ext": "odt",
            "to": "odt"
        },
        {
            "name": "Word docx",
            "ext": "docx",
            "to": "docx"
        },
        {
            "name": "reStructuredText txt",
            "ext": "txt",
            "to": "rst"
        },
        {
            "name": "ConTeXt tex",
            "ext": "tex",
            "to": "context"
        },
        {
            "name": "groff man",
            "ext": "man",
            "to": "man"
        },
        {
            "name": "MediaWiki markup",
            "ext": "txt",
            "to": "mediawiki"
        },
        {
            "name": "OpenDocument XML",
            "ext": "xml",
            "to": "opendocument"
        },
        {
            "name": "OpenDocument XML",
            "ext": "texi",
            "to": "texinfo"
        },
        {
            "name": "Slidy HTML and javascript slide show",
            "ext": "html",
            "to": "slidy"
        },
        {
            "name": "Slideous HTML and javascript slide show",
            "ext": "html",
            "to": "slideous"
        },
        {
            "name": "HTML5 + javascript slide show",
            "ext": "html",
            "to": "dzslides"
        },
        {
            "name": "S5 HTML and javascript slide show",
            "ext": "html",
            "to": "s5"
        },
        {
            "name": "EPub electronic publication",
            "ext": "epub",
            "to": "epub"
        },
        {
            "name": "RTF Rich Text Format",
            "ext": "rtf",
            "to": "rtf"
        }
    ]

    def __init__(self, filename):
        """Set up the about dialog"""
        self.builder = get_builder('Export')
        self.dialog = self.builder.get_object("Export")
        self.stack = self.builder.get_object("export_stack")
        self.stack_switcher = self.builder.get_object("format_switcher")

        stack_pdf_disabled = self.builder.get_object("pdf_disabled")
        filename = filename or _("Untitled document.md")

        self.filechoosers = {export_format: self.stack.get_child_by_name(export_format)
                             for export_format in ["pdf", "html", "odt", "advanced"]}
        for export_format, filechooser in self.filechoosers.items():
            filechooser.set_do_overwrite_confirmation(True)
            filechooser.set_current_folder(os.path.dirname(filename))
            if export_format == "advanced":
                self.adv_export_name = self.builder.get_object("advanced_export_name")
                self.adv_export_name.set_text(os.path.basename(filename)[:-3])
            else:
                filechooser.set_current_name(os.path.basename(filename)[:-2] + export_format)

        # Disable pdf if Texlive not installed
        texlive_installed = helpers.exist_executable("pdftex")

        if not texlive_installed:
            self.filechoosers["pdf"].set_visible(False)
            stack_pdf_disabled.set_visible(True)
            stack_pdf_disabled.set_text(disabled_text())
            stack_pdf_disabled.set_justify(Gtk.Justification.CENTER)
            self.stack.connect('notify', self.allow_export, 'visible_child_name')

        self.builder.get_object("highlight_style").set_active(0)

        self.builder.get_object("css_filechooser").set_uri(
            helpers.path_to_file(Theme.get_current().web_css_path))

        format_store = Gtk.ListStore(int, str)
        for i, fmt in enumerate(self.formats):
            format_store.append([i, fmt["name"]])
        self.format_field = self.builder.get_object('choose_format')
        self.format_field.set_model(format_store)

        format_renderer = Gtk.CellRendererText()
        self.format_field.pack_start(format_renderer, True)
        self.format_field.add_attribute(format_renderer, "text", 1)
        self.format_field.set_active(0)

    def export(self, text=""):
        """Export the given text using the specified format.
        For advanced export, this includes special flags for the enabled options.

        Keyword Arguments:
            text {str} -- Text to export (default: {""})
        """

        export_type = self.stack.get_visible_child_name()
        args = []
        if export_type == "advanced":
            filename = self.adv_export_name.get_text()
            output_dir = os.path.abspath(self.filechoosers["advanced"].get_current_folder())
            basename = os.path.basename(filename)

            fmt = self.formats[self.format_field.get_active()]
            to = fmt["to"]
            ext = fmt["ext"]

            if self.builder.get_object("html5").get_active() and to == "html":
                to = "html5"
            if self.builder.get_object("smart").get_active():
                to += "+smart"

            args.extend(self.get_advanced_arguments())

        else:
            filename = self.filechoosers[export_type].get_filename()
            if filename.endswith("." + export_type):
                filename = filename[:-len(export_type)-1]
            output_dir = os.path.abspath(os.path.join(filename, os.path.pardir))
            basename = os.path.basename(filename)

            to = export_type
            ext = export_type

            if export_type == "html":
                to = "html5"
                args.append("--standalone")
                args.append("--css=%s" % Theme.get_current().web_css_path)
                args.append("--mathjax")
                args.append("--lua-filter=%s" % helpers.get_script_path('relative_to_absolute.lua'))
                args.append("--lua-filter=%s" % helpers.get_script_path('task-list.lua'))

        helpers.pandoc_convert(
            text, to=to, args=args,
            outputfile="%s/%s.%s" % (output_dir, basename, ext))

    def get_advanced_arguments(self):
        """Retrieve a list of the selected advanced arguments

        For most of the advanced option checkboxes, returns a list
        of the related pandoc flags

        Arguments:
            basename {str} -- the name of the file

        Returns:
            list of {str} -- related pandoc flags
        """

        highlight_style = self.builder.get_object("highlight_style").get_active_text()

        conditions = [
            {
                "condition": self.builder.get_object("toc").get_active(),
                "yes": "--toc",
                "no": None
            },
            {
                "condition": self.builder.get_object("highlight").get_active(),
                "yes": "--highlight-style=%s" % highlight_style,
                "no": "--no-highlight"
            },
            {
                "condition": self.builder.get_object("standalone").get_active(),
                "yes": "--standalone",
                "no": None
            },
            {
                "condition": self.builder.get_object("number_sections").get_active(),
                "yes": "--number-sections",
                "no": None
            },
            {
                "condition": self.builder.get_object("strict").get_active(),
                "yes": "--strict",
                "no": None
            },
            {
                "condition": self.builder.get_object("incremental").get_active(),
                "yes": "--incremental",
                "no": None
            },
            {
                "condition": self.builder.get_object("self_contained").get_active(),
                "yes": "--self-contained",
                "no": None
            }
        ]

        args = []

        args.extend([c["yes"] if c["condition"] else c["no"] for c in conditions])

        args = list(filter(lambda arg: arg is not None, args))

        css_uri = self.builder.get_object("css_filechooser").get_uri()
        if css_uri:
            if css_uri.startswith("file://"):
                css_uri = css_uri[7:]
            args.append("--css=%s" % css_uri)

        bib_uri = self.builder.get_object("bib_filechooser").get_uri()
        if bib_uri:
            if bib_uri.startswith("file://"):
                bib_uri = bib_uri[7:]
            args.append("--bibliography=%s" % bib_uri)

        return args

    def allow_export(self, widget, data, signal):
        """Disable export button if the visible child is "pdf_disabled"
        """

        del widget, data, signal

        export_btn = self.builder.get_object("export_btn")

        if self.stack.get_visible_child_name() == "pdf_disabled":
            export_btn.set_sensitive(False)
        else:
            export_btn.set_sensitive(True)

def disabled_text():
    """Return the TexLive installation instructions

    Returns:
        {str} -- [TexLive installation instructions]
    """

    if os.path.isfile("/.flatpak-info"):
        text = _("Please, install the TexLive extension from Gnome Software or running\n")\
                + ("flatpak install flathub de.wolfvollprecht.UberWriter.Plugin.TexLive")
    else:
        text = _("Please, install TexLive from your distribuiton repositories")
    return text
