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

"""Helpers for the application."""
import logging
import os
import shutil
from contextlib import contextmanager
from gettext import gettext as _
from typing import List

import gi
import pypandoc
from gi.overrides.Pango import Pango

gi.require_version('Gtk', '4.0')
from gi.repository import Adw, Gio, Gtk, Gdk, Gsk, GLib  # pylint: disable=E0611

from apostrophe import config
from apostrophe.settings import Settings


__apostrophe_data_directory__ = '../data/'

App = Gio.Application.get_default


@contextmanager
def user_action(text_buffer):
    text_buffer.begin_user_action()
    yield text_buffer
    text_buffer.end_user_action()


def get_media_path(path):
    """Return the full path of a given path under the media dir
       (doesn't start with file:///)
    """
    media_path = "{}{}".format(config.PKGDATA_DIR, path)
    if not os.path.exists(media_path):
        media_path = None
    return media_path


class NullHandler(logging.Handler):
    def emit(self, _record):
        pass


def set_up_logging(level):
    # add a handler to prevent basicConfig
    root = logging.getLogger()
    null_handler = NullHandler()
    root.addHandler(null_handler)

    formatter = logging.Formatter(
        "%(levelname)s:%(name)s: %(funcName)s() '%(message)s'")

    logger = logging.getLogger('apostrophe')
    logger_sh = logging.StreamHandler()
    logger_sh.setFormatter(formatter)
    logger.addHandler(logger_sh)

    # Set the logging level to show debug messages.
    if level == 1:
        logger.setLevel(logging.DEBUG)
        logger.debug('logging enabled')


def show_error(parent, message):
    dialog = Adw.MessageDialog.new(parent, _("Error"), message)
    dialog.add_response("close", _("Close"))
    dialog.set_close_response("close")
    dialog.show()

def exist_executable(command):
    """return if a command can be executed in the SO

    Arguments:
        command {str} -- a command

    Returns:
        {bool} -- if the given command exists in the system
    """

    return shutil.which(command) is not None


def liststore_from_list(str_list: List[str]):
    """return a Gtk.ListStore object of Gtk.StringObjects
       constructed after a list of strings

        Arguments:
            str_list {List[str]} -- a list of strings

        Returns:
            {Gtk.ListStore} -- a ListStore of Gtk.StringObject
    """

    list_store = Gio.ListStore.new(Gtk.StringObject)

    for element in str_list:
        obj = Gtk.StringObject.new(element)
        list_store.append(obj)

    return list_store


def get_char_width(widget):
    return Pango.units_to_double(
        widget.get_pango_context().get_metrics().get_approximate_char_width())


def pandoc_convert(text, to="html5", args=[], outputfile=None):
    fr = Settings.new().get_value('input-format').get_string() or "markdown"
    # args.extend(["--quiet"])
    return pypandoc.convert_text(
        text, to, fr, extra_args=args, outputfile=outputfile)

def get_debug_info():
    flatpak = "yes" if os.path.isfile("/.flatpak-info") else "no"
    os_name = GLib.get_os_info("NAME")
    os_version = GLib.get_os_info("VERSION")
    gtk_theme = os.getenv("GTK_THEME")

    default_display = Gdk.Display.get_default()
    display = type(default_display).__name__.strip("Gdk").strip("Display")
    default_surface = Gdk.Surface.new_toplevel(default_display)
    gsk_renderer = Gsk.Renderer.new_for_surface(default_surface)
    renderer = type(gsk_renderer).__name__.strip("Renderer")
    Gsk.Renderer.unrealize(gsk_renderer)

    info = ""
    info += f"Apostrophe {config.VERSION}\n"
    info += "\n"
    info += f"Flatpak: {flatpak}\n"
    info += f"GTK: {Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}\n"
    info += f"GLib: {GLib.glib_version[0]}.{GLib.glib_version[1]}.{GLib.glib_version[2]}\n"
    info += f"Libadwaita: {Adw.get_major_version()}.{Adw.get_minor_version()}.{Adw.get_micro_version()}\n"
    info += f"Pandoc: {pypandoc.get_pandoc_version()}\n"
    info += "\n"
    info += f"OS: {os_name} {os_version}\n"
    info += f"Display: {display}\n"
    info += f"Renderer: {renderer}\n"
    info += "\n"
    info += f"gtk-theme-name: {Gtk.Settings.get_default().props.gtk_theme_name}\n"
    info += f"GTK_THEME: {gtk_theme}\n"
    info += "\n"

    settings = Settings.new()
    schema = settings.props.settings_schema
    for key in schema.list_keys():
        info +=f"{key}: {settings.get_value(key)}\n"

    return info