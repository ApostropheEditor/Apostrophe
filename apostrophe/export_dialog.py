# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
# Copyright (C) 2019, Wolf Vollprecht <w.vollprecht@gmail.com>
#               2021, Manuel Genovés <manuel.genoves@gmail.com>
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

"""Manages all the export operations and dialogs
"""

# pylint: disable=no-member

import logging
import os
from gettext import gettext as _

from zipfile import ZipFile
import json

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gdk, Gio, GObject, Handy

from apostrophe import helpers
from apostrophe.theme_switcher import Theme

LOGGER = logging.getLogger('apostrophe')


class Format(GObject.Object):

    def __init__(self, name, ext, to, **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.ext: str = ext
        self.to: str = to

    @property
    def has_pages(self):
        return self.to in {"pdf", "odt", "docx"}

    @property
    def is_html(self):
        return self.to == "html5"

    @property
    def has_syntax(self):
        return self.ext in {"html", "tex", "docx", "pdf"}

    @property
    def is_presentation(self):
        return self.to in {"beamer", "revealjs", "dzslides"}

    @property
    def requires_texlive(self):
        return self.ext in {"tex", "pdf"}


class ExportDialog:

    __gtype_name__ = "ExportDialog"

    formats = {
        "pdf":
        {
            "name": "PDF",
            "extension": "pdf",
            "to": "pdf",
            "mimetype": "application/pdf",
            "args": ["--pdf-engine=xelatex",
                     "--variable=papersize:a4"]
        },
        "html":
        {
            "name": "HTML",
            "extension": "html",
            "to": "html5",
            "mimetype": "text/html",
            "args": ["--self-contained",
                     "--css=%s" % Theme.get_current().web_css,
                     "--mathjax",
                     "--lua-filter=%s"
                     % helpers.get_media_path('/lua/relative_to_absolute.lua'),
                     "--lua-filter=%s"
                     % helpers.get_media_path('/lua/task-list.lua')]
        },
        "odt":
        {
            "name": "ODT",
            "extension": "odt",
            "to": "odt",
            "mimetype": "application/vnd.oasis.opendocument.text",
            "args": ["--variable=papersize:a4"]
        }
    }

    def __init__(self, file, _format, text):
        self.format = _format
        self.text = text

        self._show_texlive_warning = (self.format == "pdf" and
                                      not helpers.exist_executable("pdftex"))

        if (self._show_texlive_warning):
            self.dialog = Gtk.MessageDialog(
                None,
                Gtk.DialogFlags.MODAL |
                Gtk.DialogFlags.DESTROY_WITH_PARENT,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CLOSE
            )

            self.dialog.get_message_area().add(TexliveWarning())

        else:
            self.dialog = Gtk.FileChooserNative.new(
                          _("Export"),
                          None,
                          Gtk.FileChooserAction.SAVE,
                          _("Export to %s") %
                          self.formats[self.format]["name"],
                          _("Cancel"))

            dialog_filter = Gtk.FileFilter.new()
            dialog_filter.set_name(self.formats[self.format]["name"])
            dialog_filter.add_mime_type(self.formats[self.format]["mimetype"])
            self.dialog.add_filter(dialog_filter)
            self.dialog.set_do_overwrite_confirmation(True)

            self.dialog.set_current_name(
                file.name + '.' + self.formats[self.format]["extension"])

    def export(self):
        response = self.dialog.run()

        if not self._show_texlive_warning:
            file = self.dialog.get_file()
            fmt = self.formats[self.format]["to"]
            args = self.formats[self.format]["args"]

            if response == Gtk.ResponseType.ACCEPT:
                try:
                    export(self.text, file, fmt, args)
                except (NotADirectoryError, RuntimeError) as e:
                    helpers.show_error(
                        None,
                        _("An error happened while trying to export:\n\n"
                          "{err_msg}")
                        .format(err_msg=str(e).encode()
                                .decode("unicode-escape")))

        self.dialog.destroy()


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/Export.ui')
class AdvancedExportDialog(Handy.Window):

    __gtype_name__ = "AdvancedExportDialog"

    headerbar = Gtk.Template.Child()

    formats_list = Gtk.Template.Child()

    leaflet = Gtk.Template.Child()
    options_page = Gtk.Template.Child()
    formats_page = Gtk.Template.Child()

    # #### --option properties-- #####
    sw_standalone = Gtk.Template.Child()
    sw_toc = Gtk.Template.Child()
    sw_numbers = Gtk.Template.Child()

    cmb_page_size = Gtk.Template.Child()

    sw_self_contained = Gtk.Template.Child()

    sw_syntax_highlighting = Gtk.Template.Child()
    cmb_syntax_highlighting = Gtk.Template.Child()

    sw_incremental_bullets = Gtk.Template.Child()
    # #### ---------------------- #####

    formats = Gio.ListStore.new(Format)

    page_sizes = ['A4', 'Letter']
    syntax_styles = ['pygments',
                     'kate',
                     'monochrome',
                     'espresso',
                     'zenburn',
                     'haddock',
                     'tango']

    def __init__(self, file, text, **kwargs):
        super().__init__(**kwargs)

        self.file = file
        self.text = text

        if not self.formats:
            with open(helpers.get_media_path("/media/formats.json")) as f:
                _formats_list = json.load(f)
            for _i, format in enumerate(_formats_list):
                self.formats.append(Format(format["name"],
                                           format["ext"],
                                           format["to"]))

        self.formats_list.bind_model(self.formats, self.row_constructor, None)
        self.formats_list.select_row(self.formats_list.get_row_at_index(0))

        page_sizes_list = helpers.liststore_from_list(self.page_sizes)
        self.cmb_page_size.bind_name_model(page_sizes_list,
                                           self.get_hdy_name, None, None)

        syntax_styles_list = helpers.liststore_from_list(self.syntax_styles)
        self.cmb_syntax_highlighting.bind_name_model(syntax_styles_list,
                                                     self.get_hdy_name,
                                                     None, None)

    @GObject.Property(type=str)
    def title(self):
        name = self.formats_list.get_selected_row().item.name
        return _("Export to {}").format(name)

    @GObject.Property(type=bool, default=False)
    def show_page_size_options(self):
        return self.formats_list.get_selected_row().item.has_pages

    @GObject.Property(type=bool, default=False)
    def show_html_options(self):
        return self.formats_list.get_selected_row().item.is_html

    @GObject.Property(type=bool, default=False)
    def show_syntax_options(self):
        return self.formats_list.get_selected_row().item.has_syntax

    @GObject.Property(type=bool, default=False)
    def show_presentation_options(self):
        return self.formats_list.get_selected_row().item.is_presentation

    @GObject.Property(type=bool, default=False)
    def show_texlive_warning(self):
        is_tex = self.formats_list.get_selected_row().item.requires_texlive
        texlive_installed = helpers.exist_executable("pdftex")

        return is_tex and not texlive_installed

    @GObject.Property(type=bool, default=False)
    def show_go_back_button(self):
        folded = self.leaflet.props.folded
        on_options_page = (self.leaflet.get_visible_child() ==
                           self.options_page)

        return folded and on_options_page

    @GObject.Property(type=str, default="options")
    def options_page_name(self):
        name = "texlive_warning" if self.show_texlive_warning else "options"
        return name

    @GObject.Property(type=bool, default=False)
    def exports_multiple_files(self):
        return self.formats_list.get_selected_row().item.to == "revealjs"

    def row_constructor(self, item, _user_data):
        row = Handy.ActionRow.new()
        row.item = item
        row.set_title(item.name)

        return row

    def get_hdy_name(self, item, _user_data, _user_data_free):
        return item.dup_string()

    def get_hdy_comborow_name(self, hdy_cmbrow):
        model = hdy_cmbrow.get_model()
        index = hdy_cmbrow.get_selected_index()
        item = model.get_item(index)

        return item.dup_string()

    @Gtk.Template.Callback()
    def reveal_go_back(self, _widget, *args):
        self.notify("show_go_back_button")

    @Gtk.Template.Callback()
    def go_back(self, _widget):
        self.leaflet.set_visible_child(self.formats_page)

    @Gtk.Template.Callback()
    def on_format_selected(self, _widget, _row):
        self.leaflet.set_visible_child(self.options_page)

        self.notify("show_page_size_options")
        self.notify("show_html_options")
        self.notify("show_syntax_options")
        self.notify("show_presentation_options")
        self.notify("show_texlive_warning")
        self.notify("options_page_name")
        self.notify("title")

    @Gtk.Template.Callback()
    def on_destroy(self, _widget):
        self.destroy()

    @Gtk.Template.Callback()
    def export(self, widget):
        self.retrieve_args()

        if self.exports_multiple_files:
            export_dialog = Gtk.FileChooserNative.new(
                _("Export"), None, Gtk.FileChooserAction.SELECT_FOLDER,
                _("Select folder"), _("Cancel"))
        else:
            export_dialog = Gtk.FileChooserNative.new(
                _("Export"), None,  Gtk.FileChooserAction.SAVE,
                _("Export to %s") %
                self.formats_list.get_selected_row().item.name, _("Cancel"))

            export_dialog.set_current_name(
                self.file.name + '.' +
                self.formats_list.get_selected_row().item.ext)

        export_dialog.set_transient_for(self)
        export_dialog.set_do_overwrite_confirmation(True)

        response = export_dialog.run()
        if self.exports_multiple_files:
            folder = export_dialog.get_file()
            with ZipFile(helpers.get_media_path("/media/reveal.js.zip"),
                         "r") as zipObj:
                zipObj.extractall(folder.get_path())
            export_file = folder.get_child(self.file.name + '.' +
                              self.formats_list.get_selected_row().item.ext)
        else:
            export_file = export_dialog.get_file()

        fmt = self.formats_list.get_selected_row().item.to
        args = self.retrieve_args()

        if response == Gtk.ResponseType.ACCEPT:
            try:
                export(self.text, export_file, fmt, args)
            except (NotADirectoryError, RuntimeError) as e:
                helpers.show_error(
                    None,
                    _("An error happened while trying to export:\n\n{err_msg}")
                    .format(err_msg=str(e).encode().decode("unicode-escape")))

        export_dialog.destroy()
        self.destroy()

    def retrieve_args(self):
        args = []

        if self.formats_list.get_selected_row().item.ext == "pdf":
            args.append("--pdf-engine=xelatex")

        if self.sw_standalone.get_active():
            args.append("--standalone")
        if self.sw_toc.get_active():
            args.append("--toc")
        if self.sw_numbers.get_active():
            args.append("--number-sections")

        if (self.show_page_size_options and
           self.cmb_page_size.get_selected_index() == 0):
            if ((fmt := self.formats_list.get_selected_row().item.to) in
               {"pdf", "latex", "context"}):
                args.append("--variable=papersize:a4")
            elif fmt in ("odt", "docx"):
                args.append("--reference-doc=" + helpers.get_media_path(
                    "/reference_files/reference-a4." + fmt))

        if self.show_html_options:
            args.append("--css=%s" % Theme.get_current().web_css)
            args.append("--mathjax")
            args.append("--lua-filter=%s" % helpers.get_media_path(
                '/lua/relative_to_absolute.lua'))
            args.append("--lua-filter=%s" % helpers.get_media_path(
                '/lua/task-list.lua'))
            if self.sw_self_contained.get_active():
                args.append("--self-contained")

        if self.show_syntax_options:
            if self.sw_syntax_highlighting.get_enable_expansion():
                selected_style = self.get_hdy_comborow_name(
                    self.cmb_syntax_highlighting)
                args.append("--highlight-style={}".format(selected_style))

        if self.show_presentation_options:
            if self.sw_incremental_bullets.get_active():
                args.append("--incremental")

        if self.formats_list.get_selected_row().item.to == "revealjs":
            args.extend(["-V", "revealjs-url=reveal.js"])

        return args


@Gtk.Template(resource_path='/org/gnome/gitlab/somas/Apostrophe/ui/TexliveWarning.ui')
class TexliveWarning(Gtk.Stack):

    __gtype_name__ = 'TexliveWarning'
    command = Gtk.Template.Child()

    def __init__(self):
        super().__init__()
        child_name = "flatpak" if os.path.isfile("/.flatpak-info") else "distro"
        self.set_visible_child_name(child_name)

    @Gtk.Template.Callback()
    def copy(self, _widget):
        cb = Gtk.Clipboard.get_default(Gdk.Display.get_default())
        cb.set_text(self.command.get_text(), -1)


def export(text, file, _format, args):
    """Export the given text using the specified format.
    For advanced export, this includes special flags for the enabled options.

    Keyword Arguments:
        text {str} -- Text to export (default: {""})
    """

    to = _format

    helpers.pandoc_convert(
        text, to=to, args=args, outputfile=file.get_path())
