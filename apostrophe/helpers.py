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

"""Helpers for the application."""
import logging
import os
import shutil
from contextlib import contextmanager

from typing import List

from gettext import gettext as _

import gi
import pypandoc
from gi.overrides.Pango import Pango

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gio, Handy  # pylint: disable=E0611

from apostrophe.settings import Settings
from apostrophe import config

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
    dialog = Gtk.MessageDialog(
        parent, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, message)

    dialog.set_title(_("Error"))
    dialog.run()
    dialog.destroy()


def exist_executable(command):
    """return if a command can be executed in the SO

    Arguments:
        command {str} -- a command

    Returns:
        {bool} -- if the given command exists in the system
    """

    return shutil.which(command) is not None


def get_descendant(widget, child_name, level, doPrint=False):
    if widget is not None:
        if doPrint:
            print("-" * level + str(Gtk.Buildable.get_name(widget)) +
                  " :: " + widget.get_name())
    else:
        if doPrint:
            print("-" * level + "None")
        return None
    # /*** If it is what we are looking for ***/
    if Gtk.Buildable.get_name(widget) == child_name:  # not widget.get_name() !
        return widget
    # /*** If this widget has one child only search its child ***/
    if (hasattr(widget, 'get_child') and
            callable(getattr(widget, 'get_child')) and
            child_name != ""):
        child = widget.get_child()
        if child is not None:
            return get_descendant(child, child_name, level + 1, doPrint)
    # /*** Ity might have many children, so search them ***/
    elif (hasattr(widget, 'get_children') and
          callable(getattr(widget, 'get_children')) and
          child_name != ""):
        children = widget.get_children()
        # /*** For each child ***/
        found = None
        for child in children:
            if child is not None:
                found = get_descendant(child, child_name, level + 1, doPrint)
                if found:
                    return found


def liststore_from_list(str_list: List[str]):
    """return a Gtk.ListStore object of Handy.TypeValues
       constructed after a list of strings

        Arguments:
            str_list {List[str]} -- a list of strings

        Returns:
            {Gtk.ListStore} -- a ListStore of Handy.ValueObjects
    """

    list_store = Gio.ListStore.new(Handy.ValueObject)

    for element in str_list:
        obj = Handy.ValueObject.new(element)
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
