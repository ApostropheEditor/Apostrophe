# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
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
### END LICENSE
"""Manages all the export operations and dialogs
"""


import logging
import os
from gettext import gettext as _

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from apostrophe import helpers
from apostrophe.theme import Theme

LOGGER = logging.getLogger('apostrophe')


class Export:
    """
    Manages all the export operations and dialogs
    """

    __gtype_name__ = "export_dialog"

    formats = [
        {
            "name": "LaTeX (pdf)",
            "ext": "pdf",
            "to": "pdf"
        },
        {
            "name": "LaTeX Beamer Slideshow (pdf)",
            "ext": "pdf",
            "to": "beamer"
        },
        {
            "name": "LaTeX (tex)",
            "ext": "tex",
            "to": "latex"
        },
        {
            "name": "LaTeX Beamer Slideshow (tex)",
            "ext": "tex",
            "to": "beamer"
        },
        {
            "name": "ConTeXt",
            "ext": "tex",
            "to": "context"
        },
        {
            "name": "HTML",
            "ext": "html",
            "to": "html"
        },
        {
            "name": "HTML and JavaScript Slideshow (Slidy)",
            "ext": "html",
            "to": "slidy"
        },
        {
            "name": "HTML and JavaScript Slideshow (Slideous)",
            "ext": "html",
            "to": "slideous"
        },
        {
            "name": "HTML5 and JavaScript Slideshow (DZSlides)",
            "ext": "html",
            "to": "dzslides"
        },
        {
            "name": "HTML5 and JavaScript Slideshow (reveal.js)",
            "ext": "html",
            "to": "revealjs"
        },
        {
            "name": "HTML and JavaScript Slideshow (S5)",
            "ext": "html",
            "to": "s5"
        },
        {
            "name": "Textile",
            "ext": "txt",
            "to": "textile"
        },
        {
            "name": "reStructuredText",
            "ext": "txt",
            "to": "rst"
        },
        {
            "name": "MediaWiki Markup",
            "ext": "txt",
            "to": "mediawiki"
        },
        {
            "name": "OpenDocument (xml)",
            "ext": "xml",
            "to": "opendocument"
        },
        {
            "name": "OpenDocument (texi)",
            "ext": "texi",
            "to": "texinfo"
        },
        {
            "name": "LibreOffice Text Document",
            "ext": "odt",
            "to": "odt"
        },
        {
            "name": "Microsoft Word (docx)",
            "ext": "docx",
            "to": "docx"
        },
        {
            "name": "Rich Text Format",
            "ext": "rtf",
            "to": "rtf"
        },
        {
            "name": "Groff Man",
            "ext": "man",
            "to": "man"
        },
        {
            "name": "EPUB v3",
            "ext": "epub",
            "to": "epub"
        }
    ]

    def __init__(self, filename, export_format, text):
        """Set up the export dialog"""

        self.export_menu = {
            "pdf":
            {
                "extension": "pdf",
                "name": "PDF",
                "mimetype": "application/pdf",
                "dialog": self.regular_export_dialog
            },
            "html":
            {
                "extension": "html",
                "name": "HTML",
                "mimetype": "text/html",
                "dialog": self.regular_export_dialog
            },
            "odt":
            {
                "extension": "odt",
                "name": "ODT",
                "mimetype": "application/vnd.oasis.opendocument.text",
                "dialog": self.regular_export_dialog
            },
            "advanced":
            {
                "extension": "",
                "name": "",
                "mimetype": "",
                "dialog": self.advanced_export_dialog
            }
        }

        self.filename = filename or _("Untitled document.md")
        self.export_format = export_format

        self.dialog = self.export_menu[export_format]["dialog"]()

        response = self.dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            try:
                self.export(export_format, text)
            except (NotADirectoryError, RuntimeError) as e:
                dialog = Gtk.MessageDialog(None,
                                       Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CLOSE,
                                       _("An error happened while trying to export:\n\n{err_msg}")
                                           .format(err_msg= str(e).encode().decode("unicode-escape"))
                                       )
                dialog.run()
                dialog.destroy()
        
        self.dialog.destroy()

    def regular_export_dialog(self):
        texlive_installed = helpers.exist_executable("pdftex")

        if (self.export_menu[self.export_format]["extension"] == "pdf" and
           not texlive_installed):
            dialog = Gtk.MessageDialog(None,
                            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            Gtk.MessageType.INFO,
                            Gtk.ButtonsType.CLOSE,
                            _("Oh, no!")
                            )
            
            dialog.props.secondary_text = _("Seems that you don’t have TexLive installed.\n" +
                                            disabled_text())
        else:
            dialog = Gtk.FileChooserNative.new(_("Export"),
                                                None,
                                                Gtk.FileChooserAction.SAVE,
                                                _("Export to %s") % 
                                                self.export_menu[self.export_format]["extension"],
                                                _("Cancel"))
            dialog_filter = Gtk.FileFilter.new()
            dialog_filter.set_name(self.export_menu[self.export_format]["name"])
            dialog_filter.add_mime_type(self.export_menu[self.export_format]["mimetype"])
            dialog.add_filter(dialog_filter)
            dialog.set_do_overwrite_confirmation(True)
            dialog.set_current_folder(os.path.dirname(self.filename))
            dialog.set_current_name(os.path.basename(self.filename)[:-2] +
                                    self.export_menu[self.export_format]["extension"])

        return dialog

    def advanced_export_dialog(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_resource(
            "/org/gnome/gitlab/somas/Apostrophe/ui/Export.ui")

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

        self.adv_export_folder = self.builder.get_object("advanced")

        self.adv_export_name = self.builder.get_object("advanced_export_name")
        self.adv_export_name.set_text(os.path.basename(self.filename)[:-3])
        self.paper_size = self.builder.get_object("combobox_paper_size")

        return self.builder.get_object("Export")

    def export(self, export_type, text=""):
        """Export the given text using the specified format.
        For advanced export, this includes special flags for the enabled options.

        Keyword Arguments:
            text {str} -- Text to export (default: {""})
        """

        args = []
        if export_type == "advanced":
            filename = self.adv_export_name.get_text()

            # TODO: use walrust operator
            output_uri = self.adv_export_folder.get_uri()
            if output_uri:
                output_dir = GLib.filename_from_uri(output_uri)[0]
            else:
                raise NotADirectoryError(_("A folder must be selected before proceeding"))
            basename = os.path.basename(filename)

            fmt = self.formats[self.format_field.get_active()]
            to = fmt["to"]
            ext = fmt["ext"]

            if self.builder.get_object("html5").get_active() and to == "html":
                to = "html5"
            if self.builder.get_object("smart").get_active():
                to += "+smart"

            args.extend(self.get_advanced_arguments(to, ext))

        else:
            args = [
                "--variable=papersize:a4"
            ]
            filename = self.dialog.get_filename()
            if filename.endswith("." + export_type):
                filename = filename[:-len(export_type)-1]
            output_dir = os.path.abspath(os.path.join(filename, os.path.pardir))
            basename = os.path.basename(filename)

            to = export_type
            ext = export_type

            if export_type == "html":
                to = "html5"
                args.append("--self-contained")
                args.append("--css=%s" % Theme.get_current().web_css_path)
                args.append("--mathjax")
                args.append("--lua-filter=%s" % helpers.get_script_path('relative_to_absolute.lua'))
                args.append("--lua-filter=%s" % helpers.get_script_path('task-list.lua'))


        helpers.pandoc_convert(
            text, to=to, args=args,
            outputfile="%s/%s.%s" % (output_dir, basename, ext))

    def get_advanced_arguments(self, to_fmt, ext_fmt):
        """Retrieve a list of the selected advanced arguments

        For most of the advanced option checkboxes, returns a list
        of the related pandoc flags

        Arguments:
            basename {str} -- the name of the file
            to_fmt {str} -- the format of the export
            ext_fmt {str} -- the extension of the export

        Returns:
            list of {str} -- related pandoc flags
        """

        highlight_style = self.builder.get_object("highlight_style").get_active_text()

        conditions = [
            {
                "condition": to_fmt == "pdf",
                "yes": "--variable=papersize:" + self.get_paper_size(),
                "no": None
            },
            {
                "condition": (self.get_paper_size() == "a4" and (to_fmt in ("odt", "docx"))),
                "yes": "--reference-doc=" + helpers.get_reference_files_path('reference-a4.' + to_fmt),
                "no": None
            },
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

    def get_paper_size(self):
        paper_size = self.paper_size.get_active_text()

        paper_formats = {
            "A4": "a4",
            "US Letter": "letter"
        }

        return paper_formats[paper_size]

def disabled_text():
    """Return the TexLive installation instructions

    Returns:
        {str} -- [TexLive installation instructions]
    """

    if os.path.isfile("/.flatpak-info"):
        text = _("Please, install the TexLive extension from Gnome Software or running\n")\
                + ("flatpak install flathub org.gnome.gitlab.somas.Apostrophe.Plugin.TexLive")
    else:
        text = _("Please, install TexLive from your distribuiton repositories")
    return text
