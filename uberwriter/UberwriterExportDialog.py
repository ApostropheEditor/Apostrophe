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
 
from gi.repository import Gtk
import os
import subprocess
import gettext

from gettext import gettext as _

import logging
logger = logging.getLogger('uberwriter')

from uberwriter_lib import helpers
from uberwriter_lib.helpers import get_builder

class Export:
    __gtype_name__ = "UberwriterExportDialog"

    def __init__(self, filename):
        """Set up the about dialog"""
        self.builder = get_builder('Export')
        self.Dialog = self.builder.get_object("Export")
        self.stack = self.builder.get_object("export_stack")
        self.filename = filename or _("Untitled document.md")

        # TODO: Disable pdf if Texlive not installed

        self.filechoosers = {format:self.stack.get_child_by_name(format)\
                   for format in ["pdf", "html", "odt", "advanced"]}
        for format, filechooser in self.filechoosers.items():
            filechooser.set_do_overwrite_confirmation(True)
            filechooser.set_current_folder(os.path.dirname(self.filename))
            if format is "advanced":
                self.adv_export_name = self.builder.get_object("advanced_export_name")
                self.adv_export_name.set_text(os.path.basename(self.filename)[:-3])
            else:
                filechooser.set_current_name(os.path.basename(self.filename)[:-2] + format)

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

    def export(self, text = ""):
        """Export to pdf, html or odt the given text
                
        Keyword Arguments:
            text {str} -- Text to export (default: {""})
        """

        format = self.stack.get_visible_child_name()

        if format == "advanced":
            self.advanced_export(text)
        else:
            filename = self.filechoosers[format].get_filename()
            if filename.endswith("." + format):
                filename = filename[:-len(format)-1]

            output_dir = os.path.abspath(os.path.join(filename, os.path.pardir))
            basename = os.path.basename(filename)

            args = ['pandoc', '--from=markdown', '-s']

            if format == "pdf":
                args.append("-o%s.pdf" % basename)

            elif format == "odt":
                args.append("-o%s.odt" % basename)

            elif format == "html":
                css = helpers.get_media_file('uberwriter.css')
                relativize = helpers.get_script_path('relative_to_absolute.lua')
                task_list = helpers.get_script_path('task-list.lua')
                args.append("-c%s" % css)
                args.append("-o%s.html" % basename)
                args.append("--mathjax")
                args.append("--lua-filter=" + relativize)
                args.append("--lua-filter=" + task_list)

            p = subprocess.Popen(args, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, cwd=output_dir)
            p.communicate(text)[0]
            
    def advanced_export(self, text = ""):
        tree_iter = self.format_field.get_active_iter()
        if tree_iter != None:
            model = self.format_field.get_model()
            row_id, name = model[tree_iter][:2]

        fmt = self.formats_dict[row_id]
        logger.info(fmt)
        
        filename = self.adv_export_name.get_text()
     
        output_dir = os.path.abspath(self.filechoosers["advanced"].get_current_folder())
        
        basename = os.path.basename(filename)

        args = ['pandoc', '--from=markdown']
        
        to = "--to=%s" % fmt["to"]
        
        if basename.endswith("." + fmt["ext"]):
            output_file = "--output=%s" % basename
        else:
            output_file = "--output=%s.%s" % (basename, fmt["ext"])

        if self.builder.get_object("toc").get_active():
            args.append('--toc')

        if self.builder.get_object("highlight").get_active == False:
            args.append('--no-highlight')
        else:
            hs = self.builder.get_object("highlight_style").get_active_text()
            args.append("--highlight-style=%s" % hs)
        
        if self.builder.get_object("standalone").get_active():
            args.append("--standalone")

        if self.builder.get_object("number_sections").get_active():
            args.append("--number-sections")
        
        if self.builder.get_object("strict").get_active():
            args.append("--strict")
        
        if self.builder.get_object("incremental").get_active():
            args.append("--incremental")

        if self.builder.get_object("self_contained").get_active():
            args.append("--self-contained")

        if self.builder.get_object("html5").get_active():
            if fmt["to"] == "html":
                to = "--to=%s" % "html5"
              
        if self.builder.get_object("smart").get_active():
            smart = '+smart'
        else:
            smart = '-smart'

        if fmt["to"] != "pdf":
            args.append(to + smart)

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

        logger.info(args)

        p = subprocess.Popen(args, stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, cwd=output_dir)
      
        p.communicate(text)[0]
        