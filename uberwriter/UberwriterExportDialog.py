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


import os
import subprocess
import logging
# import gettext

from gettext import gettext as _
from gi.repository import Gtk

from uberwriter_lib import helpers
from uberwriter_lib.helpers import get_builder

LOGGER = logging.getLogger('uberwriter')

class Export:
    """
    Manages all the export operations and dialogs
    """

    __gtype_name__ = "UberwriterExportDialog"

    def __init__(self, filename):
        """Set up the about dialog"""
        self.builder = get_builder('Export')
        self.dialog = self.builder.get_object("Export")
        self.stack = self.builder.get_object("export_stack")
        self.stack_switcher = self.builder.get_object("format_switcher")

        stack_pdf_disabled = self.builder.get_object("pdf_disabled")
        filename = filename or _("Untitled document.md")

        self.filechoosers = {export_format:self.stack.get_child_by_name(export_format)\
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

        format_store = Gtk.ListStore(int, str)
        for fmt_id in self.formats_dict:
            format_store.append([fmt_id, self.formats_dict[fmt_id]["name"]])
        self.format_field = self.builder.get_object('choose_format')
        self.format_field.set_model(format_store)

        format_renderer = Gtk.CellRendererText()
        self.format_field.pack_start(format_renderer, True)
        self.format_field.add_attribute(format_renderer, "text", 1)
        self.format_field.set_active(0)

    formats_dict = {
        1: {
            "name": "LaTeX Source",
            "ext": "tex",
            "to": "latex"
        },
        2: {
            "name": "LaTeX PDF",
            "ext": "pdf",
            "to": "pdf"
        },
        3: {
            "name": "LaTeX beamer slide show Source .tex",
            "ext": "tex",
            "to": "beamer"
        },
        4: {
            "name": "LaTeX beamer slide show PDF",
            "ext": "pdf",
            "to": "beamer"
        },
        5: {
            "name": "HTML",
            "ext": "html",
            "to": "html"
        },
        6: {
            "name": "Textile",
            "ext": "txt",
            "to": "textile"
        },
        7: {
            "name": "OpenOffice text document",
            "ext": "odt",
            "to": "odt"
        },
        8: {
            "name": "Word docx",
            "ext": "docx",
            "to": "docx"
        },
        9: {
            "name": "reStructuredText txt",
            "ext": "txt",
            "to": "rst"
        },
        10: {
            "name": "ConTeXt tex",
            "ext": "tex",
            "to": "context"
        },
        11: {
            "name": "groff man",
            "ext": "man",
            "to": "man"
        },
        12: {
            "name": "MediaWiki markup",
            "ext": "txt",
            "to": "mediawiki"
        },
        13: {
            "name": "OpenDocument XML",
            "ext": "xml",
            "to": "opendocument"
        },
        14: {
            "name": "OpenDocument XML",
            "ext": "texi",
            "to": "texinfo"
        },
        15: {
            "name": "Slidy HTML and javascript slide show",
            "ext": "html",
            "to": "slidy"
        },
        16: {
            "name": "Slideous HTML and javascript slide show",
            "ext": "html",
            "to": "slideous"
        },
        17: {
            "name": "HTML5 + javascript slide show",
            "ext": "html",
            "to": "dzslides"
        },
        18: {
            "name": "S5 HTML and javascript slide show",
            "ext": "html",
            "to": "s5"
        },
        19: {
            "name": "EPub electronic publication",
            "ext": "epub",
            "to": "epub"
        },
        20: {
            "name": "RTF Rich Text Format",
            "ext": "rtf",
            "to": "rtf"
        }

    }

    def export(self, text=""):
        """Export to pdf, html or odt the given text

        Keyword Arguments:
            text {str} -- Text to export (default: {""})
        """

        export_format = self.stack.get_visible_child_name()

        if export_format == "advanced":
            self.advanced_export(text)
        else:
            filename = self.filechoosers[export_format].get_filename()
            if filename.endswith("." + export_format):
                filename = filename[:-len(export_format)-1]

            output_dir = os.path.abspath(os.path.join(filename, os.path.pardir))
            basename = os.path.basename(filename)

            args = ['pandoc', '--from=markdown', '-s']

            if export_format == "pdf":
                args.append("-o%s.pdf" % basename)

            elif export_format == "odt":
                args.append("-o%s.odt" % basename)

            elif export_format == "html":
                css = helpers.get_media_file('github-md.css')
                relativize = helpers.get_script_path('relative_to_absolute.lua')
                task_list = helpers.get_script_path('task-list.lua')
                args.append("-c%s" % css)
                args.append("-o%s.html" % basename)
                args.append("--mathjax")
                args.append("--lua-filter=" + relativize)
                args.append("--lua-filter=" + task_list)

            proc = subprocess.Popen(args, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, cwd=output_dir)
            _ = proc.communicate(text)[0]

    def advanced_export(self, text=""):
        """Export the given text to special formats with the enabled flags

        Keyword Arguments:
            text {str} -- The text to export (default: {""})
        """

        filename = self.adv_export_name.get_text()
        output_dir = os.path.abspath(self.filechoosers["advanced"].get_current_folder())
        basename = os.path.basename(filename)
        args = self.set_arguments(basename)

        LOGGER.info(args)

        proc = subprocess.Popen(args, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, cwd=output_dir)
        _ = proc.communicate(text)[0]

    def set_arguments(self, basename):
        """Retrieve a list of the selected arguments

        For most of the advanced option checkboxes, returns a list
        of the related pandoc flags

        Arguments:
            basename {str} -- the name of the file

        Returns:
            list of {str} -- related pandoc flags
        """

        highlight_style = self.builder.get_object("highlight_style").get_active_text()

        conditions_dict = {
            1: {
                "condition": self.builder.get_object("toc").get_active(),
                "yes": "--toc",
                "no": None
            },
            2: {
                "condition": self.builder.get_object("highlight").get_active(),
                "yes": "--highlight-style=%s" % highlight_style,
                "no": "--no-highlight"
            },
            3: {
                "condition": self.builder.get_object("standalone").get_active(),
                "yes": "--standalone",
                "no": None
            },
            4: {
                "condition": self.builder.get_object("number_sections").get_active(),
                "yes": "--number-sections",
                "no": None
            },
            5: {
                "condition": self.builder.get_object("strict").get_active(),
                "yes": "--strict",
                "no": None
            },
            6: {
                "condition": self.builder.get_object("incremental").get_active(),
                "yes": "--incremental",
                "no": None
            },
            7: {
                "condition": self.builder.get_object("self_contained").get_active(),
                "yes": "--self-contained",
                "no": None
            }
        }

        tree_iter = self.format_field.get_active_iter()
        if tree_iter is not None:
            model = self.format_field.get_model()
            row_id, _ = model[tree_iter][:2]

        fmt = self.formats_dict[row_id]

        args = ['pandoc', '--from=markdown']

        extension = "--to=%s" % fmt["to"]

        if basename.endswith("." + fmt["ext"]):
            output_file = "--output=%s" % basename
        else:
            output_file = "--output=%s.%s" % (basename, fmt["ext"])

        args.extend([conditions_dict[c_id]["yes"]\
                    if conditions_dict[c_id]["condition"]\
                    else conditions_dict[c_id]["no"]\
                    for c_id in conditions_dict])

        args = list(filter(None, args))

        if self.builder.get_object("html5").get_active():
            if fmt["to"] == "html":
                extension = "--to=%s" % "html5"

        if self.builder.get_object("smart").get_active():
            extension += '+smart'
        else:
            extension += '-smart'

        if fmt["to"] != "pdf":
            args.append(extension)

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

        args.append(output_file)

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
